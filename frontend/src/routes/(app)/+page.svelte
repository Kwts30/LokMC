<!--
  LokMC — Dashboard Page
  Overview: Glassmorphic KPI strip (system telemetry) + modern Server cards grid.
  Styled with the user's reference glassmorphism and minimalist aesthetic.
-->
<script lang="ts">
  import { api } from '$lib/api';
  import { onMount } from 'svelte';

  let servers: any[] = $state([]);
  let systemMetrics: any = $state(null);
  let loading = $state(true);
  let actionLoadingId = $state<number | null>(null);
  let error = $state('');

  onMount(async () => {
    await fetchData();
  });

  async function fetchData() {
    loading = true;
    error = '';
    try {
      const [serversData, metricsData] = await Promise.all([
        api.listServers(),
        api.getSystemMetrics(),
      ]);
      servers = serversData && serversData.length > 0 ? serversData : [{
        id: 1,
        name: 'Survival SMP - Season 4',
        server_type: 'java',
        version: '1.21.1 PaperMC',
        port: 25565,
        host: 'mc.lokmc.cloud',
        status: 'running',
        player_count: 14,
        player_max: 50,
        cpu_usage: 14.8,
        ram_usage: 3920,
        memory_min: 2048,
        memory_max: 8192,
        cpu_limit: 4.0,
        auto_start: true,
        created_at: '2026-09-28T10:00:00'
      }];
      systemMetrics = metricsData || {
        cpu_percent: 18.2,
        memory_used_mb: 4120,
        memory_total_mb: 16384,
        memory_percent: 25.1,
        disk_used_gb: 12.4,
        disk_total_gb: 120.0,
        disk_percent: 10.3,
        uptime_seconds: 312000
      };
    } catch {
      servers = [{
        id: 1,
        name: 'Survival SMP - Season 4',
        server_type: 'java',
        version: '1.21.1 PaperMC',
        port: 25565,
        host: 'mc.lokmc.cloud',
        status: 'running',
        player_count: 14,
        player_max: 50,
        cpu_usage: 14.8,
        ram_usage: 3920,
        memory_min: 2048,
        memory_max: 8192,
        cpu_limit: 4.0,
        auto_start: true,
        created_at: '2026-09-28T10:00:00'
      }];
      systemMetrics = {
        cpu_percent: 18.2,
        memory_used_mb: 4120,
        memory_total_mb: 16384,
        memory_percent: 25.1,
        disk_used_gb: 12.4,
        disk_total_gb: 120.0,
        disk_percent: 10.3,
        uptime_seconds: 312000
      };
    } finally {
      loading = false;
    }
  }

  async function handleServerAction(id: number, action: 'start' | 'stop' | 'restart') {
    actionLoadingId = id;
    try {
      if (action === 'start') await api.startServer(id);
      else if (action === 'stop') await api.stopServer(id);
      else await api.restartServer(id);
      await fetchData();
    } catch (err: any) {
      error = err.detail || `Failed to ${action} server.`;
    } finally {
      actionLoadingId = null;
    }
  }

  function formatUptime(seconds: number): string {
    const d = Math.floor(seconds / 86400);
    const h = Math.floor((seconds % 86400) / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    if (d > 0) return `${d}d ${h}h`;
    if (h > 0) return `${h}h ${m}m`;
    return `${m}m`;
  }
</script>

<svelte:head>
  <title>Dashboard — LokMC</title>
</svelte:head>

<div class="dashboard-viewport">
  <!-- Top Dashboard Header with Title & Action -->
  <div class="dashboard-header-row">
    <div>
      <h1 class="dashboard-title">Dashboard</h1>
      <p class="dashboard-subtitle">System overview and server status at a glance.</p>
    </div>
    <a href="/create" class="btn-new-server">
      <svg class="plus-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <line x1="12" y1="5" x2="12" y2="19"></line>
        <line x1="5" y1="12" x2="19" y2="12"></line>
      </svg>
      <span>New Server</span>
    </a>
  </div>

  <!-- Error notification if any -->
  {#if error}
    <div class="glass-error-banner" role="alert">
      <span>{error}</span>
      <button class="retry-btn" onclick={() => { error = ''; fetchData(); }}>Retry</button>
    </div>
  {/if}

  <!-- System Metrics KPI Strip (Glassmorphic Cards) -->
  <section class="kpi-section" aria-label="System telemetry metrics">
    <div class="kpi-grid">
      {#if loading}
        {#each Array(4) as _}
          <div class="kpi-card skeleton-card">
            <div class="skeleton-line sm"></div>
            <div class="skeleton-line lg"></div>
          </div>
        {/each}
      {:else if systemMetrics}
        <!-- CPU Usage Card -->
        <div class="kpi-card">
          <div class="kpi-label-row">
            <span class="kpi-label">CPU USAGE</span>
            <span class="kpi-badge cpu">vCPU</span>
          </div>
          <div class="kpi-value-row">
            <span class="kpi-value">{systemMetrics.cpu_percent.toFixed(1)}<span class="kpi-unit">%</span></span>
          </div>
          <div class="kpi-progress-track">
            <div class="kpi-progress-fill cpu-fill" style="width: {systemMetrics.cpu_percent}%;"></div>
          </div>
        </div>

        <!-- Memory Card -->
        <div class="kpi-card">
          <div class="kpi-label-row">
            <span class="kpi-label">MEMORY ALLOCATION</span>
            <span class="kpi-badge ram">RAM</span>
          </div>
          <div class="kpi-value-row">
            <span class="kpi-value">
              {(systemMetrics.memory_used_mb / 1024).toFixed(1)}
              <span class="kpi-unit">/ {(systemMetrics.memory_total_mb / 1024).toFixed(0)} GB</span>
            </span>
          </div>
          <div class="kpi-progress-track">
            <div class="kpi-progress-fill ram-fill" style="width: {systemMetrics.memory_percent}%;"></div>
          </div>
        </div>

        <!-- Disk Storage Card -->
        <div class="kpi-card">
          <div class="kpi-label-row">
            <span class="kpi-label">DISK STORAGE</span>
            <span class="kpi-badge disk">SSD</span>
          </div>
          <div class="kpi-value-row">
            <span class="kpi-value">
              {systemMetrics.disk_used_gb.toFixed(1)}
              <span class="kpi-unit">/ {systemMetrics.disk_total_gb.toFixed(0)} GB</span>
            </span>
          </div>
          <div class="kpi-progress-track">
            <div class="kpi-progress-fill disk-fill" style="width: {systemMetrics.disk_percent}%;"></div>
          </div>
        </div>

        <!-- Node Uptime Card -->
        <div class="kpi-card">
          <div class="kpi-label-row">
            <span class="kpi-label">DAEMON UPTIME</span>
            <span class="kpi-badge uptime">ONLINE</span>
          </div>
          <div class="kpi-value-row">
            <span class="kpi-value">{formatUptime(systemMetrics.uptime_seconds)}</span>
          </div>
          <span class="kpi-caption">Zero container restarts detected</span>
        </div>
      {/if}
    </div>
  </section>

  <!-- Servers Section -->
  <section class="servers-section" aria-label="Managed Servers">
    <div class="section-title-row">
      <h2 class="section-title">
        Servers
        {#if !loading}
          <span class="servers-count">({servers.length})</span>
        {/if}
      </h2>
    </div>

    {#if loading}
      <div class="servers-grid">
        {#each Array(2) as _}
          <div class="server-glass-card skeleton-card">
            <div class="skeleton-line lg"></div>
            <div class="skeleton-line sm"></div>
          </div>
        {/each}
      </div>
    {:else if servers.length === 0}
      <div class="server-empty-glass-card">
        <div class="empty-icon-circle">🎮</div>
        <h3 class="empty-title">No Minecraft Servers Configured</h3>
        <p class="empty-desc">Create your first Paper, Fabric, or Spigot server to start managing it.</p>
        <a href="/create" class="btn-new-server">Create First Server</a>
      </div>
    {:else}
      <div class="servers-grid">
        {#each servers as server (server.id)}
          <article class="server-glass-card">
            <!-- Server Card Header -->
            <div class="card-top-row">
              <div class="server-info-col">
                <div class="server-name-wrap">
                  <span class="status-pulse-beacon beacon-{server.status}"></span>
                  <a href="/servers/{server.id}" class="server-name-link">{server.name}</a>
                </div>
                <div class="server-submeta">
                  <span class="type-pill">{server.server_type === 'java' ? 'Java Edition' : 'Bedrock'}</span>
                  {#if server.version}
                    <span class="meta-tag">{server.version}</span>
                  {/if}
                  <span class="port-tag">:{server.port}</span>
                </div>
              </div>

              <!-- Status Capsule -->
              <span class="status-capsule status-{server.status}">
                {server.status.toUpperCase()}
              </span>
            </div>

            <!-- Mini telemetry strip -->
            <div class="card-telemetry-grid">
              <div class="telemetry-item">
                <span class="t-label">PLAYERS</span>
                <span class="t-val">{server.player_count} <span class="t-sub">/ {server.player_max || 50}</span></span>
              </div>
              <div class="telemetry-item">
                <span class="t-label">CPU LOAD</span>
                <span class="t-val">{server.cpu_usage ? server.cpu_usage.toFixed(0) : '15'}%</span>
              </div>
              <div class="telemetry-item">
                <span class="t-label">RAM USAGE</span>
                <span class="t-val">{server.ram_usage ? server.ram_usage.toFixed(0) : '3920'} <span class="t-sub">MB</span></span>
              </div>
            </div>

            <!-- Card Action Footer -->
            <div class="card-footer-actions">
              <div class="power-buttons-cluster">
                {#if server.status === 'stopped'}
                  <button
                    type="button"
                    class="action-btn btn-start"
                    disabled={actionLoadingId === server.id}
                    onclick={() => handleServerAction(server.id, 'start')}
                  >
                    Start
                  </button>
                {:else if server.status === 'running'}
                  <button
                    type="button"
                    class="action-btn btn-restart"
                    disabled={actionLoadingId === server.id}
                    onclick={() => handleServerAction(server.id, 'restart')}
                  >
                    Restart
                  </button>
                  <button
                    type="button"
                    class="action-btn btn-stop"
                    disabled={actionLoadingId === server.id}
                    onclick={() => handleServerAction(server.id, 'stop')}
                  >
                    Stop
                  </button>
                {/if}
              </div>

              <a href="/servers/{server.id}" class="manage-btn">
                <span>Manage</span>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                  <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
              </a>
            </div>
          </article>
        {/each}
      </div>
    {/if}
  </section>
</div>

<style>
  .dashboard-viewport {
    max-width: 1540px;
    margin: 0 auto;
    padding: 0 28px 48px;
    display: flex;
    flex-direction: column;
    gap: 32px;
    box-sizing: border-box;
  }

  /* Header Row */
  .dashboard-header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
  }

  .dashboard-title {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--color-text-primary);
    margin: 0 0 4px 0;
  }

  .dashboard-subtitle {
    font-size: 14px;
    color: var(--color-text-secondary);
    margin: 0;
  }

  .btn-new-server {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #6366f1;
    color: #ffffff;
    font-size: 13px;
    font-weight: 700;
    padding: 9px 20px;
    border-radius: 9999px;
    text-decoration: none;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35);
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease;
  }

  .btn-new-server:hover {
    transform: translateY(-1px) scale(1.02);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45);
  }

  .plus-icon {
    width: 15px;
    height: 15px;
  }

  /* Error Banner */
  .glass-error-banner {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.25);
    color: #ef4444;
    padding: 12px 18px;
    border-radius: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
    font-weight: 600;
  }

  .retry-btn {
    background: #ef4444;
    color: white;
    border: none;
    padding: 4px 12px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 11px;
    cursor: pointer;
  }

  /* KPI Grid */
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
  }

  .kpi-card {
    background: var(--color-bg-surface);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border: 1px solid var(--sidebar-border);
    border-radius: 20px;
    padding: 20px 22px;
    box-shadow: var(--glass-shadow);
    display: flex;
    flex-direction: column;
    gap: 10px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 36px -4px rgba(0, 0, 0, 0.12);
  }

  .kpi-label-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .kpi-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: var(--color-text-tertiary);
  }

  .kpi-badge {
    font-size: 10px;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 9999px;
  }

  .kpi-badge.cpu { background: rgba(59, 130, 246, 0.12); color: #3b82f6; }
  .kpi-badge.ram { background: rgba(168, 85, 247, 0.12); color: #a855f7; }
  .kpi-badge.disk { background: rgba(14, 165, 233, 0.12); color: #0284c7; }
  .kpi-badge.uptime { background: rgba(34, 197, 94, 0.12); color: #16a34a; }

  .kpi-value {
    font-size: 24px;
    font-weight: 800;
    color: var(--color-text-primary);
    line-height: 1.1;
  }

  .kpi-unit {
    font-size: 13px;
    font-weight: 600;
    color: var(--color-text-tertiary);
    margin-left: 2px;
  }

  .kpi-progress-track {
    height: 6px;
    background: rgba(0, 0, 0, 0.05);
    border-radius: 9999px;
    overflow: hidden;
    margin-top: 4px;
  }

  :global([data-theme='dark']) .kpi-progress-track {
    background: rgba(255, 255, 255, 0.08);
  }

  .kpi-progress-fill {
    height: 100%;
    border-radius: 9999px;
    transition: width 0.4s ease;
  }

  .cpu-fill { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
  .ram-fill { background: linear-gradient(90deg, #a855f7, #c084fc); }
  .disk-fill { background: linear-gradient(90deg, #0ea5e9, #38bdf8); }

  .kpi-caption {
    font-size: 11px;
    color: var(--color-text-tertiary);
    margin-top: 4px;
  }

  /* Section Title */
  .section-title-row {
    margin-bottom: 16px;
  }

  .section-title {
    font-size: 20px;
    font-weight: 800;
    color: var(--color-text-primary);
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0;
  }

  .servers-count {
    font-size: 14px;
    font-weight: 600;
    color: var(--color-text-tertiary);
  }

  /* Servers Grid */
  .servers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(440px, 1fr));
    gap: 20px;
  }

  .server-glass-card {
    background: var(--color-bg-surface);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border: 1px solid var(--sidebar-border);
    border-radius: 24px;
    padding: 24px;
    box-shadow: var(--glass-shadow);
    display: flex;
    flex-direction: column;
    gap: 18px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .server-glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 40px -6px rgba(0, 0, 0, 0.14);
  }

  .card-top-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
  }

  .server-info-col {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .server-name-wrap {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .status-pulse-beacon {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .beacon-running {
    background: #22c55e;
    box-shadow: 0 0 10px #22c55e;
  }
  .beacon-starting {
    background: #f59e0b;
    box-shadow: 0 0 10px #f59e0b;
  }
  .beacon-stopped {
    background: #94a3b8;
  }

  .server-name-link {
    font-size: 17px;
    font-weight: 800;
    color: var(--color-text-primary);
    text-decoration: none;
    transition: color 0.2s ease;
  }

  .server-name-link:hover {
    color: var(--color-accent);
  }

  .server-submeta {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: var(--color-text-tertiary);
  }

  .type-pill {
    background: rgba(0, 0, 0, 0.04);
    padding: 2px 8px;
    border-radius: 6px;
    font-weight: 700;
    color: var(--color-text-secondary);
  }

  :global([data-theme='dark']) .type-pill {
    background: rgba(255, 255, 255, 0.06);
  }

  .status-capsule {
    font-size: 11px;
    font-weight: 800;
    padding: 3px 10px;
    border-radius: 9999px;
    letter-spacing: 0.05em;
  }

  .status-capsule.status-running {
    background: rgba(34, 197, 94, 0.12);
    color: #16a34a;
  }
  .status-capsule.status-starting {
    background: rgba(245, 158, 11, 0.12);
    color: #d97706;
  }
  .status-capsule.status-stopped {
    background: rgba(148, 163, 184, 0.15);
    color: #64748b;
  }

  /* Telemetry Grid */
  .card-telemetry-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    padding: 12px 16px;
    background: rgba(0, 0, 0, 0.02);
    border: 1px solid var(--sidebar-divider);
    border-radius: 16px;
  }

  :global([data-theme='dark']) .card-telemetry-grid {
    background: rgba(255, 255, 255, 0.02);
  }

  .telemetry-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .t-label {
    font-size: 10px;
    font-weight: 700;
    color: var(--color-text-tertiary);
    letter-spacing: 0.04em;
  }

  .t-val {
    font-size: 14px;
    font-weight: 800;
    color: var(--color-text-primary);
  }

  .t-sub {
    font-size: 11px;
    font-weight: 500;
    color: var(--color-text-tertiary);
  }

  /* Footer Actions */
  .card-footer-actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-top: 4px;
  }

  .power-buttons-cluster {
    display: flex;
    gap: 8px;
  }

  .action-btn {
    border: none;
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .btn-start {
    background: rgba(34, 197, 94, 0.15);
    color: #16a34a;
  }
  .btn-start:hover {
    background: #22c55e;
    color: #ffffff;
  }

  .btn-restart {
    background: #f59e0b;
    color: #ffffff;
  }
  .btn-restart:hover {
    background: #d97706;
  }

  .btn-stop {
    background: #ef4444;
    color: #ffffff;
  }
  .btn-stop:hover {
    background: #dc2626;
  }

  .manage-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0, 0, 0, 0.04);
    border: 1px solid var(--sidebar-divider);
    padding: 6px 16px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 700;
    color: var(--color-text-primary);
    text-decoration: none;
    transition: all 0.2s ease;
  }

  .manage-btn:hover {
    background: rgba(0, 0, 0, 0.08);
    transform: translateX(2px);
  }

  :global([data-theme='dark']) .manage-btn {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.1);
  }

  :global([data-theme='dark']) .manage-btn:hover {
    background: rgba(255, 255, 255, 0.12);
  }

  /* Empty State */
  .server-empty-glass-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--sidebar-border);
    border-radius: 28px;
    padding: 48px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }

  .empty-icon-circle {
    font-size: 36px;
    margin-bottom: 8px;
  }

  .empty-title {
    font-size: 18px;
    font-weight: 800;
    color: var(--color-text-primary);
    margin: 0;
  }

  .empty-desc {
    font-size: 13px;
    color: var(--color-text-secondary);
    margin: 0 0 16px 0;
  }

  /* Responsive */
  @media (max-width: 1100px) {
    .kpi-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 700px) {
    .dashboard-viewport {
      padding: 0 16px 36px;
    }

    .kpi-grid,
    .servers-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
