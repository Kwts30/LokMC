<!--
  LokMC — ServerHeroCard
  Top quick status bar: Identity, status beacon, 1-click IP copy, power actions, and KPI strip.
-->
<script lang="ts">
  let {
    server = $bindable(),
    actionLoading = null,
    onPowerAction = (action: 'start' | 'stop' | 'restart' | 'kill') => {},
    onCopyAddress = () => {},
    copyFeedback = false
  }: {
    server: any;
    actionLoading?: string | null;
    onPowerAction?: (action: 'start' | 'stop' | 'restart' | 'kill') => void;
    onCopyAddress?: () => void;
    copyFeedback?: boolean;
  } = $props();
</script>

<section class="server-hero-card" aria-label="Server quick controls">
  <div class="hero-top-row">
    <!-- Title & Status Details -->
    <div class="server-identity-group">
      <div class="server-name-row">
        <h1 class="server-title">{server.name}</h1>
        <span
          class="status-capsule status-{server.status}"
          title="Current node container status"
        >
          <span class="pulse-beacon beacon-{server.status}"></span>
          <span class="status-text">{server.status.toUpperCase()}</span>
        </span>
      </div>

      <div class="server-meta-tags">
        <span class="meta-tag">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="2" width="20" height="8" rx="2"></rect>
            <rect x="2" y="14" width="20" height="8" rx="2"></rect>
          </svg>
          {server.version}
        </span>
        <span class="meta-separator">•</span>
        <!-- 1-Click Copy IP Address Pill -->
        <button
          type="button"
          class="ip-pill-btn"
          onclick={onCopyAddress}
          title="Click to copy server connection address"
        >
          <span class="ip-address-text">{server.host}:{server.port}</span>
          <svg class="copy-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            {#if copyFeedback}
              <polyline points="20 6 9 17 4 12"></polyline>
            {:else}
              <rect x="9" y="9" width="13" height="13" rx="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            {/if}
          </svg>
          {#if copyFeedback}
            <span class="copied-tag">Copied!</span>
          {/if}
        </button>
      </div>
    </div>

    <!-- Power Controls (Pill Action Buttons) -->
    <div class="power-controls-cluster">
      {#if server.status !== 'running'}
        <button
          type="button"
          class="power-btn btn-start"
          disabled={actionLoading !== null}
          onclick={() => onPowerAction('start')}
        >
          {#if actionLoading === 'start'}
            <span class="micro-spinner"></span>
          {:else}
            <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
          {/if}
          <span>Start</span>
        </button>
      {/if}

      {#if server.status === 'running'}
        <button
          type="button"
          class="power-btn btn-restart"
          disabled={actionLoading !== null}
          onclick={() => onPowerAction('restart')}
        >
          {#if actionLoading === 'restart'}
            <span class="micro-spinner"></span>
          {:else}
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="23 4 23 10 17 10"></polyline>
              <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
            </svg>
          {/if}
          <span>Restart</span>
        </button>

        <button
          type="button"
          class="power-btn btn-stop"
          disabled={actionLoading !== null}
          onclick={() => onPowerAction('stop')}
        >
          {#if actionLoading === 'stop'}
            <span class="micro-spinner"></span>
          {:else}
            <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
              <rect x="6" y="6" width="12" height="12" rx="2"></rect>
            </svg>
          {/if}
          <span>Stop</span>
        </button>
      {/if}

      <button
        type="button"
        class="power-btn btn-kill"
        title="Force terminate container PID"
        disabled={actionLoading !== null}
        onclick={() => onPowerAction('kill')}
      >
        <span>Kill</span>
      </button>
    </div>
  </div>

  <!-- Quick Telemetry KPI Strip -->
  <div class="kpi-strip-grid">
    <div class="kpi-pill">
      <span class="kpi-label">PLAYERS ONLINE</span>
      <div class="kpi-val-row">
        <span class="kpi-val">{server.player_count}</span>
        <span class="kpi-unit">/ {server.player_max}</span>
      </div>
    </div>

    <div class="kpi-pill">
      <span class="kpi-label">SERVER TICKRATE</span>
      <div class="kpi-val-row">
        <span class="kpi-val tps-good">{server.tps.toFixed(1)}</span>
        <span class="kpi-unit">TPS</span>
      </div>
    </div>

    <div class="kpi-pill">
      <span class="kpi-label">CPU ALLOCATION</span>
      <div class="kpi-val-row">
        <span class="kpi-val">{server.cpu_usage.toFixed(1)}</span>
        <span class="kpi-unit">%</span>
      </div>
    </div>

    <div class="kpi-pill">
      <span class="kpi-label">RAM USAGE</span>
      <div class="kpi-val-row">
        <span class="kpi-val">{(server.ram_usage / 1024).toFixed(1)}</span>
        <span class="kpi-unit">/ {(server.memory_max / 1024).toFixed(0)} GB</span>
      </div>
    </div>

    <div class="kpi-pill">
      <span class="kpi-label">NODE UPTIME</span>
      <div class="kpi-val-row">
        <span class="kpi-val-sm">{server.uptime}</span>
      </div>
    </div>
  </div>
</section>

<style>
  .server-hero-card {
    background: var(--glass-bg);
    border: 1px solid var(--header-glass-border);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border-radius: 28px;
    box-shadow: var(--glass-shadow);
    padding: 24px 28px;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .hero-top-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
  }

  .server-identity-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .server-name-row {
    display: flex;
    align-items: center;
    gap: 14px;
    flex-wrap: wrap;
  }

  .server-title {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--color-text-primary);
    margin: 0;
  }

  .status-capsule {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 4px 14px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.06em;
    background: rgba(0, 0, 0, 0.05);
  }

  :global([data-theme='dark']) .status-capsule {
    background: rgba(255, 255, 255, 0.08);
  }

  .status-capsule.status-running {
    background: rgba(34, 197, 94, 0.12);
    color: #16a34a;
  }
  :global([data-theme='dark']) .status-capsule.status-running {
    color: #4ade80;
  }

  .status-capsule.status-stopped {
    background: rgba(100, 116, 139, 0.12);
    color: var(--color-text-tertiary);
  }

  .pulse-beacon {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }

  .beacon-running {
    background: #22c55e;
    box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.25);
    animation: pulse-beacon 2s infinite ease-in-out;
  }

  .beacon-stopped {
    background: #94a3b8;
  }

  @keyframes pulse-beacon {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.2); opacity: 0.6; }
  }

  .server-meta-tags {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    color: var(--color-text-secondary);
  }

  .meta-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-weight: 500;
  }

  .meta-separator {
    opacity: 0.4;
  }

  .ip-pill-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0, 0, 0, 0.04);
    border: 1px solid var(--sidebar-divider);
    border-radius: 9999px;
    padding: 3px 12px;
    font-size: 12px;
    font-family: var(--font-mono);
    color: var(--color-text-primary);
    cursor: pointer;
    transition: background 0.2s ease, transform 0.2s ease;
  }

  .ip-pill-btn:hover {
    background: rgba(0, 0, 0, 0.08);
    transform: translateY(-1px);
  }

  :global([data-theme='dark']) .ip-pill-btn {
    background: rgba(255, 255, 255, 0.05);
  }
  :global([data-theme='dark']) .ip-pill-btn:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  .copy-icon {
    width: 13px;
    height: 13px;
  }

  .copied-tag {
    font-size: 11px;
    font-weight: 700;
    color: #16a34a;
  }

  .power-controls-cluster {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .power-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 18px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 700;
    border: none;
    cursor: pointer;
    transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease, opacity 0.2s ease;
  }

  .power-btn:hover {
    transform: translateY(-2px);
  }

  .btn-start {
    background: #16a34a;
    color: #ffffff;
    box-shadow: 0 4px 14px rgba(22, 163, 74, 0.35);
  }

  .btn-restart {
    background: #f59e0b;
    color: #ffffff;
    box-shadow: 0 4px 14px rgba(245, 158, 11, 0.35);
  }

  .btn-stop {
    background: #dc2626;
    color: #ffffff;
    box-shadow: 0 4px 14px rgba(220, 38, 38, 0.35);
  }

  .btn-kill {
    background: rgba(0, 0, 0, 0.06);
    color: var(--color-text-secondary);
    border: 1px solid var(--sidebar-divider);
  }

  :global([data-theme='dark']) .btn-kill {
    background: rgba(255, 255, 255, 0.06);
  }

  .micro-spinner {
    width: 14px;
    height: 14px;
    border: 2px solid currentColor;
    border-top-color: transparent;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .kpi-strip-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    padding-top: 18px;
    border-top: 1px solid var(--sidebar-divider);
  }

  .kpi-pill {
    background: rgba(0, 0, 0, 0.02);
    border: 1px solid var(--sidebar-divider);
    border-radius: 18px;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  :global([data-theme='dark']) .kpi-pill {
    background: rgba(255, 255, 255, 0.03);
  }

  .kpi-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: var(--color-text-tertiary);
  }

  .kpi-val-row {
    display: flex;
    align-items: baseline;
    gap: 4px;
  }

  .kpi-val {
    font-size: 20px;
    font-weight: 800;
    color: var(--color-text-primary);
  }

  .kpi-val.tps-good {
    color: #16a34a;
  }

  .kpi-val-sm {
    font-size: 16px;
    font-weight: 700;
    color: var(--color-text-primary);
  }

  .kpi-unit {
    font-size: 12px;
    color: var(--color-text-secondary);
  }

  @media (max-width: 1200px) {
    .kpi-strip-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }

  @media (max-width: 900px) {
    .kpi-strip-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>
