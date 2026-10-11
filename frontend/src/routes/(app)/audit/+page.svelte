<!--
  LokMC — Security Audit Log & Operational Telemetry
  High-compliance, immutable audit trail interface.
  Strict 8pt spatial grid, semantic markup, and responsive presentation.
-->
<script lang="ts">
  import { api } from '$lib/api';
  import { onMount } from 'svelte';

  let auditEntries: any[] = $state([]);
  let totalEntries = $state(0);
  let loading = $state(true);
  let error = $state('');
  let categoryFilter = $state<'all' | 'AUTH' | 'SERVER' | 'CONFIG' | 'USER_MGMT'>('all');
  let searchQuery = $state('');

  onMount(async () => {
    await fetchLogs();
  });

  async function fetchLogs() {
    loading = true;
    error = '';
    try {
      const res = await api.getAuditLogs(categoryFilter === 'all' ? undefined : categoryFilter);
      auditEntries = res.entries;
      totalEntries = res.total;
    } catch (err: any) {
      error = err.detail || 'Failed to retrieve audit trail.';
    } finally {
      loading = false;
    }
  }

  function setCategory(cat: typeof categoryFilter) {
    categoryFilter = cat;
    fetchLogs();
  }

  function formatTimestamp(isoStr: string): string {
    try {
      const date = new Date(isoStr);
      return date.toLocaleString('en-US', {
        month: 'short',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
      });
    } catch {
      return isoStr;
    }
  }

  let filteredEntries = $derived(
    auditEntries.filter((entry) => {
      if (!searchQuery.trim()) return true;
      const q = searchQuery.toLowerCase();
      return (
        (entry.user && entry.user.toLowerCase().includes(q)) ||
        entry.action.toLowerCase().includes(q) ||
        (entry.detail && entry.detail.toLowerCase().includes(q)) ||
        (entry.ip_address && entry.ip_address.includes(q))
      );
    })
  );
</script>

<svelte:head>
  <title>Security Audit Log — LokMC</title>
  <meta name="description" content="Immutable operational and security audit log trail." />
</svelte:head>

<div class="page-container">
  <!-- Page Header -->
  <header class="page-header">
    <div>
      <h1 class="page-title">Security Audit Log</h1>
      <p class="page-subtitle">
        Append-only chronological record of authentication events, node mutations, and privilege checks.
      </p>
    </div>
    <div class="header-actions">
      <button
        type="button"
        class="btn btn-secondary btn-sm"
        onclick={fetchLogs}
        disabled={loading}
        aria-label="Refresh audit entries"
      >
        <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z"/>
          <path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/>
        </svg>
        <span>Refresh</span>
      </button>
    </div>
  </header>

  <!-- Error Alert -->
  {#if error}
    <div class="alert-banner" role="alert" aria-live="assertive">
      <svg class="alert-icon" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
        <path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1zm-.75 3.75a.75.75 0 0 1 1.5 0v3.5a.75.75 0 0 1-1.5 0v-3.5zM8 11a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>
      </svg>
      <div class="alert-content">
        <span class="alert-title">Query Error</span>
        <span class="alert-text">{error}</span>
      </div>
      <button class="btn btn-ghost btn-sm" onclick={fetchLogs}>Retry</button>
    </div>
  {/if}

  <!-- Filter & Search Toolbar -->
  <section class="toolbar" aria-label="Audit filters">
    <div class="search-box">
      <label for="audit-search" class="visually-hidden">Search audit logs</label>
      <div class="input-with-icon">
        <svg class="input-icon" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M11.5 7a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0zm-.82 4.74a6 6 0 1 1 1.06-1.06l3.04 3.04a.75.75 0 1 1-1.06 1.06l-3.04-3.04z"/>
        </svg>
        <input
          id="audit-search"
          type="search"
          class="form-input search-input"
          bind:value={searchQuery}
          placeholder="Filter by user, action, detail, or IP..."
        />
      </div>
    </div>

    <!-- Category Pill Group -->
    <div class="filter-group" role="group" aria-label="Filter by event category">
      <button
        type="button"
        class="filter-pill"
        class:active={categoryFilter === 'all'}
        onclick={() => setCategory('all')}
        aria-pressed={categoryFilter === 'all'}
      >
        All
      </button>
      <button
        type="button"
        class="filter-pill"
        class:active={categoryFilter === 'AUTH'}
        onclick={() => setCategory('AUTH')}
        aria-pressed={categoryFilter === 'AUTH'}
      >
        Auth
      </button>
      <button
        type="button"
        class="filter-pill"
        class:active={categoryFilter === 'SERVER'}
        onclick={() => setCategory('SERVER')}
        aria-pressed={categoryFilter === 'SERVER'}
      >
        Server
      </button>
      <button
        type="button"
        class="filter-pill"
        class:active={categoryFilter === 'CONFIG'}
        onclick={() => setCategory('CONFIG')}
        aria-pressed={categoryFilter === 'CONFIG'}
      >
        Config
      </button>
      <button
        type="button"
        class="filter-pill"
        class:active={categoryFilter === 'USER_MGMT'}
        onclick={() => setCategory('USER_MGMT')}
        aria-pressed={categoryFilter === 'USER_MGMT'}
      >
        Users
      </button>
    </div>
  </section>

  <!-- Content Presentation -->
  {#if loading}
    <div class="card table-container" aria-busy="true" aria-label="Loading audit table">
      <div class="skeleton-header-row">
        <div class="skeleton" style="height: 16px; width: 15%;"></div>
        <div class="skeleton" style="height: 16px; width: 10%;"></div>
        <div class="skeleton" style="height: 16px; width: 12%;"></div>
        <div class="skeleton" style="height: 16px; width: 12%;"></div>
        <div class="skeleton" style="height: 16px; width: 35%;"></div>
        <div class="skeleton" style="height: 16px; width: 12%; margin-left: auto;"></div>
      </div>
      {#each Array(5) as _}
        <div class="skeleton-table-row">
          <div class="skeleton" style="height: 18px; width: 15%;"></div>
          <div class="skeleton" style="height: 18px; width: 10%;"></div>
          <div class="skeleton" style="height: 18px; width: 12%;"></div>
          <div class="skeleton" style="height: 18px; width: 12%;"></div>
          <div class="skeleton" style="height: 18px; width: 35%;"></div>
          <div class="skeleton" style="height: 18px; width: 12%; margin-left: auto;"></div>
        </div>
      {/each}
    </div>
  {:else if filteredEntries.length === 0}
    <div class="card empty-card">
      <div class="empty-state">
        <svg class="empty-state-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
        </svg>
        <span class="empty-state-title">No audit records found</span>
        <p class="empty-state-text">
          {searchQuery || categoryFilter !== 'all'
            ? 'No entries match your search query or selected category.'
            : 'Operational actions and security events will automatically appear here.'}
        </p>
      </div>
    </div>
  {:else}
    <!-- Desktop Table View -->
    <div class="card table-container desktop-table-view">
      <table class="data-table" aria-label="Security audit records">
        <thead>
          <tr>
            <th scope="col" style="width: 170px;">Timestamp</th>
            <th scope="col" style="width: 110px;">Category</th>
            <th scope="col" style="width: 140px;">Action</th>
            <th scope="col" style="width: 130px;">Principal</th>
            <th scope="col">Event Details</th>
            <th scope="col" style="width: 130px;" class="text-right">Source IP</th>
          </tr>
        </thead>
        <tbody>
          {#each filteredEntries as entry (entry.id)}
            <tr>
              <td>
                <time datetime={entry.created_at} class="mono-text text-secondary">
                  {formatTimestamp(entry.created_at)}
                </time>
              </td>
              <td>
                <span class="badge"
                  class:badge-info={entry.category === 'AUTH'}
                  class:badge-success={entry.category === 'SERVER'}
                  class:badge-warning={entry.category === 'CONFIG'}
                  class:badge-neutral={entry.category === 'USER_MGMT'}
                >
                  {entry.category}
                </span>
              </td>
              <td>
                <span class="action-tag">{entry.action}</span>
              </td>
              <td>
                <span class="principal-text">{entry.user || 'system'}</span>
              </td>
              <td>
                <span class="detail-text">{entry.detail || '—'}</span>
              </td>
              <td class="text-right">
                <span class="mono-text ip-tag">{entry.ip_address || '127.0.0.1'}</span>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <!-- Mobile Stacked Card View -->
    <div class="mobile-card-list" aria-label="Audit records (mobile view)">
      {#each filteredEntries as entry (entry.id)}
        <article class="card mobile-audit-card">
          <header class="mobile-audit-header">
            <span class="badge"
              class:badge-info={entry.category === 'AUTH'}
              class:badge-success={entry.category === 'SERVER'}
              class:badge-warning={entry.category === 'CONFIG'}
              class:badge-neutral={entry.category === 'USER_MGMT'}
            >
              {entry.category} · {entry.action}
            </span>
            <time datetime={entry.created_at} class="mono-text text-xs">
              {formatTimestamp(entry.created_at)}
            </time>
          </header>
          <p class="mobile-audit-detail">{entry.detail || 'No additional detail.'}</p>
          <footer class="mobile-audit-meta">
            <span>By: <strong>{entry.user || 'system'}</strong></span>
            <span class="mono-text">IP: {entry.ip_address || '127.0.0.1'}</span>
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

  .text-secondary {
    color: var(--color-text-secondary);
  }

  .text-xs {
    font-size: var(--text-xs);
  }

  .mono-text {
    font-family: var(--font-mono);
    font-size: var(--text-xs);
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
    max-width: 420px;
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

  /* Table */
  .table-container {
    padding: 0;
    overflow-x: auto;
  }

  .action-tag {
    font-weight: var(--font-medium);
    color: var(--color-text-primary);
  }

  .principal-text {
    font-weight: var(--font-medium);
    color: var(--color-accent-text);
  }

  .detail-text {
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
    max-width: 500px;
    display: block;
    word-break: break-word;
  }

  .ip-tag {
    color: var(--color-text-tertiary);
  }

  /* Skeletons */
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

  /* Mobile Stacked View */
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

  .mobile-audit-card {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
    padding: var(--space-4);
  }

  .mobile-audit-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-2);
  }

  .mobile-audit-detail {
    font-size: var(--text-sm);
    color: var(--color-text-primary);
  }

  .mobile-audit-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: var(--text-xs);
    color: var(--color-text-tertiary);
    border-top: 1px solid var(--color-border-subtle);
    padding-top: var(--space-2);
  }
</style>
