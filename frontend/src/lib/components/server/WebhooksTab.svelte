<script lang="ts">
  interface WebhookConfig {
    url: string;
    onStart: boolean;
    onStop: boolean;
    onCrash: boolean;
    onPlayerJoin: boolean;
    onBackup: boolean;
  }

  interface Props {
    discordWebhook: WebhookConfig;
    server: { name: string; port: number };
    onShowToast: (msg: string) => void;
  }

  let { discordWebhook = $bindable(), server, onShowToast }: Props = $props();
  let webhookTestSuccess = $state(false);

  function testWebhook() {
    webhookTestSuccess = true;
    onShowToast('Simulated test webhook dispatched to Discord channel!');
  }
</script>

<section class="view-card" aria-label="Webhooks integration">
  <div class="card-header-flex">
    <div>
      <h2 class="section-heading">Discord & Slack Webhooks</h2>
      <p class="section-subheading">Push notifications to Discord channels on server starts, deaths, or crashes.</p>
    </div>
    <button class="btn-glass-action" onclick={testWebhook}>
      Send Test Ping
    </button>
  </div>

  <div class="webhook-config-box">
    <label for="wh-url" class="field-label">DISCORD WEBHOOK URL</label>
    <input
      id="wh-url"
      class="glass-input font-mono"
      bind:value={discordWebhook.url}
      placeholder="https://discord.com/api/webhooks/..."
    />

    <div class="webhook-events-list">
      <span class="events-title">SUBSCRIBED LIFECYCLE EVENTS:</span>
      <div class="events-checkboxes">
        <label class="event-checkbox">
          <input type="checkbox" bind:checked={discordWebhook.onStart} />
          <span>Node Startup</span>
        </label>
        <label class="event-checkbox">
          <input type="checkbox" bind:checked={discordWebhook.onStop} />
          <span>Node Shutdown</span>
        </label>
        <label class="event-checkbox">
          <input type="checkbox" bind:checked={discordWebhook.onCrash} />
          <span>Crash & Out-of-Memory Alerts</span>
        </label>
        <label class="event-checkbox">
          <input type="checkbox" bind:checked={discordWebhook.onPlayerJoin} />
          <span>Player Joins / Leaves</span>
        </label>
        <label class="event-checkbox">
          <input type="checkbox" bind:checked={discordWebhook.onBackup} />
          <span>Scheduled Backup Finished</span>
        </label>
      </div>
    </div>

    <!-- Discord Embed Preview -->
    {#if webhookTestSuccess}
      <div class="discord-embed-preview">
        <div class="discord-sidebar-pill"></div>
        <div class="discord-embed-body">
          <span class="embed-author">LokMC Node Daemon</span>
          <span class="embed-title">Server Online — {server.name}</span>
          <p class="embed-desc">Instance started on port {server.port}. 0/50 players connected.</p>
          <span class="embed-footer">Today at 12:00 PM • LokMC Cloud</span>
        </div>
      </div>
    {/if}
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

  .webhook-config-box {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .field-label {
    font-size: 11px;
    font-weight: 700;
    color: var(--color-text-tertiary);
    letter-spacing: 0.05em;
  }

  .glass-input {
    background: rgba(0, 0, 0, 0.03);
    border: 1px solid var(--sidebar-divider);
    border-radius: 12px;
    padding: 10px 14px;
    font-size: 13px;
    color: var(--color-text-primary);
    outline: none;
    transition: border-color 0.2s ease;
  }

  .glass-input:focus {
    border-color: var(--color-accent);
  }

  .font-mono {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  }

  .webhook-events-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .events-title {
    font-size: 11px;
    font-weight: 700;
    color: var(--color-text-tertiary);
  }

  .events-checkboxes {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }

  .event-checkbox {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: var(--color-text-secondary);
    cursor: pointer;
  }

  .event-checkbox input {
    accent-color: #22c55e;
  }

  .discord-embed-preview {
    display: flex;
    background: #2f3136;
    border-radius: 8px;
    padding: 12px 14px;
    max-width: 440px;
    margin-top: 8px;
  }

  .discord-sidebar-pill {
    width: 4px;
    background: #22c55e;
    border-radius: 4px;
    margin-right: 12px;
  }

  .discord-embed-body {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .embed-author { font-size: 11px; color: #b9bbbe; }
  .embed-title { font-size: 13px; font-weight: 700; color: #ffffff; }
  .embed-desc { font-size: 12px; color: #dcddde; margin: 0; }
  .embed-footer { font-size: 10px; color: #72767d; }

  @media (max-width: 900px) {
    .events-checkboxes {
      grid-template-columns: 1fr;
    }
  }
</style>
