<!--
  LokMC — NameTab
  Server name, live Minecraft MOTD color preview box, and server.properties editor.
-->
<script lang="ts">
  let {
    server = $bindable(),
    selectedFile = 'server.properties',
    fileContent = $bindable(''),
    onSave = () => {}
  }: {
    server: any;
    selectedFile?: string;
    fileContent: string;
    onSave: () => void;
  } = $props();
</script>

<section class="view-card">
  <div class="card-header-flex">
    <div>
      <h2 class="section-heading">Server Identity & Properties</h2>
      <p class="section-subheading">Manage display naming, MOTD color preview, and server.properties.</p>
    </div>
    <button class="btn-glass-action" onclick={onSave}>
      Save Changes
    </button>
  </div>

  <div class="name-editor-grid">
    <div class="field-item">
      <label for="srv-name" class="field-label">SERVER DISPLAY NAME</label>
      <input id="srv-name" class="glass-input" bind:value={server.name} />
    </div>

    <div class="field-item">
      <label for="srv-motd" class="field-label">MESSAGE OF THE DAY (MOTD)</label>
      <input id="srv-motd" class="glass-input font-mono" bind:value={server.motd} />
    </div>
  </div>

  <!-- MOTD Preview Card -->
  <div class="motd-preview-card">
    <span class="motd-preview-label">LIVE IN-GAME MOTD PREVIEW:</span>
    <div class="motd-box">
      <div class="motd-line-1">
        <span class="mc-green">✦ </span>
        <span class="mc-aqua bold">LokMC Survival SMP</span>
        <span class="mc-green"> ✦ </span>
        <span class="mc-gray">Season 4 </span>
        <span class="mc-yellow">[1.21.1]</span>
      </div>
      <div class="motd-line-2">
        <span class="mc-white">High performance paper server with custom terrain and anti-grief.</span>
      </div>
    </div>
  </div>

  <!-- Quick File Editor -->
  <div class="file-editor-wrap">
    <div class="file-editor-header">
      <span class="file-title">📁 {selectedFile}</span>
      <span class="file-hint">Ready to edit</span>
    </div>
    <textarea class="properties-textarea" bind:value={fileContent} rows="10"></textarea>
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

  .name-editor-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }

  .field-item {
    display: flex;
    flex-direction: column;
    gap: 6px;
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
    border-radius: 14px;
    padding: 10px 14px;
    font-size: 13px;
    color: var(--color-text-primary);
    outline: none;
  }

  .font-mono {
    font-family: var(--font-mono);
  }

  .motd-preview-card {
    background: #111217;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 14px 18px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .motd-preview-label {
    font-size: 10px;
    font-weight: 700;
    color: #64748b;
    letter-spacing: 0.05em;
  }

  .motd-box {
    font-family: var(--font-mono);
    font-size: 13px;
    line-height: 1.5;
  }

  .mc-green { color: #55ff55; }
  .mc-aqua { color: #55ffff; }
  .mc-yellow { color: #ffff55; }
  .mc-gray { color: #aaaaaa; }
  .mc-white { color: #ffffff; }
  .bold { font-weight: 700; }

  .file-editor-wrap {
    display: flex;
    flex-direction: column;
    gap: 6px;
    background: rgba(0, 0, 0, 0.02);
    border: 1px solid var(--sidebar-divider);
    border-radius: 18px;
    padding: 14px;
  }

  .file-editor-header {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 700;
    color: var(--color-text-primary);
  }

  .properties-textarea {
    width: 100%;
    background: rgba(0, 0, 0, 0.03);
    border: 1px solid var(--sidebar-divider);
    border-radius: 12px;
    padding: 12px;
    font-family: var(--font-mono);
    font-size: 12px;
    line-height: 1.5;
    color: var(--color-text-primary);
    box-sizing: border-box;
    resize: vertical;
  }

  @media (max-width: 900px) {
    .name-editor-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
