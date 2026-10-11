<!--
  LokMC — Default Floating Glassmorphic Header
  Strictly reflects the design in the user's reference image:
  - Floating rounded pill bar with frosted glassmorphism & soft shadow
  - Left: Moon/Sun theme toggle with fluid rotation
  - Left-Center: SUPPORT, ACTIVITY, HOME
  - Center: 3D Isometric Cube Logo with >_ + LokMC + "Server Admin Remote System"
  - Right-Center: SERVERS (active dark pill badge), DOCUMENTATION
  - Right: Bell (Notification center), User profile silhouette
-->
<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { api } from '$lib/api';

  let isDark = $state(false);
  let showNotifications = $state(false);
  let showUserMenu = $state(false);
  let showSupportModal = $state(false);
  let showDocsModal = $state(false);
  let mobileMenuOpen = $state(false);
  let userProfile: any = $state(null);

  // Notifications sample state
  let notifications = $state([
    { id: 1, title: 'Server Backup Complete', time: '5m ago', type: 'success', text: 'Daily snapshot of Survival SMP saved to local storage.' },
    { id: 2, title: 'Player Steve Joined', time: '18m ago', type: 'info', text: 'Connected from 192.168.1.102 (TPS: 20.0)' },
    { id: 3, title: 'Memory Optimized', time: '1h ago', type: 'info', text: 'JVM garbage collection freed 420 MB RAM.' }
  ]);
  let unreadCount = $derived(notifications.length);

  onMount(() => {
    // Check saved theme or system preference.
    // Default to 'light' to match the user's screenshot aesthetic
    const savedTheme = localStorage.getItem('lokmc_theme');
    if (savedTheme === 'dark') {
      isDark = true;
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      isDark = false;
      document.documentElement.setAttribute('data-theme', 'light');
    }

    // Load user profile if authenticated
    if (api.isAuthenticated) {
      api.getProfile().then(p => userProfile = p).catch(() => {});
    }
  });

  function toggleTheme() {
    isDark = !isDark;
    const themeName = isDark ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', themeName);
    localStorage.setItem('lokmc_theme', themeName);
  }

  function toggleNotifications(e: MouseEvent) {
    e.stopPropagation();
    showNotifications = !showNotifications;
    showUserMenu = false;
  }

  function toggleUserMenu(e: MouseEvent) {
    e.stopPropagation();
    showUserMenu = !showUserMenu;
    showNotifications = false;
  }

  function closeDropdowns() {
    showNotifications = false;
    showUserMenu = false;
    mobileMenuOpen = false;
  }

  async function handleLogout() {
    await api.logout();
    goto('/login');
  }

  function clearNotifications() {
    notifications = [];
  }

  let activeNav = $derived.by(() => {
    if (showSupportModal) return 'support';
    if (showDocsModal) return 'docs';
    const path = $page.url.pathname;
    if (path === '/') return 'home';
    if (path.startsWith('/servers') || path.startsWith('/create')) return 'servers';
    if (path.startsWith('/audit') || path.startsWith('/activity')) return 'activity';
    if (path.startsWith('/support')) return 'support';
    if (path.startsWith('/docs')) return 'docs';
    return 'home';
  });
</script>

<svelte:window onclick={closeDropdowns} />

<!-- Floating Pill Header -->
<header class="lokmc-floating-header" aria-label="Main Navigation">
  <div class="header-inner">
    <!-- Left Section: Theme Toggle & Nav Links -->
    <div class="header-left">
      <!-- Dark/Light Theme Toggle (Moon/Sun) -->
      <button
        class="theme-toggle-btn"
        onclick={toggleTheme}
        title={isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        aria-label="Toggle visual theme"
      >
        {#if isDark}
          <!-- Sun Icon for switching to light -->
          <svg class="theme-icon sun-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
          </svg>
        {:else}
          <!-- Crescent Moon Icon matching screenshot -->
          <svg class="theme-icon moon-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
        {/if}
      </button>

      <!-- Primary Left Navigation Links -->
      <nav class="nav-links nav-links-left" aria-label="Support and Activity">
        <button
          type="button"
          class="nav-link-btn"
          class:active-pill={activeNav === 'support'}
          onclick={() => (showSupportModal = true)}
        >
          SUPPORT
        </button>
        <a
          href="/audit"
          class="nav-link-btn"
          class:active-pill={activeNav === 'activity'}
          aria-current={activeNav === 'activity' ? 'page' : undefined}
        >
          ACTIVITY
        </a>
        <a
          href="/"
          class="nav-link-btn"
          class:active-pill={activeNav === 'home'}
          aria-current={activeNav === 'home' ? 'page' : undefined}
        >
          HOME
        </a>
      </nav>
    </div>

    <!-- Center Section: 3D Isometric Cube Brand Logo -->
    <a href="/" class="header-brand" aria-label="LokMC Home">
      <div class="brand-cube-container">
        <!-- 3D Isometric Cube with Terminal Prompt >_ -->
        <svg class="brand-cube-svg" viewBox="0 0 40 40" fill="none">
          <!-- Top isometric face -->
          <polygon points="20,4 36,13 20,22 4,13" class="cube-face cube-face-top" />
          <!-- Left isometric face with terminal prompt -->
          <polygon points="4,13 20,22 20,38 4,29" class="cube-face cube-face-left" />
          <!-- Right isometric face -->
          <polygon points="20,22 36,13 36,29 20,38" class="cube-face cube-face-right" />
          <!-- Terminal Prompt >_ on the front-left face -->
          <path d="M8 20 L12 23 L8 26" stroke="#4ade80" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
          <line x1="13" y1="26" x2="17" y2="26" stroke="#4ade80" stroke-width="1.8" stroke-linecap="round" />
        </svg>
      </div>
      <div class="brand-text-block">
        <span class="brand-title">LokMC</span>
        <span class="brand-subtitle">Server Admin Remote System</span>
      </div>
    </a>

    <!-- Right Section: SERVERS pill, DOCS, Bell, Profile -->
    <div class="header-right">
      <nav class="nav-links nav-links-right" aria-label="Servers and Documentation">
        <a
          href="/servers"
          class="nav-link-btn"
          class:active-pill={activeNav === 'servers'}
          aria-current={activeNav === 'servers' ? 'page' : undefined}
        >
          SERVERS
        </a>
        <button
          type="button"
          class="nav-link-btn"
          class:active-pill={activeNav === 'docs'}
          onclick={() => (showDocsModal = true)}
        >
          DOCUMENTATION
        </button>
      </nav>

      <!-- Utility Icons -->
      <div class="header-actions">
        <!-- Notification Bell -->
        <div class="action-dropdown-wrapper">
          <button
            type="button"
            class="action-icon-btn bell-btn"
            class:has-unread={unreadCount > 0}
            onclick={toggleNotifications}
            aria-label="View notifications"
            aria-expanded={showNotifications}
          >
            <svg class="action-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
            {#if unreadCount > 0}
              <span class="unread-badge">{unreadCount}</span>
            {/if}
          </button>

          <!-- Notifications Glass Dropdown -->
          {#if showNotifications}
            <div
              class="glass-dropdown notifications-panel"
              role="dialog"
              aria-label="Notifications"
              onclick={(e) => e.stopPropagation()}
            >
              <div class="dropdown-header">
                <span class="dropdown-title">System Alerts</span>
                {#if notifications.length > 0}
                  <button class="clear-btn" onclick={clearNotifications}>Clear all</button>
                {/if}
              </div>
              <div class="notifications-list">
                {#if notifications.length === 0}
                  <div class="empty-notif">
                    <span>No unread notifications</span>
                  </div>
                {:else}
                  {#each notifications as item}
                    <div class="notif-item">
                      <div class="notif-indicator {item.type}"></div>
                      <div class="notif-content">
                        <div class="notif-title-row">
                          <span class="notif-title">{item.title}</span>
                          <span class="notif-time">{item.time}</span>
                        </div>
                        <p class="notif-text">{item.text}</p>
                      </div>
                    </div>
                  {/each}
                {/if}
              </div>
            </div>
          {/if}
        </div>

        <!-- User Profile Avatar -->
        <div class="action-dropdown-wrapper">
          <button
            type="button"
            class="action-icon-btn profile-btn"
            onclick={toggleUserMenu}
            aria-label="Open user profile menu"
            aria-expanded={showUserMenu}
          >
            <svg class="action-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </button>

          <!-- Profile Glass Dropdown -->
          {#if showUserMenu}
            <div
              class="glass-dropdown profile-panel"
              role="menu"
              onclick={(e) => e.stopPropagation()}
            >
              <div class="user-meta-block">
                <div class="user-avatar-mini">
                  {userProfile?.username ? userProfile.username[0].toUpperCase() : 'A'}
                </div>
                <div class="user-text-info">
                  <span class="username-display">{userProfile?.username ?? 'Sysadmin'}</span>
                  <span class="user-badge-role">
                    {userProfile?.is_superuser ? 'Super Administrator' : 'Operator'}
                  </span>
                </div>
              </div>
              <div class="menu-divider"></div>
              <a href="/settings" class="menu-link-item" onclick={closeDropdowns}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="3"></circle>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                </svg>
                System Settings
              </a>
              <a href="/create" class="menu-link-item" onclick={closeDropdowns}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                Deploy New Node
              </a>
              <div class="menu-divider"></div>
              <button class="menu-link-item logout-link" onclick={handleLogout}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16 17 21 12 16 7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                Sign Out
              </button>
            </div>
          {/if}
        </div>

        <!-- Mobile Menu Toggle Button -->
        <button
          type="button"
          class="mobile-menu-btn"
          onclick={() => (mobileMenuOpen = !mobileMenuOpen)}
          aria-label="Toggle mobile menu"
          aria-expanded={mobileMenuOpen}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            {#if mobileMenuOpen}
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            {:else}
              <line x1="3" y1="12" x2="21" y2="12"></line>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <line x1="3" y1="18" x2="21" y2="18"></line>
            {/if}
          </svg>
        </button>
      </div>
    </div>
  </div>

  <!-- Mobile Drawer Dropdown -->
  {#if mobileMenuOpen}
    <div class="mobile-drawer" onclick={(e) => e.stopPropagation()}>
      <nav class="mobile-nav-links">
        <a href="/" class="mobile-nav-link" onclick={() => (mobileMenuOpen = false)}>HOME</a>
        <a href="/servers" class="mobile-nav-link" onclick={() => (mobileMenuOpen = false)}>SERVERS</a>
        <a href="/audit" class="mobile-nav-link" onclick={() => (mobileMenuOpen = false)}>ACTIVITY</a>
        <button class="mobile-nav-link" onclick={() => { showSupportModal = true; mobileMenuOpen = false; }}>SUPPORT</button>
        <button class="mobile-nav-link" onclick={() => { showDocsModal = true; mobileMenuOpen = false; }}>DOCUMENTATION</button>
      </nav>
    </div>
  {/if}
</header>

<!-- Support Glass Modal -->
{#if showSupportModal}
  <div class="modal-backdrop" onclick={() => (showSupportModal = false)}>
    <div class="modal-card" onclick={(e) => e.stopPropagation()}>
      <div class="modal-header">
        <h3 class="modal-title">LokMC Technical Support</h3>
        <button class="modal-close-btn" onclick={() => (showSupportModal = false)}>✕</button>
      </div>
      <div class="modal-body">
        <p class="modal-desc">
          Get real-time assistance and operational telemetry support for your Minecraft cluster.
        </p>
        <div class="support-cards-grid">
          <div class="support-card">
            <span class="support-icon">📖</span>
            <h4>Knowledge Base</h4>
            <p>Read step-by-step troubleshooting, JVM tuning, and port forwarding guides.</p>
          </div>
          <div class="support-card">
            <span class="support-icon">💬</span>
            <h4>Discord Community</h4>
            <p>Connect with network admins and the LokMC development community.</p>
          </div>
          <div class="support-card">
            <span class="support-icon">🛡️</span>
            <h4>Security Advisories</h4>
            <p>Zero-trust rootless runtime patches and CVE mitigation releases.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
{/if}

<!-- Documentation Glass Modal -->
{#if showDocsModal}
  <div class="modal-backdrop" onclick={() => (showDocsModal = false)}>
    <div class="modal-card" onclick={(e) => e.stopPropagation()}>
      <div class="modal-header">
        <h3 class="modal-title">Documentation & Architecture</h3>
        <button class="modal-close-btn" onclick={() => (showDocsModal = false)}>✕</button>
      </div>
      <div class="modal-body">
        <p class="modal-desc">
          LokMC provides a high-performance, single-port unified daemon for Minecraft server management.
        </p>
        <div class="doc-sections">
          <div class="doc-badge">Daemon Port: 8443</div>
          <div class="doc-badge">Protocol: REST / WebSockets</div>
          <div class="doc-badge">Isolation: Non-root POSIX namespaces</div>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  /* ── Floating Header Shell ── */
  .lokmc-floating-header {
    position: sticky;
    top: 14px;
    left: 0;
    right: 0;
    margin: 14px 28px 20px;
    z-index: 100;
  }

  .header-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    padding: 0 24px;
    background: var(--header-glass-bg);
    border: 1px solid var(--header-glass-border);
    border-radius: 9999px; /* Pill shape matching reference */
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    box-shadow: var(--glass-shadow);
    transition: background 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
  }

  /* ── Left Section ── */
  .header-left {
    display: flex;
    align-items: center;
    gap: 28px;
    flex: 1;
  }

  /* Theme Toggle Icon Button (Moon / Sun) */
  .theme-toggle-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: transparent;
    border: none;
    color: var(--color-text-primary);
    cursor: pointer;
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.2s ease;
    padding: 0;
  }

  .theme-toggle-btn:hover {
    background: rgba(0, 0, 0, 0.05);
    transform: scale(1.1) rotate(12deg);
  }

  :global([data-theme='dark']) .theme-toggle-btn:hover {
    background: rgba(255, 255, 255, 0.08);
  }

  .theme-icon {
    width: 22px;
    height: 22px;
    stroke: currentColor;
    transition: transform 0.3s ease;
  }

  .moon-icon {
    transform: rotate(-10deg);
  }

  /* Nav Links */
  .nav-links {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .nav-link-btn,
  .nav-item {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 7px 18px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: var(--color-text-primary);
    text-decoration: none;
    background: transparent;
    border: none;
    cursor: pointer;
    border-radius: 9999px;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    opacity: 0.65;
    text-transform: uppercase;
    font-family: inherit;
    white-space: nowrap;
  }

  .nav-link-btn:hover,
  .nav-item:hover {
    opacity: 1;
    background: rgba(0, 0, 0, 0.05);
    transform: translateY(-1px);
  }

  :global([data-theme='dark']) .nav-link-btn:hover,
  :global([data-theme='dark']) .nav-item:hover {
    background: rgba(255, 255, 255, 0.08);
  }

  /* Active Pill (White in Dark Mode, Dark in Light Mode) */
  .nav-link-btn.active-pill,
  .nav-pill-btn,
  .nav-item.active {
    opacity: 1;
    background: var(--pill-active-bg);
    color: var(--pill-active-text);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
    transform: none;
  }

  :global([data-theme='dark']) .nav-link-btn.active-pill,
  :global([data-theme='dark']) .nav-pill-btn,
  :global([data-theme='dark']) .nav-item.active {
    background: #ffffff;
    color: #0f1117;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
  }

  :global([data-theme='light']) .nav-link-btn.active-pill,
  :global([data-theme='light']) .nav-pill-btn,
  :global([data-theme='light']) .nav-item.active {
    background: #35353a;
    color: #ffffff;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  /* ── Center Brand Logo ── */
  .header-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    color: inherit;
    user-select: none;
    margin: 0 16px;
  }

  .brand-cube-container {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.12));
    transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .header-brand:hover .brand-cube-container {
    transform: scale(1.08) rotate(4deg);
  }

  .brand-cube-svg {
    width: 36px;
    height: 36px;
  }

  .cube-face-top {
    fill: #3e414c;
    transition: fill 0.25s ease;
  }
  .cube-face-left {
    fill: #22242c;
  }
  .cube-face-right {
    fill: #16181f;
  }

  :global([data-theme='dark']) .cube-face-top {
    fill: #4b4e5d;
  }
  :global([data-theme='dark']) .cube-face-left {
    fill: #2e313c;
  }
  :global([data-theme='dark']) .cube-face-right {
    fill: #1b1d24;
  }

  .brand-text-block {
    display: flex;
    flex-direction: column;
    line-height: 1.1;
  }

  .brand-title {
    font-size: 19px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--color-text-primary);
  }

  .brand-subtitle {
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: var(--color-text-tertiary);
    text-transform: capitalize;
  }

  /* ── Right Section ── */
  .header-right {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 24px;
    flex: 1;
  }

  /* Dark Active Pill Button for SERVERS as in reference screenshot */
  .nav-pill-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 7px 18px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.06em;
    border-radius: 9999px;
    text-decoration: none;
    text-transform: uppercase;
    background: var(--pill-active-bg);
    color: var(--pill-active-text);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease, opacity 0.2s ease;
  }

  .nav-pill-btn:hover {
    transform: translateY(-1px) scale(1.02);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.18);
    opacity: 0.95;
  }

  /* Utility Icons */
  .header-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .action-dropdown-wrapper {
    position: relative;
  }

  .action-icon-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: transparent;
    border: none;
    color: var(--color-text-primary);
    cursor: pointer;
    position: relative;
    padding: 0;
    transition: background 0.2s ease, transform 0.2s ease;
  }

  .action-icon-btn:hover {
    background: rgba(0, 0, 0, 0.06);
    transform: scale(1.08);
  }

  :global([data-theme='dark']) .action-icon-btn:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  .action-svg {
    width: 21px;
    height: 21px;
    stroke: currentColor;
  }

  .unread-badge {
    position: absolute;
    top: 4px;
    right: 4px;
    background: #ef4444;
    color: #fff;
    font-size: 10px;
    font-weight: 700;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid var(--color-bg-surface);
  }

  /* ── Glass Dropdowns ── */
  .glass-dropdown {
    position: absolute;
    top: calc(100% + 14px);
    right: 0;
    background: var(--header-glass-bg);
    border: 1px solid var(--header-glass-border);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border-radius: 20px;
    box-shadow: var(--glass-shadow);
    z-index: 200;
    animation: dropdown-pop 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  }

  @keyframes dropdown-pop {
    from {
      opacity: 0;
      transform: translateY(-8px) scale(0.96);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }

  .notifications-panel {
    width: 340px;
    padding: 16px;
  }

  .dropdown-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--sidebar-divider);
  }

  .dropdown-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--color-text-primary);
  }

  .clear-btn {
    background: none;
    border: none;
    color: var(--color-text-tertiary);
    font-size: 11px;
    cursor: pointer;
    transition: color 0.2s ease;
  }

  .clear-btn:hover {
    color: var(--color-text-primary);
  }

  .notifications-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-height: 280px;
    overflow-y: auto;
  }

  .notif-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 12px;
    background: rgba(0, 0, 0, 0.02);
    transition: background 0.15s ease;
  }

  :global([data-theme='dark']) .notif-item {
    background: rgba(255, 255, 255, 0.03);
  }

  .notif-item:hover {
    background: rgba(0, 0, 0, 0.05);
  }

  .notif-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
  }

  .notif-indicator.success { background: #22c55e; }
  .notif-indicator.info { background: #3b82f6; }

  .notif-content {
    flex: 1;
  }

  .notif-title-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 2px;
  }

  .notif-title {
    font-size: 12px;
    font-weight: 600;
    color: var(--color-text-primary);
  }

  .notif-time {
    font-size: 10px;
    color: var(--color-text-tertiary);
  }

  .notif-text {
    font-size: 11px;
    color: var(--color-text-secondary);
    line-height: 1.3;
    margin: 0;
  }

  .empty-notif {
    padding: 24px;
    text-align: center;
    color: var(--color-text-tertiary);
    font-size: 12px;
  }

  /* Profile Dropdown */
  .profile-panel {
    width: 240px;
    padding: 12px;
  }

  .user-meta-block {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px;
  }

  .user-avatar-mini {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: var(--color-accent);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
  }

  .user-text-info {
    display: flex;
    flex-direction: column;
  }

  .username-display {
    font-size: 13px;
    font-weight: 700;
    color: var(--color-text-primary);
  }

  .user-badge-role {
    font-size: 10px;
    color: var(--color-text-tertiary);
  }

  .menu-divider {
    height: 1px;
    background: var(--sidebar-divider);
    margin: 8px 0;
  }

  .menu-link-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 600;
    color: var(--color-text-secondary);
    text-decoration: none;
    background: none;
    border: none;
    width: 100%;
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
    font-family: inherit;
    text-align: left;
  }

  .menu-link-item:hover {
    background: rgba(0, 0, 0, 0.05);
    color: var(--color-text-primary);
  }

  :global([data-theme='dark']) .menu-link-item:hover {
    background: rgba(255, 255, 255, 0.06);
  }

  .logout-link {
    color: #ef4444;
  }

  .logout-link:hover {
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
  }

  .mobile-menu-btn {
    display: none;
    background: none;
    border: none;
    color: var(--color-text-primary);
    cursor: pointer;
    padding: 6px;
  }

  /* ── Modals ── */
  .modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
    animation: fade-in 0.2s ease;
  }

  @keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .modal-card {
    background: var(--color-bg-surface);
    border: 1px solid var(--header-glass-border);
    border-radius: 24px;
    box-shadow: var(--glass-shadow);
    width: 100%;
    max-width: 560px;
    padding: 28px;
    animation: modal-scale 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }

  @keyframes modal-scale {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }

  .modal-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--color-text-primary);
  }

  .modal-close-btn {
    background: none;
    border: none;
    color: var(--color-text-tertiary);
    font-size: 18px;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 8px;
  }

  .modal-close-btn:hover {
    color: var(--color-text-primary);
    background: rgba(0, 0, 0, 0.05);
  }

  .modal-desc {
    font-size: 14px;
    color: var(--color-text-secondary);
    margin-bottom: 20px;
    line-height: 1.5;
  }

  .support-cards-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }

  .support-card {
    padding: 16px;
    border-radius: 16px;
    background: rgba(0, 0, 0, 0.03);
    border: 1px solid var(--sidebar-divider);
    text-align: center;
  }

  :global([data-theme='dark']) .support-card {
    background: rgba(255, 255, 255, 0.03);
  }

  .support-icon {
    font-size: 24px;
    display: block;
    margin-bottom: 8px;
  }

  .support-card h4 {
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 6px;
    color: var(--color-text-primary);
  }

  .support-card p {
    font-size: 11px;
    color: var(--color-text-secondary);
    line-height: 1.4;
    margin: 0;
  }

  .doc-sections {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }

  .doc-badge {
    padding: 8px 14px;
    border-radius: 12px;
    background: rgba(0, 0, 0, 0.04);
    font-size: 12px;
    font-weight: 600;
    color: var(--color-text-primary);
    border: 1px solid var(--sidebar-divider);
  }

  :global([data-theme='dark']) .doc-badge {
    background: rgba(255, 255, 255, 0.04);
  }

  /* ── Responsive Mobile ── */
  @media (max-width: 1024px) {
    .nav-links-left {
      display: none;
    }
  }

  @media (max-width: 820px) {
    .lokmc-floating-header {
      margin: 10px 14px 16px;
    }

    .header-inner {
      padding: 0 16px;
      height: 56px;
    }

    .nav-links-right {
      display: none;
    }

    .mobile-menu-btn {
      display: block;
    }

    .brand-subtitle {
      display: none;
    }

    .mobile-drawer {
      margin-top: 10px;
      padding: 16px;
      background: var(--header-glass-bg);
      border: 1px solid var(--header-glass-border);
      border-radius: 20px;
      backdrop-filter: var(--glass-blur);
      box-shadow: var(--glass-shadow);
    }

    .mobile-nav-links {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .mobile-nav-link {
      font-size: 14px;
      font-weight: 700;
      color: var(--color-text-primary);
      text-decoration: none;
      background: none;
      border: none;
      text-align: left;
      padding: 6px 0;
      cursor: pointer;
    }
  }
</style>
