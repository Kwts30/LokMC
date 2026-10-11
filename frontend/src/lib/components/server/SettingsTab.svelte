<script lang="ts">
  interface Props {
    server: { auto_start: boolean; [key: string]: any };
    onShowToast: (msg: string) => void;
  }

  let { server = $bindable(), onShowToast }: Props = $props();
  let selectedJava = $state('Java 21 LTS (Recommended)');
  let aikarFlags = $state(true);

  function handleReinstall() {
    if (confirm('Are you sure you want to reinstall and reset this server?')) {
      onShowToast('Server reinstalled to default state.');
    }
  }

  function handleDelete() {
    if (confirm('Permanently delete this server and all world data? This cannot be undone.')) {
      onShowToast('Server deleted permanently.');
    }
  }
</script>

<section class="view-card" aria-label="Server settings and container runtime">
  <div class="card-header-flex">
    <div>
      <h2 class="section-heading">JVM Runtime & Container Engine</h2>
      <p class="section-subheading">Java memory flags, auto-start policies, and destructive actions.</p>
    </div>
    <button class="btn-glass-action" onclick={() => onShowToast('Saved runtime flags.')}>
      Save Settings
    </button>
  </div>

  <div class="settings-rows-list">
    <div class="setting-item">
      <div>
        <span class="setting-title">Java Runtime Environment</span>
        <p class="setting-desc">Select Java version installed on host machine.</p>
      </div>
      <select class="glass-select-sm" bind:value={selectedJava}>
        <option>Java 21 LTS (Recommended)</option>
        <option>Java 17 LTS</option>
        <option>Java 8 (Legacy)</option>
      </select>
    </div>

    <div class="setting-item">
      <div>
        <span class="setting-title">Aikar's Garbage Collection Flags</span>
        <p class="setting-desc">Optimizes G1GC for low latency and zero tick hiccups.</p>
      </div>
      <label class="switch-toggle" aria-label="Toggle Aikar Flags">
        <input type="checkbox" bind:checked={aikarFlags} />
        <span class="switch-slider"></span>
      </label>
    </div>

    <div class="setting-item">
      <div>
        <span class="setting-title">Auto-start on System Boot</span>
        <p class="setting-desc">Automatically spin up server when LokMC daemon restarts.</p>
      </div>
      <label class="switch-toggle" aria-label="Toggle auto start">
        <input type="checkbox" bind:checked={server.auto_start} />
        <span class="switch-slider"></span>
      </label>
    </div>
  </div>

  <!-- Danger Zone -->
  <div class="danger-zone-card">
    <h3 class="danger-title">Danger Zone</h3>
    <p class="danger-desc">
      Destructive operations cannot be undone. Always create a backup before proceeding.
    </p>
    <div class="danger-actions-row">
      <button
        type="button"
        class="btn-danger-pill"
        onclick={handleReinstall}
      >
        Reinstall Server
      </button>
      <button
        type="button"
        class="btn-danger-pill"
        onclick={handleDelete}
      >
        Delete Server Permanently
      </button>
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

  .btn-glass-action {
    background: rgba(0, 0, 0, 0.04);
    border: 1px solid var(--sidebar-divider);
    padding: 8px 18px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    color: var(--color-text-primary);
    transition: all 0.2s ease;
  }

  .btn-glass-action:hover {
    background: rgba(0, 0, 0, 0.08);
  }

  :global([data-theme='dark']) .btn-glass-action {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.1);
  }

  :global([data-theme='dark']) .btn-glass-action:hover {
    background: rgba(255, 255, 255, 0.12);
  }

  .settings-rows-list {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .setting-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 18px;
    border-radius: 16px;
    background: rgba(0, 0, 0, 0.02);
    border: 1px solid var(--sidebar-divider);
  }

  :global([data-theme='dark']) .setting-item {
    background: rgba(255, 255, 255, 0.03);
    border-color: rgba(255, 255, 255, 0.08);
  }

  .setting-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--color-text-primary);
    display: block;
  }

  .setting-desc {
    font-size: 12px;
    color: var(--color-text-tertiary);
    margin: 2px 0 0 0;
  }

  .glass-select-sm {
    background: rgba(0, 0, 0, 0.04);
    border: 1px solid var(--sidebar-divider);
    border-radius: 10px;
    padding: 6px 10px;
    font-size: 12px;
    color: var(--color-text-primary);
    outline: none;
    cursor: pointer;
    color-scheme: dark;
  }

  :global([data-theme='light']) .glass-select-sm {
    color-scheme: light;
  }

  .glass-select-sm option {
    background-color: #1a1d2a;
    color: #e8eaf0;
    padding: 8px 12px;
  }

  :global([data-theme='light']) .glass-select-sm option {
    background-color: #ffffff;
    color: #121316;
  }

  :global([data-theme='dark']) .glass-select-sm {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.12);
  }


  /* Toggle Switch */
  .switch-toggle {
    position: relative;
    display: inline-block;
    width: 42px;
    height: 24px;
    flex-shrink: 0;
  }

  .switch-toggle input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  .switch-slider {
    position: absolute;
    cursor: pointer;
    inset: 0;
    background-color: #cbd5e1;
    border-radius: 9999px;
    transition: 0.25s;
  }

  .switch-slider:before {
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    border-radius: 50%;
    transition: 0.25s;
  }

  input:checked + .switch-slider {
    background-color: #22c55e;
  }

  input:checked + .switch-slider:before {
    transform: translateX(18px);
  }

  /* Danger Zone */
  .danger-zone-card {
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 20px;
    padding: 20px;
    background: rgba(239, 68, 68, 0.03);
    margin-top: 10px;
  }

  .danger-title {
    color: #ef4444;
    font-size: 16px;
    font-weight: 800;
    margin: 0 0 4px 0;
  }

  .danger-desc {
    font-size: 13px;
    color: var(--color-text-secondary);
    margin: 0 0 16px 0;
  }

  .danger-actions-row {
    display: flex;
    gap: 12px;
  }

  .btn-danger-pill {
    padding: 8px 18px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 700;
    background: rgba(239, 68, 68, 0.12);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
    cursor: pointer;
    transition: background 0.2s ease, color 0.2s ease;
  }

  .btn-danger-pill:hover {
    background: #ef4444;
    color: #ffffff;
  }

  @media (max-width: 600px) {
    .danger-actions-row {
      flex-direction: column;
    }
  }
</style>
