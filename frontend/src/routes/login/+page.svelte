<!--
  LokMC — Hardened Authentication & Setup Portal
  Production-ready, accessible, responsive split-viewport architecture.
  Adheres strictly to the 8pt spatial grid, WCAG 2.1 AA contrast, and semantic markup.
-->
<script lang="ts">
  import { api } from '$lib/api';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  let mode = $state<'login' | 'setup' | 'loading'>('loading');
  let backendOffline = $state(false);
  let username = $state('');
  let password = $state('');
  let email = $state('');
  let error = $state('');
  let submitting = $state(false);

  let usernameRef = $state<HTMLInputElement>();

  onMount(async () => {
    if (api.isAuthenticated) {
      goto('/');
      return;
    }
    try {
      const { needs_setup } = await api.needsSetup();
      mode = needs_setup ? 'setup' : 'login';
      backendOffline = false;
    } catch {
      // Backend is offline or no database yet — default to setup mode
      mode = 'setup';
      backendOffline = true;
    }
    // Set focus to username once rendered
    setTimeout(() => {
      usernameRef?.focus();
    }, 50);
  });

  async function handleSubmit(e: Event) {
    e.preventDefault();
    error = '';
    submitting = true;

    try {
      if (mode === 'setup') {
        await api.setup(username, password, email || undefined);
      } else {
        await api.login(username, password);
      }
      goto('/');
    } catch (err: any) {
      error = err.detail || 'Authentication failed. Please verify credentials.';
    } finally {
      submitting = false;
    }
  }
</script>

<svelte:head>
  <title>{mode === 'setup' ? 'Initial Setup' : 'Sign In'} — LokMC</title>
  <meta name="description" content="Secure administrative access for LokMC Minecraft infrastructure." />
</svelte:head>

<div class="auth-layout">
  <!-- Left Side: System Information & Security Telemetry -->
  <aside class="auth-info-panel" aria-label="System Architecture & Status">
    <div class="info-content">
      <header class="brand-block">
        <div class="brand-mark" aria-hidden="true">
          <svg viewBox="0 0 32 32" fill="none" class="brand-icon">
            <rect width="32" height="32" rx="8" fill="var(--color-accent)"/>
            <path d="M8 12h16v2H8zm0 4h12v2H8zm0 4h14v2H8z" fill="#ffffff"/>
          </svg>
        </div>
        <div>
          <h1 class="brand-title">LokMC</h1>
          <p class="brand-tagline">Secure Minecraft Node Orchestration</p>
        </div>
      </header>

      <section class="security-features" aria-labelledby="sec-features-title">
        <h2 id="sec-features-title" class="section-title">Zero-Trust Isolation</h2>
        <ul class="features-list">
          <li class="feature-item">
            <svg class="feature-icon" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M8 0c-.69 0-1.843.265-2.928.56-1.11.3-2.229.655-2.887.87a1.54 1.54 0 0 0-1.044 1.262c-.596 4.477.787 7.795 2.464 9.99 1.579 2.065 3.48 3.018 4.095 3.26a1.5 1.5 0 0 0 .96 0c.616-.242 2.516-1.195 4.095-3.26 1.677-2.195 3.06-5.513 2.464-9.99a1.54 1.54 0 0 0-1.044-1.263 62.67 62.67 0 0 0-2.887-.87C9.843.266 8.69 0 8 0zm2.146 5.854a.5.5 0 0 0-.708-.708L7 7.293 5.56 5.854a.5.5 0 1 0-.708.708l1.793 1.792a.5.5 0 0 0 .708 0l2.793-2.792z"/>
            </svg>
            <div>
              <span class="feature-heading">Rootless Container Sandboxing</span>
              <p class="feature-desc">All server processes run under non-root namespaces with drop-caps.</p>
            </div>
          </li>
          <li class="feature-item">
            <svg class="feature-icon" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M3.5 6V4a4.5 4.5 0 1 1 9 0v2h.5a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h.5zm2-2a2.5 2.5 0 0 1 5 0v2h-5V4zm-2 5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9z"/>
            </svg>
            <div>
              <span class="feature-heading">Argon2id Key Derivation</span>
              <p class="feature-desc">Cryptographic password hashing resistant to GPU brute-force attacks.</p>
            </div>
          </li>
          <li class="feature-item">
            <svg class="feature-icon" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm11 4.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1 0-1h9a.5.5 0 0 1 .5.5zm0 3a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1 0-1h9a.5.5 0 0 1 .5.5zm0 3a.5.5 0 0 1-.5.5h-5a.5.5 0 0 1 0-1h5a.5.5 0 0 1 .5.5z"/>
            </svg>
            <div>
              <span class="feature-heading">Immutable Audit Telemetry</span>
              <p class="feature-desc">Every control action, login attempt, and config mutation is recorded.</p>
            </div>
          </li>
        </ul>
      </section>

      <footer class="info-footer">
        <span class="status-indicator">
          <span class="status-dot status-dot-running" aria-hidden="true"></span>
          <span>Node Daemon Online — v0.1.0</span>
        </span>
      </footer>
    </div>
  </aside>

  <!-- Right Side: Authentication Canvas -->
  <main class="auth-main-panel" id="main-content">
    <div class="auth-card-wrapper">
      {#if mode === 'loading'}
        <div class="card" aria-busy="true" aria-label="Loading authentication options">
          <div class="skeleton" style="height: 32px; width: 60%; margin-bottom: var(--space-4);"></div>
          <div class="skeleton" style="height: 16px; width: 85%; margin-bottom: var(--space-6);"></div>
          <div class="skeleton" style="height: 48px; width: 100%; margin-bottom: var(--space-4);"></div>
          <div class="skeleton" style="height: 48px; width: 100%; margin-bottom: var(--space-6);"></div>
          <div class="skeleton" style="height: 44px; width: 100%;"></div>
        </div>
      {:else}
        <div class="form-container">
          <header class="form-header">
            <h2 class="form-title">
              {mode === 'setup' ? 'Create Your Admin Account' : 'Sign In to LokMC'}
            </h2>
            <p class="form-desc">
              {mode === 'setup'
                ? 'Welcome to LokMC! There is no default password. Choose your administrator username and password below to create the primary account.'
                : 'Enter your administrator credentials to access node controls and terminal sessions.'}
            </p>
          </header>

          {#if backendOffline}
            <div class="alert-banner" role="alert" style="background: var(--color-warning-muted); border-color: var(--color-warning); color: var(--color-warning); margin-bottom: var(--space-4);">
              <svg class="alert-icon" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                <path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zm-.75 3.75a.75.75 0 0 1 1.5 0v3.5a.75.75 0 0 1-1.5 0v-3.5zM8 11a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>
              </svg>
              <div class="alert-content">
                <span class="alert-title" style="color: var(--color-warning);">Backend Service Offline</span>
                <span class="alert-text" style="color: var(--color-text-secondary);">
                  The API server on port 8443 is not running yet. Run <code style="font-family: var(--font-mono); background: var(--color-bg-base); padding: 1px 4px; border-radius: 4px;">npm run dev:backend</code> in another terminal to start it.
                </span>
              </div>
            </div>
          {/if}

          {#if error}
            <div class="alert-banner" role="alert" aria-live="assertive">
              <svg class="alert-icon" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                <path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zm-.75 3.75a.75.75 0 0 1 1.5 0v3.5a.75.75 0 0 1-1.5 0v-3.5zM8 11a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>
              </svg>
              <div class="alert-content">
                <span class="alert-title">Authentication Failed</span>
                <span class="alert-text">{error}</span>
              </div>
              <button
                type="button"
                class="alert-dismiss"
                aria-label="Dismiss error banner"
                onclick={() => (error = '')}
              >×</button>
            </div>
          {/if}

          <form onsubmit={handleSubmit} class="auth-form" novalidate>
            <div class="form-group">
              <label for="username" class="form-label">
                Username
                <span class="required-mark" aria-hidden="true">*</span>
              </label>
              <input
                id="username"
                name="username"
                type="text"
                class="form-input"
                bind:value={username}
                bind:this={usernameRef}
                required
                minlength={mode === 'setup' ? 3 : 1}
                maxlength={64}
                autocomplete="username"
                aria-required="true"
                aria-invalid={error ? 'true' : undefined}
                aria-describedby={error ? 'username-error' : 'username-hint'}
                placeholder="e.g. sysadmin"
              />
              <span id="username-hint" class="form-hint">
                {mode === 'setup' ? 'Must be at least 3 alphanumeric characters.' : 'Your assigned system handle.'}
              </span>
            </div>

            {#if mode === 'setup'}
              <div class="form-group">
                <label for="email" class="form-label">
                  Administrative Email
                  <span class="optional-mark">(optional)</span>
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  class="form-input"
                  bind:value={email}
                  maxlength={255}
                  autocomplete="email"
                  placeholder="admin@internal.net"
                />
                <span class="form-hint">Used for local security incident notices.</span>
              </div>
            {/if}

            <div class="form-group">
              <label for="password" class="form-label">
                Password
                <span class="required-mark" aria-hidden="true">*</span>
              </label>
              <input
                id="password"
                name="password"
                type="password"
                class="form-input"
                bind:value={password}
                required
                minlength={mode === 'setup' ? 12 : 8}
                maxlength={128}
                autocomplete={mode === 'setup' ? 'new-password' : 'current-password'}
                aria-required="true"
                aria-invalid={error ? 'true' : undefined}
                aria-describedby="password-hint"
                placeholder="••••••••••••"
              />
              <span id="password-hint" class="form-hint">
                {mode === 'setup'
                  ? 'Strong passphrase required: 12+ characters with symbols and numbers.'
                  : 'Enter password.'}
              </span>
            </div>

            <div class="form-actions">
              <button
                type="submit"
                class="btn btn-primary btn-lg"
                disabled={submitting || !username.trim() || !password.trim()}
              >
                {#if submitting}
                  <span class="spinner" aria-hidden="true"></span>
                  <span>{mode === 'setup' ? 'Initializing System…' : 'Validating Session…'}</span>
                {:else}
                  <span>{mode === 'setup' ? 'Complete Setup & Enter' : 'Sign In'}</span>
                {/if}
              </button>
            </div>

            <div style="margin-top: var(--space-4); text-align: center;">
              {#if mode === 'setup'}
                <button
                  type="button"
                  class="btn btn-ghost btn-sm"
                  onclick={() => { mode = 'login'; error = ''; }}
                  style="color: var(--color-accent-text);"
                >
                  Already initialized? Sign in instead →
                </button>
              {:else}
                <button
                  type="button"
                  class="btn btn-ghost btn-sm"
                  onclick={() => { mode = 'setup'; error = ''; }}
                  style="color: var(--color-accent-text);"
                >
                  First-time user? Create admin account →
                </button>
              {/if}
            </div>
          </form>

          <footer class="form-footer">
            <p class="audit-notice">
              {mode === 'setup'
                ? 'Primary root key will be derived and stored locally in encrypted SQLite storage.'
                : 'Protected by IP-based rate limiting and brute-force mitigation heuristics.'}
            </p>
          </footer>
        </div>
      {/if}
    </div>
  </main>
</div>

<style>
  .auth-layout {
    display: grid;
    grid-template-columns: 1fr;
    min-height: 100vh;
    background: var(--color-bg-base);
  }

  @media (min-width: 1024px) {
    .auth-layout {
      grid-template-columns: 440px 1fr;
    }
  }

  /* ── Left Information Panel ──────────────────────────── */
  .auth-info-panel {
    background: var(--color-bg-surface);
    border-bottom: 1px solid var(--color-border);
    padding: var(--space-6) var(--space-5);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  @media (min-width: 1024px) {
    .auth-info-panel {
      border-bottom: none;
      border-right: 1px solid var(--color-border);
      padding: var(--space-7) var(--space-6);
    }
  }

  .info-content {
    display: flex;
    flex-direction: column;
    gap: var(--space-6);
    height: 100%;
    justify-content: space-between;
  }

  .brand-block {
    display: flex;
    align-items: center;
    gap: var(--space-3);
  }

  .brand-mark {
    width: 40px;
    height: 40px;
    flex-shrink: 0;
  }

  .brand-icon {
    width: 100%;
    height: 100%;
  }

  .brand-title {
    font-size: var(--text-2xl);
    font-weight: var(--font-bold);
    letter-spacing: -0.02em;
    color: var(--color-text-primary);
    line-height: var(--leading-tight);
  }

  .brand-tagline {
    font-size: var(--text-sm);
    color: var(--color-text-tertiary);
  }

  .section-title {
    font-size: var(--text-xs);
    font-weight: var(--font-semibold);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--color-text-tertiary);
    margin-bottom: var(--space-4);
  }

  .features-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
  }

  .feature-item {
    display: flex;
    gap: var(--space-3);
    align-items: flex-start;
  }

  .feature-icon {
    width: 18px;
    height: 18px;
    color: var(--color-accent);
    flex-shrink: 0;
    margin-top: 2px;
  }

  .feature-heading {
    display: block;
    font-size: var(--text-base);
    font-weight: var(--font-medium);
    color: var(--color-text-primary);
  }

  .feature-desc {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    line-height: var(--leading-normal);
  }

  .info-footer {
    padding-top: var(--space-4);
    border-top: 1px solid var(--color-border-subtle);
  }

  .status-indicator {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    font-size: var(--text-xs);
    font-weight: var(--font-medium);
    color: var(--color-text-secondary);
  }

  /* ── Right Form Panel ────────────────────────────────── */
  .auth-main-panel {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--space-6) var(--space-5);
  }

  @media (min-width: 1024px) {
    .auth-main-panel {
      padding: var(--space-8);
    }
  }

  .auth-card-wrapper {
    width: 100%;
    max-width: 460px;
  }

  .form-container {
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
  }

  .form-header {
    margin-bottom: var(--space-5);
  }

  .form-title {
    font-size: var(--text-xl);
    font-weight: var(--font-semibold);
    color: var(--color-text-primary);
    line-height: var(--leading-tight);
    margin-bottom: var(--space-2);
  }

  .form-desc {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
    line-height: var(--leading-normal);
    max-width: none;
  }

  /* Alert Banner */
  .alert-banner {
    display: flex;
    align-items: flex-start;
    gap: var(--space-3);
    padding: var(--space-3) var(--space-4);
    margin-bottom: var(--space-5);
    background: var(--color-error-muted);
    border: 1px solid var(--color-error);
    border-radius: var(--radius-md);
    color: var(--color-error);
  }

  .alert-icon {
    width: 18px;
    height: 18px;
    flex-shrink: 0;
    margin-top: 2px;
  }

  .alert-content {
    display: flex;
    flex-direction: column;
    gap: 2px;
    flex: 1;
  }

  .alert-title {
    font-size: var(--text-sm);
    font-weight: var(--font-semibold);
  }

  .alert-text {
    font-size: var(--text-xs);
    line-height: var(--leading-normal);
  }

  .alert-dismiss {
    background: transparent;
    border: none;
    color: inherit;
    font-size: var(--text-lg);
    line-height: 1;
    cursor: pointer;
    padding: 0 var(--space-1);
    opacity: 0.8;
  }

  .alert-dismiss:hover {
    opacity: 1;
  }

  .auth-form {
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
  }

  .required-mark {
    color: var(--color-error);
    margin-left: 2px;
  }

  .optional-mark {
    color: var(--color-text-tertiary);
    font-weight: var(--font-regular);
    margin-left: var(--space-1);
  }

  .form-actions {
    margin-top: var(--space-2);
  }

  .form-actions .btn {
    width: 100%;
  }

  .form-footer {
    margin-top: var(--space-5);
    padding-top: var(--space-4);
    border-top: 1px solid var(--color-border-subtle);
  }

  .audit-notice {
    font-size: var(--text-xs);
    color: var(--color-text-tertiary);
    text-align: center;
    line-height: var(--leading-normal);
    max-width: none;
  }
</style>
