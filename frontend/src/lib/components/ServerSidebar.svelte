<!--
  LokMC — Floating Glassmorphic Server Sidebar
  Strictly implements the design in the user's reference images:
  - Image 1: Expanded state with icons, uppercase labels, and horizontal dividers
  - Image 2: Collapsed / minimalist dock state with centered icons
  - Supports smooth fluid cubic-bezier animation between expanded & collapsed
  - Hover micro-animations, active glass pill indicator, floating tooltips in collapsed mode
-->
<script lang="ts">
  import { onMount } from 'svelte';

  export type ServerTab =
    | 'terminal'
    | 'logs'
    | 'schedule'
    | 'backup'
    | 'name'
    | 'config'
    | 'players'
    | 'metrics'
    | 'webhooks'
    | 'settings';

  let {
    activeTab = 'terminal',
    onTabChange = (tab: ServerTab) => {},
    collapsed = $bindable(false)
  }: {
    activeTab?: ServerTab;
    onTabChange?: (tab: ServerTab) => void;
    collapsed?: boolean;
  } = $props();

  onMount(() => {
    // Check saved sidebar state preference
    const saved = localStorage.getItem('lokmc_sidebar_collapsed');
    if (saved !== null) {
      collapsed = saved === 'true';
    }
  });

  function toggleCollapse() {
    collapsed = !collapsed;
    localStorage.setItem('lokmc_sidebar_collapsed', String(collapsed));
  }

  function handleSelect(tab: ServerTab) {
    onTabChange(tab);
  }

  const menuItems: { id: ServerTab; label: string; icon: string }[] = [
    { id: 'terminal', label: 'TERMINAL', icon: 'terminal' },
    { id: 'logs', label: 'LOGS', icon: 'book' },
    { id: 'schedule', label: 'SCHEDULE', icon: 'clock' },
    { id: 'backup', label: 'BACKUP', icon: 'disk' },
    { id: 'name', label: 'NAME', icon: 'file' },
    { id: 'config', label: 'CONFIG', icon: 'gear' },
    { id: 'players', label: 'PLAYER MANAGEMENT', icon: 'users' },
    { id: 'metrics', label: 'METRICS', icon: 'pulse' },
    { id: 'webhooks', label: 'WEBHOOKS', icon: 'bell' },
    { id: 'settings', label: 'SERVER SETTINGS', icon: 'cog' }
  ];
</script>

<aside
  class="server-glass-sidebar"
  class:collapsed={collapsed}
  aria-label="Server control navigation"
>
  <!-- Collapse / Expand Toggle Handle -->
  <div class="sidebar-toggle-bar">
    <button
      type="button"
      class="sidebar-toggle-btn"
      onclick={toggleCollapse}
      title={collapsed ? 'Expand Sidebar (Image 1)' : 'Collapse to Minimalist Dock (Image 2)'}
      aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
    >
      <svg
        class="toggle-chevron"
        class:flipped={collapsed}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.2"
      >
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
      {#if !collapsed}
        <span class="toggle-text">MINIMIZE</span>
      {/if}
    </button>
  </div>

  <!-- Navigation Items List -->
  <nav class="sidebar-menu-list" role="tablist">
    {#each menuItems as item, index}
      <!-- Horizontal divider line as visible in Image 1 -->
      {#if index > 0}
        <div class="menu-divider-line" class:hidden={collapsed} aria-hidden="true"></div>
      {/if}

      <button
        type="button"
        role="tab"
        aria-selected={activeTab === item.id}
        class="menu-row-btn"
        class:active={activeTab === item.id}
        onclick={() => handleSelect(item.id)}
        aria-label={item.label}
      >
        <!-- Icon Container -->
        <span class="icon-slot" aria-hidden="true">
          {#if item.icon === 'terminal'}
            <!-- >_ icon -->
            <svg class="sidebar-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="4 17 10 11 4 5"></polyline>
              <line x1="12" y1="19" x2="20" y2="19"></line>
            </svg>
          {:else if item.icon === 'book'}
            <!-- Book icon (LOGS) -->
            <svg class="sidebar-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
            </svg>
          {:else if item.icon === 'clock'}
            <!-- Clock icon (SCHEDULE) -->
            <svg class="sidebar-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
          {:else if item.icon === 'disk'}
            <!-- Floppy disk icon (BACKUP) -->
            <svg class="sidebar-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
              <polyline points="17 21 17 13 7 13 7 21"></polyline>
              <polyline points="7 3 7 8 15 8"></polyline>
            </svg>
          {:else if item.icon === 'file'}
            <!-- Document page icon (NAME / FILES) -->
            <svg class="sidebar-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
          {:else if item.icon === 'gear'}
            <!-- Gear icon (CONFIG) -->
            <svg class="sidebar-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
          {:else if item.icon === 'users'}
            <!-- Users icon (PLAYER MANAGEMENT) -->
            <svg class="sidebar-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          {:else if item.icon === 'pulse'}
            <!-- Activity pulse waveform (METRICS) -->
            <svg class="sidebar-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
          {:else if item.icon === 'bell'}
            <!-- Bell icon (WEBHOOKS) -->
            <svg class="sidebar-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
          {:else if item.icon === 'cog'}
            <!-- Cog icon (SERVER SETTINGS) -->
            <svg class="sidebar-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
          {/if}
        </span>

        <!-- Label (visible in Expanded mode, Image 1) -->
        {#if !collapsed}
          <span class="label-slot">{item.label}</span>
        {/if}

        <!-- Floating Glassmorphic Tooltip (visible on hover in Collapsed mode, Image 2) -->
        {#if collapsed}
          <span class="collapsed-tooltip" role="tooltip">
            {item.label}
          </span>
        {/if}
      </button>
    {/each}
  </nav>
</aside>

<style>
  /* ── Floating Sidebar Container ── */
  .server-glass-sidebar {
    width: 236px;
    background: var(--sidebar-glass-bg);
    border: 1px solid var(--header-glass-border);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border-radius: 28px; /* Deep rounded corners matching Image 1 */
    box-shadow: var(--glass-shadow);
    padding: 12px 10px 16px;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    transition: width 0.32s cubic-bezier(0.16, 1, 0.3, 1),
                border-radius 0.32s cubic-bezier(0.16, 1, 0.3, 1),
                padding 0.32s ease,
                background 0.25s ease,
                box-shadow 0.25s ease;
    user-select: none;
    align-self: flex-start;
    position: sticky;
    top: 96px;
    z-index: 50;
  }

  /* ── Collapsed Minimalist Dock (Image 2) ── */
  .server-glass-sidebar.collapsed {
    width: 66px;
    border-radius: 36px; /* High pill radius matching Image 2 */
    padding: 12px 6px 16px;
  }

  /* ── Toggle Bar ── */
  .sidebar-toggle-bar {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 6px 8px 10px;
    border-bottom: 1px solid var(--sidebar-divider);
    margin-bottom: 6px;
    cursor: pointer;
  }

  .server-glass-sidebar.collapsed .sidebar-toggle-bar {
    justify-content: center;
    padding: 6px 0 10px;
  }

  .sidebar-toggle-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    background: none;
    border: none;
    color: var(--color-text-tertiary);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.05em;
    cursor: pointer;
    padding: 6px 10px;
    border-radius: 9999px;
    transition: color 0.2s ease, background 0.2s ease;
    width: 100%;
  }

  .sidebar-toggle-btn:hover {
    color: var(--color-text-primary);
    background: rgba(0, 0, 0, 0.05);
  }

  :global([data-theme='dark']) .sidebar-toggle-btn:hover {
    background: rgba(255, 255, 255, 0.06);
  }

  .toggle-chevron {
    width: 14px;
    height: 14px;
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .toggle-chevron.flipped {
    transform: rotate(180deg);
  }

  /* ── Navigation Menu List ── */
  .sidebar-menu-list {
    display: flex;
    flex-direction: column;
    gap: 0;
  }

  /* Divider line as visible between items in Image 1 */
  .menu-divider-line {
    height: 1px;
    background: var(--sidebar-divider);
    margin: 1px 6px;
    transition: opacity 0.2s ease;
  }

  .menu-divider-line.hidden {
    opacity: 0;
    margin: 2px 0;
  }

  /* ── Menu Row Item ── */
  .menu-row-btn {
    display: flex;
    align-items: center;
    width: 100%;
    background: none;
    border: none;
    padding: 10px 14px;
    border-radius: 16px;
    color: var(--color-text-primary);
    cursor: pointer;
    position: relative;
    text-align: left;
    transition: background 0.2s cubic-bezier(0.16, 1, 0.3, 1),
                color 0.2s ease,
                transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    font-family: inherit;
  }

  .server-glass-sidebar.collapsed .menu-row-btn {
    justify-content: center;
    padding: 11px 0;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    margin: 2px auto;
  }

  /* Hover micro-animation */
  .menu-row-btn:hover {
    background: rgba(0, 0, 0, 0.04);
    transform: translateX(2px);
  }

  :global([data-theme='dark']) .menu-row-btn:hover {
    background: rgba(255, 255, 255, 0.06);
  }

  .server-glass-sidebar.collapsed .menu-row-btn:hover {
    transform: scale(1.1);
  }

  /* Active State (Glass pill highlight with depth) */
  .menu-row-btn.active {
    background: rgba(0, 0, 0, 0.08);
    color: var(--color-text-primary);
    box-shadow: inset 0 1px 2px rgba(255, 255, 255, 0.2), 0 2px 8px rgba(0, 0, 0, 0.04);
  }

  :global([data-theme='dark']) .menu-row-btn.active {
    background: rgba(255, 255, 255, 0.12);
    box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.15), 0 2px 10px rgba(0, 0, 0, 0.2);
  }

  /* Icon Slot */
  .icon-slot {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px;
    height: 26px;
    flex-shrink: 0;
    transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), color 0.2s ease;
    color: currentColor;
  }

  .menu-row-btn:hover .icon-slot {
    transform: scale(1.12);
  }

  .sidebar-svg {
    width: 20px;
    height: 20px;
    stroke: currentColor;
  }

  /* Label Slot (Uppercase, bold, matching Image 1) */
  .label-slot {
    margin-left: 14px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.05em;
    white-space: nowrap;
    text-transform: uppercase;
    color: var(--color-text-primary);
    transition: transform 0.2s ease, opacity 0.2s ease;
  }

  .menu-row-btn:hover .label-slot {
    transform: translateX(1px);
  }

  /* ── Floating Tooltip in Collapsed Mode ── */
  .collapsed-tooltip {
    position: absolute;
    left: calc(100% + 14px);
    top: 50%;
    transform: translateY(-50%) translateX(-6px);
    background: var(--color-bg-elevated);
    color: var(--color-text-primary);
    border: 1px solid var(--header-glass-border);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.05em;
    white-space: nowrap;
    box-shadow: var(--glass-shadow);
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.18s cubic-bezier(0.16, 1, 0.3, 1),
                transform 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    z-index: 200;
  }

  .menu-row-btn:hover .collapsed-tooltip {
    opacity: 1;
    transform: translateY(-50%) translateX(0);
  }

  /* ── Responsive Mobile ── */
  @media (max-width: 900px) {
    .server-glass-sidebar {
      width: 66px;
      border-radius: 36px;
      padding: 12px 6px 16px;
    }

    .label-slot {
      display: none;
    }

    .menu-divider-line {
      display: none;
    }

    .toggle-text {
      display: none;
    }

    .server-glass-sidebar .menu-row-btn {
      justify-content: center;
      padding: 11px 0;
      border-radius: 50%;
      width: 48px;
      height: 48px;
      margin: 2px auto;
    }
  }
</style>
