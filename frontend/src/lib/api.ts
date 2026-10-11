/**
 * LokMC — High-Performance API Client
 *
 * Features:
 * - Request deduplication (coalesces identical concurrent GET requests)
 * - In-memory TTL caching for hot endpoints (profile, server details)
 * - Automatic token refresh on 401 with retry
 * - Safe fallback handling when daemon is offline
 */

import { browser } from '$app/environment';

const API_BASE = '/api';

interface ApiError {
  detail: string;
  status: number;
}

interface CacheEntry<T> {
  data: T;
  timestamp: number;
}

class LokMCApi {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  // In-memory request deduplication map
  private inFlightRequests = new Map<string, Promise<any>>();

  // In-memory TTL cache
  private cache = new Map<string, CacheEntry<any>>();

  constructor() {
    if (browser) {
      this.accessToken = localStorage.getItem('lokmc_access_token');
      this.refreshToken = localStorage.getItem('lokmc_refresh_token');
    }
  }

  setTokens(access: string, refresh: string) {
    this.accessToken = access;
    this.refreshToken = refresh;
    this.cache.clear();
    if (browser) {
      localStorage.setItem('lokmc_access_token', access);
      localStorage.setItem('lokmc_refresh_token', refresh);
    }
  }

  clearTokens() {
    this.accessToken = null;
    this.refreshToken = null;
    this.cache.clear();
    if (browser) {
      localStorage.removeItem('lokmc_access_token');
      localStorage.removeItem('lokmc_refresh_token');
    }
  }

  get isAuthenticated(): boolean {
    return this.accessToken !== null;
  }

  clearCache(pattern?: string) {
    if (!pattern) {
      this.cache.clear();
      return;
    }
    for (const key of this.cache.keys()) {
      if (key.includes(pattern)) {
        this.cache.delete(key);
      }
    }
  }

  private async request<T>(
    path: string,
    options: RequestInit = {},
    ttlMs: number = 0
  ): Promise<T> {
    const isGet = !options.method || options.method.toUpperCase() === 'GET';
    const cacheKey = `${isGet ? 'GET' : options.method}:${path}`;

    // 1. Check TTL cache for GET requests
    if (isGet && ttlMs > 0) {
      const cached = this.cache.get(cacheKey);
      if (cached && Date.now() - cached.timestamp < ttlMs) {
        return cached.data;
      }
    }

    // 2. Coalesce identical concurrent in-flight GET requests
    if (isGet && this.inFlightRequests.has(cacheKey)) {
      return this.inFlightRequests.get(cacheKey) as Promise<T>;
    }

    const fetchPromise = this.executeFetch<T>(path, options, cacheKey, ttlMs);

    if (isGet) {
      this.inFlightRequests.set(cacheKey, fetchPromise);
    }

    try {
      return await fetchPromise;
    } finally {
      if (isGet) {
        this.inFlightRequests.delete(cacheKey);
      }
    }
  }

  private async executeFetch<T>(
    path: string,
    options: RequestInit,
    cacheKey: string,
    ttlMs: number
  ): Promise<T> {
    const url = `${API_BASE}${path}`;
    const isFormData = typeof FormData !== 'undefined' && options.body instanceof FormData;
    const headers: Record<string, string> = {
      ...(options.headers as Record<string, string> || {}),
    };

    if (!isFormData && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }

    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    const response = await fetch(url, { ...options, headers });

    // Handle token refresh on 401
    if (response.status === 401 && this.refreshToken) {
      const refreshed = await this.tryRefresh();
      if (refreshed) {
        headers['Authorization'] = `Bearer ${this.accessToken}`;
        const retryResponse = await fetch(url, { ...options, headers });
        if (!retryResponse.ok) {
          throw await this.parseError(retryResponse);
        }
        if (retryResponse.status === 204) return undefined as T;
        const data = await retryResponse.json();
        if (ttlMs > 0) {
          this.cache.set(cacheKey, { data, timestamp: Date.now() });
        }
        return data;
      } else {
        this.clearTokens();
        if (browser) {
          window.location.href = '/login';
        }
        throw { detail: 'Session expired', status: 401 } as ApiError;
      }
    }

    if (!response.ok) {
      throw await this.parseError(response);
    }

    if (response.status === 204) return undefined as T;
    const data = await response.json();

    if (ttlMs > 0) {
      this.cache.set(cacheKey, { data, timestamp: Date.now() });
    }

    return data;
  }

  private async tryRefresh(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: this.refreshToken }),
      });
      if (!response.ok) return false;
      const data = await response.json();
      this.setTokens(data.access_token, data.refresh_token);
      return true;
    } catch {
      return false;
    }
  }

  private async parseError(response: Response): Promise<ApiError> {
    try {
      const data = await response.json();
      return { detail: data.detail || 'An error occurred', status: response.status };
    } catch {
      return { detail: response.statusText, status: response.status };
    }
  }

  // ── Auth ────────────────────────────────────────────────

  async needsSetup(): Promise<{ needs_setup: boolean }> {
    return this.request('/auth/needs-setup', {}, 10000);
  }

  async setup(username: string, password: string, email?: string) {
    const data = await this.request<any>('/auth/setup', {
      method: 'POST',
      body: JSON.stringify({ username, password, email }),
    });
    this.setTokens(data.access_token, data.refresh_token);
    return data;
  }

  async login(username: string, password: string) {
    const data = await this.request<any>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    this.setTokens(data.access_token, data.refresh_token);
    return data;
  }

  async logout() {
    await this.request('/auth/logout', { method: 'POST' }).catch(() => {});
    this.clearTokens();
  }

  async getProfile() {
    // 15 seconds TTL cache for user profile
    return this.request<any>('/auth/me', {}, 15000);
  }

  // ── Servers ─────────────────────────────────────────────

  async listServers() {
    // 3 seconds TTL cache for server list
    return this.request<any[]>('/servers', {}, 3000);
  }

  async getServer(id: number) {
    // 3 seconds TTL cache for server details
    return this.request<any>(`/servers/${id}`, {}, 3000);
  }

  async createServer(data: any) {
    this.clearCache('/servers');
    return this.request<any>('/servers', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async startServer(id: number) {
    this.clearCache(`/servers/${id}`);
    this.clearCache('/servers');
    return this.request<any>(`/servers/${id}/start`, { method: 'POST' });
  }

  async stopServer(id: number) {
    this.clearCache(`/servers/${id}`);
    this.clearCache('/servers');
    return this.request<any>(`/servers/${id}/stop`, { method: 'POST' });
  }

  async restartServer(id: number) {
    this.clearCache(`/servers/${id}`);
    this.clearCache('/servers');
    return this.request<any>(`/servers/${id}/restart`, { method: 'POST' });
  }

  async deleteServer(id: number) {
    this.clearCache(`/servers/${id}`);
    this.clearCache('/servers');
    return this.request(`/servers/${id}`, { method: 'DELETE' });
  }

  async importWorld(id: number, file: File, worldName: string = 'world') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('world_name', worldName);

    this.clearCache(`/servers/${id}`);
    this.clearCache('/servers');
    return this.request<{ status: string; message: string; world_name: string; files_extracted: number }>(
      `/servers/${id}/import-world`,
      {
        method: 'POST',
        body: formData,
      }
    );
  }

  async getServerMetrics(id: number) {
    return this.request<any[]>(`/servers/${id}/metrics`, {}, 2000);
  }

  // ── System ──────────────────────────────────────────────

  async getSystemMetrics() {
    return this.request<any>('/system/metrics', {}, 2000);
  }

  async getAuditLogs(category?: string, limit: number = 50, offset: number = 0) {
    const params = new URLSearchParams({ limit: String(limit), offset: String(offset) });
    if (category && category !== 'all') {
      params.append('category', category);
    }
    return this.request<{ total: number; entries: any[] }>(`/audit?${params.toString()}`);
  }

  async getSecurityStatus() {
    return this.request<any>('/settings/security', {}, 10000);
  }

  async healthCheck() {
    return this.request<any>('/health', {}, 5000);
  }
}

export const api = new LokMCApi();
export type { ApiError };
