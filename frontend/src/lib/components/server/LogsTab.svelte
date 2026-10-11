<!--
  LokMC — LogsTab
  Searchable runtime logs, severity level filter, and log downloader.
-->
<script lang="ts">
  let {
    consoleLines = [],
    onDownload = () => {}
  }: {
    consoleLines: string[];
    onDownload: () => void;
  } = $props();

  let searchQuery = $state('');
  let levelFilter = $state<'ALL' | 'INFO' | 'WARN' | 'SEVERE'>('ALL');

  let filteredLines = $derived(
    consoleLines.filter((line) => {
      const matchesSearch = !searchQuery.trim() || line.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesLevel =
        levelFilter === 'ALL' ||
        (levelFilter === 'INFO' && line.includes('INFO')) ||
        (levelFilter === 'WARN' && line.includes('WARN')) ||
        (levelFilter === 'SEVERE' && (line.includes('SEVERE') || line.includes('ERROR')));
      return matchesSearch && matchesLevel;
    })
  );
</script>

<section class="view-card">
  <div class="card-header-flex">
    <div>
      <h2 class="section-heading">Runtime Logs</h2>
      <p class="section-subheading">Structured searchable container logs and stacktraces.</p>
    </div>
    <button class="btn-glass-action" onclick={onDownload}>
      Download latest.log
    </button>
  </div>

  <div class="logs-filter-strip">
    <input
      type="search"
      class="filter-search-input"
      bind:value={searchQuery}
      placeholder="Filter by keyword (e.g. 'error', 'world', 'player')..."
    />
    <div class="filter-pills-group">
      <button
        class="filter-pill"
        class:active={levelFilter === 'ALL'}
        onclick={() => (levelFilter = 'ALL')}
      >ALL</button>
      <button
        class="filter-pill"
        class:active={levelFilter === 'INFO'}
        onclick={() => (levelFilter = 'INFO')}
      >INFO</button>
      <button
        class="filter-pill"
        class:active={levelFilter === 'WARN'}
        onclick={() => (levelFilter = 'WARN')}
      >WARNING</button>
      <button
        class="filter-pill"
        class:active={levelFilter === 'SEVERE'}
        onclick={() => (levelFilter = 'SEVERE')}
      >SEVERE</button>
    </div>
  </div>

  <div class="logs-viewer-box">
    {#each filteredLines as line, i}
      <div class="log-entry">
        <span class="log-line-num">{i + 1}</span>
        <span class="log-content">{line}</span>
      </div>
    {/each}
    {#if filteredLines.length === 0}
      <div class="empty-logs">No logs match the current query.</div>
    {/if}
  </div>
</section>

<style>
  .view-card {
    background: var(--glass-bg);
    border: 1px solid var(--header-glass-border);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border-radius: 28px;
    box-shadow: var(--glass-shadow);
    padding: 24px 28px;
    display: flex;
    flex-direction: column;
    gap: 18px;
    animation: tab-fade 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }

  @keyframes tab-fade {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .card-header-flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
  }

  .section-heading {
    font-size: 19px;
    font-weight: 800;
    color: var(--color-text-primary);
    margin: 0 0 2px 0;
  }

  .section-subheading {
    font-size: 13px;
    color: var(--color-text-secondary);
    margin: 0;
  }

  .btn-glass-action {
    padding: 8px 18px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 700;
    background: rgba(0, 0, 0, 0.05);
    border: 1px solid var(--sidebar-divider);
    color: var(--color-text-primary);
    cursor: pointer;
    transition: background 0.2s ease, transform 0.2s ease;
  }

  .btn-glass-action:hover {
    background: rgba(0, 0, 0, 0.1);
    transform: translateY(-1px);
  }

  .logs-filter-strip {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
  }

  .filter-search-input {
    flex: 1;
    max-width: 380px;
    background: rgba(0, 0, 0, 0.03);
    border: 1px solid var(--sidebar-divider);
    border-radius: 12px;
    padding: 8px 14px;
    font-size: 13px;
    color: var(--color-text-primary);
    outline: none;
  }

  .filter-pills-group {
    display: flex;
    gap: 6px;
  }

  .filter-pill {
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 700;
    background: rgba(0, 0, 0, 0.04);
    border: 1px solid var(--sidebar-divider);
    color: var(--color-text-secondary);
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
  }

  .filter-pill.active {
    background: var(--pill-active-bg);
    color: var(--pill-active-text);
  }

  .logs-viewer-box {
    height: 380px;
    overflow-y: auto;
    background: rgba(0, 0, 0, 0.02);
    border: 1px solid var(--sidebar-divider);
    border-radius: 16px;
    padding: 12px;
    font-family: var(--font-mono);
    font-size: 12px;
    line-height: 1.7;
  }

  .log-entry {
    display: flex;
    gap: 12px;
  }

  .log-line-num {
    color: var(--color-text-tertiary);
    width: 28px;
    text-align: right;
    user-select: none;
  }

  .log-content {
    color: var(--color-text-primary);
    word-break: break-all;
  }

  .empty-logs {
    color: var(--color-text-tertiary);
    font-style: italic;
    padding: 24px;
    text-align: center;
  }
</style>
