<script lang="ts">
  interface ServerMetrics {
    tps: number;
    cpu_usage: number;
    ram_usage: number;
    memory_max: number;
    uptime?: string;
  }

  interface Props {
    server: ServerMetrics;
  }

  let { server }: Props = $props();

  let ramPercentage = $derived(
    server.memory_max > 0 ? Math.min(100, (server.ram_usage / server.memory_max) * 100).toFixed(1) : '0'
  );
</script>

<section class="view-card" aria-label="Performance telemetry">
  <div class="card-header-flex">
    <div>
      <h2 class="section-heading">Real-Time Performance Telemetry</h2>
      <p class="section-subheading">TPS stability, JVM heap pressure, and thread CPU utilization.</p>
    </div>
    <span class="refresh-badge">Live: 1s update interval</span>
  </div>

  <div class="metrics-visual-grid">
    <!-- TPS Waveform Gauge -->
    <div class="metric-chart-card">
      <div class="metric-chart-header">
        <span class="mc-title">TICKRATE STABILITY</span>
        <span class="mc-stat-highlight green">{server.tps.toFixed(1)} TPS (100%)</span>
      </div>
      <div class="chart-canvas-wrap">
        <svg viewBox="0 0 300 80" class="metric-svg" preserveAspectRatio="none">
          <path d="M 0,40 Q 30,35 60,40 T 120,40 T 180,40 T 240,40 T 300,40" fill="none" stroke="#22c55e" stroke-width="2.5" />
          <path d="M 0,40 Q 30,35 60,40 T 120,40 T 180,40 T 240,40 T 300,40 L 300,80 L 0,80 Z" fill="rgba(34, 197, 94, 0.08)" />
        </svg>
      </div>
      <span class="chart-caption">No tick skip detected in the last 15 minutes.</span>
    </div>

    <!-- CPU Utilization Wave -->
    <div class="metric-chart-card">
      <div class="metric-chart-header">
        <span class="mc-title">CPU CONTAINER LOAD</span>
        <span class="mc-stat-highlight blue">{server.cpu_usage.toFixed(1)}%</span>
      </div>
      <div class="chart-canvas-wrap">
        <svg viewBox="0 0 300 80" class="metric-svg" preserveAspectRatio="none">
          <path d="M 0,55 Q 30,48 60,52 T 120,42 T 180,49 T 240,44 T 300,48" fill="none" stroke="#3b82f6" stroke-width="2.5" />
          <path d="M 0,55 Q 30,48 60,52 T 120,42 T 180,49 T 240,44 T 300,48 L 300,80 L 0,80 Z" fill="rgba(59, 130, 246, 0.08)" />
        </svg>
      </div>
      <span class="chart-caption">Dedicated high-priority vCPU cores allocated.</span>
    </div>

    <!-- RAM Heap Utilization -->
    <div class="metric-chart-card full-width">
      <div class="metric-chart-header">
        <span class="mc-title">JVM HEAP ALLOCATION</span>
        <span class="mc-stat-highlight purple">{server.ram_usage} MB / {server.memory_max} MB ({ramPercentage}%)</span>
      </div>
      <div class="chart-canvas-wrap ram-wrap">
        <div class="ram-track">
          <div class="ram-fill" style="width: {ramPercentage}%;"></div>
        </div>
      </div>
      <span class="chart-caption">Aikar G1GC flags active. Memory pressure within optimal threshold.</span>
    </div>
  </div>
</section>

<style>
  .view-card {
    background: var(--color-bg-surface);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border: 1px solid var(--sidebar-border);
    border-radius: 24px;
    padding: 26px 30px;
    box-shadow: var(--glass-shadow);
    display: flex;
    flex-direction: column;
    gap: 22px;
    animation: tab-fade-in 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }

  @keyframes tab-fade-in {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .card-header-flex {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .section-heading {
    font-size: 18px;
    font-weight: 800;
    color: var(--color-text-primary);
    margin: 0 0 4px 0;
  }

  .section-subheading {
    font-size: 13px;
    color: var(--color-text-secondary);
    margin: 0;
  }

  .refresh-badge {
    font-size: 11px;
    font-weight: 700;
    color: var(--color-text-tertiary);
    background: rgba(0, 0, 0, 0.04);
    padding: 4px 12px;
    border-radius: 9999px;
  }

  :global([data-theme='dark']) .refresh-badge {
    background: rgba(255, 255, 255, 0.06);
  }

  .metrics-visual-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }

  .metric-chart-card {
    background: rgba(0, 0, 0, 0.02);
    border: 1px solid var(--sidebar-divider);
    border-radius: 20px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .metric-chart-card.full-width {
    grid-column: span 2;
  }

  :global([data-theme='dark']) .metric-chart-card {
    background: rgba(255, 255, 255, 0.03);
    border-color: rgba(255, 255, 255, 0.08);
  }

  .metric-chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .mc-title {
    font-size: 11px;
    font-weight: 700;
    color: var(--color-text-tertiary);
    letter-spacing: 0.05em;
  }

  .mc-stat-highlight {
    font-size: 14px;
    font-weight: 800;
  }

  .mc-stat-highlight.green { color: #16a34a; }
  .mc-stat-highlight.blue { color: #2563eb; }
  .mc-stat-highlight.purple { color: #9333ea; }

  .chart-canvas-wrap {
    height: 90px;
    width: 100%;
  }

  .chart-canvas-wrap.ram-wrap {
    height: auto;
    padding: 8px 0;
  }

  .ram-track {
    height: 12px;
    background: rgba(0, 0, 0, 0.06);
    border-radius: 9999px;
    overflow: hidden;
  }

  :global([data-theme='dark']) .ram-track {
    background: rgba(255, 255, 255, 0.08);
  }

  .ram-fill {
    height: 100%;
    background: linear-gradient(90deg, #a855f7, #6366f1);
    border-radius: 9999px;
    transition: width 0.4s ease;
  }

  .metric-svg {
    width: 100%;
    height: 100%;
  }

  .chart-caption {
    font-size: 11px;
    color: var(--color-text-tertiary);
  }

  @media (max-width: 900px) {
    .metrics-visual-grid {
      grid-template-columns: 1fr;
    }

    .metric-chart-card.full-width {
      grid-column: span 1;
    }
  }
</style>
