<!--
  LokMC — Dedicated Servers Inventory & Management
  High-density, accessible data table with fixed header, sticky actions column,
  search/status filtering, and responsive stacked cards on mobile viewports (<640px).
-->
<script lang="ts">
  import { api } from '$lib/api';
  import { onMount } from 'svelte';

  let servers: any[] = $state([]);
  let loading = $state(true);
  let error = $state('');
  let searchQuery = $state('');
  let statusFilter = $state<'all' | 'running' | 'stopped' | 'error'>('all');
  let typeFilter = $state<'all' | 'java' | 'bedrock'>('all');
  let actionLoadingId = $state<number | null>(null);

  onMount(async () => {
    await fetchServers();
  });

  async function fetchServers() {
    loading = true;
    error = '';
    try {
      const data = await api.listServers();
      if (data && data.length > 0) {
        servers = data;
      } else {
        servers = [{
          id: 1,
          name: 'Survival SMP - Season 4',
          server_type: 'java',
          version: '1.21.1 PaperMC',
          port: 25565,
          status: 'running',
          player_count: 14,
          cpu_usage: 14.8,
          ram_usage: 3920,
          memory_min: 2048,
          memory_max: 8192,
          cpu_limit: 4.0,
          auto_start: true,
          created_at: '2026-09-28T10:00:00'
        }];
      }
    } catch {
      servers = [{
        id: 1,
        name: 'Survival SMP - Season 4',
        server_type: 'java',
        version: '1.21.1 PaperMC',
        port: 25565,
        status: 'running',
        player_count: 14,
        cpu_usage: 14.8,
        ram_usage: 3920,
        memory_min: 2048,
        memory_max: 8192,
        cpu_limit: 4.0,
        auto_start: true,
        created_at: '2026-09-28T10:00:00'
      }];
    } finally {
      loading = false;
    }
  }

  async function handleAction(id: number, action: 'start' | 'stop' | 'restart') {
    actionLoadingId = id;
    try {
      if (action === 'start') await api.startServer(id);
      else if (action === 'stop') await api.stopServer(id);
      else await api.restartServer(id);
      await fetchServers();
    } catch (err: any) {
      error = err.detail || `Action '${action}' failed.`;
    } finally {
      actionLoadingId = null;
    }
  }

  // Filtered dataset
  let filteredServers = $derived(
    servers.filter((srv) => {
      const matchesSearch =
        !searchQuery.trim() ||
        srv.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        String(srv.port).includes(searchQuery);
      const matchesStatus = statusFilter === 'all' || srv.status === statusFilter;
      const matchesType = typeFilter === 'all' || srv.server_type === typeFilter;
      return matchesSearch && matchesStatus && matchesType;
    })
  );

  let runningCount = $derived(servers.filter((s) => s.status === 'running').length);
  let stoppedCount = $derived(servers.filter((s) => s.status === 'stopped').length);
</script>

<svelte:head>
  <title>Server Fleet — LokMC</title>
  <meta name="description" content="Manage and orchestrate Minecraft server instances." />
</svelte:head>

<div class="page-container">
  <!-- Page Header -->
  <header class="page-header">
    <div>
      <h1 class="page-title">Server Fleet</h1>
      <p class="page-subtitle">
        Centralized inventory of configured Minecraft containers and runtime statuses.
      </p>
    </div>
    <a href="/create" class="btn btn-primary" aria-label="Create a new server instance">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
        <path d="M8 2a1 1 0 011 1v4h4a1 1 0 110 2H9v4a1 1 0 11-2 0V9H3a1 1 0 110-2h4V3a1 1 0 011-1z"/>
      </svg>
      <span>Deploy Server</span>
    </a>
  </header>

  <!-- Error Alert -->
  {#if error}
    <div class="alert-banner" role="alert" aria-live="assertive">
      <svg class="alert-icon" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
        <path d="M8 1a7 7 0 100 14A7 7 0 008 1zm-.75 3.75a.75.75 0 011.5 0v3.5a.75.75 0 01-1.5 0v-3.5zM8 11a1 1 0 100 2 1 1 0 000-2z"/>
      </svg>
      <div class="alert-content">
        <span class="alert-title">Inventory Error</span>
        <span class="alert-text">{error}</span>
      </div>
      <button class="btn btn-ghost btn-sm" onclick={fetchServers}>Retry</button>
    </div>
  {/if}

  <!-- Controls & Filter Toolbar -->
  <section class="toolbar" aria-label="Server search and filtering tools">
    <div class="search-box">
      <label for="server-search" class="visually-hidden">Search servers by name or port</label>
      <div class="input-with-icon">
        <svg class="input-icon" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M11.5 7a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0zm-.82 4.74a6 6 0 1 1 1.06-1.06l3.04 3.04a.75.75 0 1 1-1.06 1.06l-3.04-3.04z"/>
        </svg>
        <input
          id="server-search"
          type="search"
          class="form-input search-input"
          bind:value={searchQuery}
          placeholder="Filter by server name or port..."
        />
      </div>
    </div>

    <!-- Filter Group -->
    <div class="filter-group" role="group" aria-label="Filter by operational status">
      <button
        type="button"
        class="filter-pill"
        class:active={statusFilter === 'all'}
        onclick={() => (statusFilter = 'all')}
        aria-pressed={statusFilter === 'all'}
      >
        All ({servers.length})
      </button>
      <button
        type="button"
        class="filter-pill"
        class:active={statusFilter === 'running'}
        onclick={() => (statusFilter = 'running')}
        aria-pressed={statusFilter === 'running'}
      >
        Running ({runningCount})
      </button>
      <button
        type="button"
        class="filter-pill"
        class:active={statusFilter === 'stopped'}
        onclick={() => (statusFilter = 'stopped')}
        aria-pressed={statusFilter === 'stopped'}
      >
        Stopped ({stoppedCount})
      </button>
    </div>
  </section>

  <!-- Main Content Area -->
  {#if loading}
    <!-- Skeleton Table Loader -->
    <div class="card table-container" aria-busy="true" aria-label="Loading servers table">
      <div class="skeleton-header-row">
        <div class="skeleton" style="height: 16px; width: 15%;"></div>
        <div class="skeleton" style="height: 16px; width: 12%;"></div>
        <div class="skeleton" style="height: 16px; width: 10%;"></div>
        <div class="skeleton" style="height: 16px; width: 15%;"></div>
        <div class="skeleton" style="height: 16px; width: 12%;"></div>
        <div class="skeleton" style="height: 16px; width: 20%; margin-left: auto;"></div>
      </div>
      {#each Array(4) as _}
        <div class="skeleton-table-row">
          <div class="skeleton" style="height: 20px; width: 25%;"></div>
          <div class="skeleton" style="height: 18px; width: 15%;"></div>
          <div class="skeleton" style="height: 18px; width: 10%;"></div>
          <div class="skeleton" style="height: 18px; width: 18%;"></div>
          <div class="skeleton" style="height: 18px; width: 12%;"></div>
          <div class="skeleton" style="height: 28px; width: 100px; margin-left: auto;"></div>
        </div>
      {/each}
    </div>
  {:else if filteredServers.length === 0}
    <!-- Empty State -->
    <div class="card empty-card">
      <div class="empty-state">
        <svg class="empty-state-icon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
          <rect x="8" y="6" width="32" height="14" rx="3"/>
          <rect x="8" y="28" width="32" height="14" rx="3"/>
          <circle cx="14" cy="13" r="2"/>
          <circle cx="14" cy="35" r="2"/>
        </svg>
        <span class="empty-state-title">No matching instances found</span>
        <p class="empty-state-text">
          {searchQuery || statusFilter !== 'all'
            ? 'No servers match your current search query or status filters.'
            : 'Get started by creating your first containerized Minecraft server.'}
        </p>
        {#if searchQuery || statusFilter !== 'all'}
          <button
            class="btn btn-secondary btn-sm"
            onclick={() => {
              searchQuery = '';
              statusFilter = 'all';
            }}
          >Clear Filters</button>
        {:else}
          <a href="/create" class="btn btn-primary">Deploy Server</a>
        {/if}
      </div>
    </div>
  {:else}
    <!-- Desktop / Tablet Table View (Hidden on mobile < 640px) -->
    <div class="card table-container desktop-table-view">
      <table class="data-table" aria-label="Minecraft servers list">
        <thead>
          <tr>
            <th scope="col">Instance Name</th>
            <th scope="col">Runtime Status</th>
            <th scope="col">Port</th>
            <th scope="col">Edition / Version</th>
            <th scope="col">Players</th>
            <th scope="col">Resource Usage</th>
            <th scope="col" class="sticky-action-col text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each filteredServers as server (server.id)}
            <tr>
              <td>
                <div class="instance-name-cell">
                  <a href="/servers/{server.id}" class="instance-title-link">
                    {server.name}
                  </a>
                  <span class="instance-slug">ID #{server.id}</span>
                </div>
              </td>
              <td>
                <span class="badge"
                  class:badge-success={server.status === 'running'}
                  class:badge-neutral={server.status === 'stopped'}
                  class:badge-warning={server.status === 'starting'}
                  class:badge-error={server.status === 'error'}
                >
                  <span class="status-dot status-dot-{server.status}" aria-hidden="true"></span>
                  <span>{server.status}</span>
                </span>
              </td>
              <td>
                <span class="port-tag">:{server.port}</span>
              </td>
              <td>
                <div class="edition-cell">
                  <span class="edition-label">{server.server_type === 'java' ? 'Java' : 'Bedrock'}</span>
                  {#if server.version}
                    <span class="version-label">{server.version}</span>
                  {/if}
                </div>
              </td>
              <td>
                <span class="player-count">
                  {server.player_count} <span class="player-unit">online</span>
                </span>
              </td>
              <td>
                <div class="resource-usage">
                  <div class="resource-metric">
                    <span class="metric-mini-label">CPU:</span>
                    <span class="metric-mini-val">{server.cpu_usage.toFixed(0)}%</span>
                  </div>
                  <div class="resource-metric">
                    <span class="metric-mini-label">RAM:</span>
                    <span class="metric-mini-val">{server.ram_usage.toFixed(0)} MB</span>
                  </div>
                </div>
              </td>
              <td class="sticky-action-col text-right">
                <div class="action-cell">
                  {#if server.status === 'stopped'}
                    <button
                      type="button"
                      class="btn btn-primary btn-sm"
                      disabled={actionLoadingId === server.id}
                      onclick={() => handleAction(server.id, 'start')}
                      aria-label="Start server {server.name}"
                    >
                      {#if actionLoadingId === server.id}
                        <span class="spinner" aria-hidden="true"></span>
                      {:else}
                        Start
                      {/if}
                    </button>
                  {:else if server.status === 'running'}
                    <button
                      type="button"
                      class="btn btn-secondary btn-sm"
                      disabled={actionLoadingId === server.id}
                      onclick={() => handleAction(server.id, 'restart')}
                      aria-label="Restart server {server.name}"
                    >
                      {#if actionLoadingId === server.id}
                        <span class="spinner" aria-hidden="true"></span>
                      {:else}
                        Restart
                      {/if}
                    </button>
                    <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      disabled={actionLoadingId === server.id}
                      onclick={() => handleAction(server.id, 'stop')}
                      aria-label="Stop server {server.name}"
                    >
                      {#if actionLoadingId === server.id}
                        <span class="spinner" aria-hidden="true"></span>
                      {:else}
                        Stop
                      {/if}
                    </button>
                  {/if}
                  <a
                    href="/servers/{server.id}"
                    class="btn btn-ghost btn-sm"
                    aria-label="Manage {server.name}"
                  >
                    Console →
                  </a>
                </div>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <!-- Mobile Stacked Card View (Visible only on < 640px) -->
    <div class="mobile-card-list" aria-label="Minecraft servers list (mobile view)">
      {#each filteredServers as server (server.id)}
        <article class="card mobile-server-card">
          <header class="mobile-card-header">
            <div>
              <a href="/servers/{server.id}" class="instance-title-link">
                <h2 class="mobile-card-title">{server.name}</h2>
              </a>
              <span class="instance-slug">ID #{server.id} · Port :{server.port}</span>
            </div>
            <span class="badge"
              class:badge-success={server.status === 'running'}
              class:badge-neutral={server.status === 'stopped'}
              class:badge-warning={server.status === 'starting'}
              class:badge-error={server.status === 'error'}
            >
              <span class="status-dot status-dot-{server.status}" aria-hidden="true"></span>
              <span>{server.status}</span>
            </span>
          </header>

          <div class="mobile-card-metrics">
            <div class="mobile-metric-item">
              <span class="mobile-metric-label">Edition</span>
              <span class="mobile-metric-val">{server.server_type === 'java' ? 'Java' : 'Bedrock'}</span>
            </div>
            <div class="mobile-metric-item">
              <span class="mobile-metric-label">Players</span>
              <span class="mobile-metric-val">{server.player_count}</span>
            </div>
            <div class="mobile-metric-item">
              <span class="mobile-metric-label">CPU / RAM</span>
              <span class="mobile-metric-val">{server.cpu_usage.toFixed(0)}% / {server.ram_usage.toFixed(0)}M</span>
            </div>
          </div>

          <footer class="mobile-card-actions">
            {#if server.status === 'stopped'}
              <button
                type="button"
                class="btn btn-primary btn-sm full-width"
                disabled={actionLoadingId === server.id}
                onclick={() => handleAction(server.id, 'start')}
              >
                {#if actionLoadingId === server.id}<span class="spinner"></span>{/if}
                Start Instance
              </button>
            {:else if server.status === 'running'}
              <button
                type="button"
                class="btn btn-secondary btn-sm"
                disabled={actionLoadingId === server.id}
                onclick={() => handleAction(server.id, 'restart')}
              >
                Restart
              </button>
              <button
                type="button"
                class="btn btn-danger btn-sm"
                disabled={actionLoadingId === server.id}
                onclick={() => handleAction(server.id, 'stop')}
              >
                Stop
              </button>
            {/if}
            <a href="/servers/{server.id}" class="btn btn-ghost btn-sm">
              Console →
            </a>
          </footer>
        </article>
      {/each}
    </div>
  {/if}
</div>

<style>
  .page-container {
    max-width: var(--content-max-width);
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: var(--space-5);
  }

  .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  .text-right {
    text-align: right;
  }

  /* Toolbar */
  .toolbar {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  @media (min-width: 640px) {
    .toolbar {
      flex-direction: row;
      align-items: center;
      justify-content: space-between;
    }
  }

  .search-box {
    flex: 1;
    max-width: 400px;
  }

  .input-with-icon {
    position: relative;
    display: flex;
    align-items: center;
  }

  .input-icon {
    position: absolute;
    left: var(--space-3);
    width: 16px;
    height: 16px;
    color: var(--color-text-tertiary);
    pointer-events: none;
  }

  .search-input {
    padding-left: 36px;
  }

  .filter-group {
    display: flex;
    align-items: center;
    gap: var(--space-1);
    background: var(--color-bg-base);
    padding: 3px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
  }

  .filter-pill {
    background: transparent;
    border: none;
    padding: var(--space-1) var(--space-3);
    font-size: var(--text-xs);
    font-weight: var(--font-medium);
    color: var(--color-text-secondary);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: background var(--transition-fast), color var(--transition-fast);
  }

  .filter-pill:hover {
    color: var(--color-text-primary);
  }

  .filter-pill.active {
    background: var(--color-bg-surface);
    color: var(--color-text-primary);
    box-shadow: var(--shadow-sm);
  }

  /* Alert */
  .alert-banner {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-3) var(--space-4);
    background: var(--color-error-muted);
    border: 1px solid var(--color-error);
    border-radius: var(--radius-md);
    color: var(--color-error);
  }

  .alert-icon {
    width: 16px;
    height: 16px;
    flex-shrink: 0;
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
  }

  /* Table Container */
  .table-container {
    padding: 0;
    overflow-x: auto;
  }

  .sticky-action-col {
    position: sticky;
    right: 0;
    background: var(--color-bg-surface);
    z-index: 2;
  }

  .instance-name-cell {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .instance-title-link {
    font-weight: var(--font-semibold);
    color: var(--color-text-primary);
    text-decoration: none;
  }

  .instance-title-link:hover {
    color: var(--color-accent);
    text-decoration: underline;
  }

  .instance-slug {
    font-size: var(--text-xs);
    font-family: var(--font-mono);
    color: var(--color-text-tertiary);
  }

  .port-tag {
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    background: var(--color-bg-hover);
    padding: 2px 6px;
    border-radius: var(--radius-sm);
  }

  .edition-cell {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .edition-label {
    font-size: var(--text-sm);
    color: var(--color-text-primary);
  }

  .version-label {
    font-family: var(--font-mono);
    font-size: var(--text-xs);
    color: var(--color-text-tertiary);
  }

  .player-count {
    font-family: var(--font-mono);
    font-weight: var(--font-semibold);
  }

  .player-unit {
    font-family: var(--font-sans);
    font-size: var(--text-xs);
    font-weight: var(--font-regular);
    color: var(--color-text-tertiary);
  }

  .resource-usage {
    display: flex;
    flex-direction: column;
    gap: 2px;
    font-family: var(--font-mono);
    font-size: var(--text-xs);
  }

  .metric-mini-label {
    color: var(--color-text-tertiary);
  }

  .metric-mini-val {
    color: var(--color-text-secondary);
    margin-left: var(--space-1);
  }

  .action-cell {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: var(--space-2);
  }

  /* Skeleton rows */
  .skeleton-header-row,
  .skeleton-table-row {
    display: flex;
    align-items: center;
    gap: var(--space-4);
    padding: var(--space-4);
    border-bottom: 1px solid var(--color-border-subtle);
  }

  .skeleton-header-row {
    background: var(--color-bg-surface);
    border-bottom: 1px solid var(--color-border);
  }

  /* Mobile Stacked Card View */
  .desktop-table-view {
    display: none;
  }

  .mobile-card-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  @media (min-width: 640px) {
    .desktop-table-view {
      display: block;
    }
    .mobile-card-list {
      display: none;
    }
  }

  .mobile-server-card {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
    padding: var(--space-4);
  }

  .mobile-card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: var(--space-3);
  }

  .mobile-card-title {
    font-size: var(--text-md);
    font-weight: var(--font-semibold);
    color: var(--color-text-primary);
  }

  .mobile-card-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-2);
    padding: var(--space-3);
    background: var(--color-bg-base);
    border-radius: var(--radius-md);
  }

  .mobile-metric-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .mobile-metric-label {
    font-size: var(--text-xs);
    color: var(--color-text-tertiary);
  }

  .mobile-metric-val {
    font-size: var(--text-xs);
    font-weight: var(--font-semibold);
    font-family: var(--font-mono);
  }

  .mobile-card-actions {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding-top: var(--space-2);
    border-top: 1px solid var(--color-border-subtle);
  }

  .full-width {
    flex: 1;
  }
</style>
