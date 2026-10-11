<!--
  LokMC — Create Server Page

  Glassmorphic form wizard for creating a new Minecraft server.
  Supports "Generate Fresh World" or "Import Existing World Archive"
  with drag-and-drop file upload (.zip, .tar.gz, .mcworld).
-->
<script lang="ts">
  import { api } from '$lib/api';
  import { goto } from '$app/navigation';

  // Server configuration state
  let name = $state('');
  let serverType = $state('java');
  let version = $state('');
  let port = $state(25565);
  let memoryMin = $state(1024);
  let memoryMax = $state(2048);
  let cpuLimit = $state(2.0);
  let autoStart = $state(false);

  // World import state
  let worldMode = $state<'fresh' | 'import'>('fresh');
  let worldFile = $state<File | null>(null);
  let worldName = $state('world');
  let isDragging = $state(false);
  let uploadProgress = $state(0);

  // Form state
  let submitting = $state(false);
  let error = $state('');
  let step = $state<1 | 2 | 3>(1);

  const ACCEPTED_EXTS = ['.zip', '.tar.gz', '.tgz', '.mcworld'];

  function formatFileSize(bytes: number): string {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
  }

  function isValidArchive(file: File): boolean {
    const name = file.name.toLowerCase();
    return ACCEPTED_EXTS.some(ext => name.endsWith(ext));
  }

  function handleDragOver(e: DragEvent) {
    e.preventDefault();
    isDragging = true;
  }

  function handleDragLeave(e: DragEvent) {
    e.preventDefault();
    isDragging = false;
  }

  function handleDrop(e: DragEvent) {
    e.preventDefault();
    isDragging = false;
    const files = e.dataTransfer?.files;
    if (files && files.length > 0) {
      const f = files[0];
      if (isValidArchive(f)) {
        worldFile = f;
        error = '';
      } else {
        error = `Invalid file type. Supported: ${ACCEPTED_EXTS.join(', ')}`;
      }
    }
  }

  function handleFileInput(e: Event) {
    const input = e.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const f = input.files[0];
      if (isValidArchive(f)) {
        worldFile = f;
        error = '';
      } else {
        error = `Invalid file type. Supported: ${ACCEPTED_EXTS.join(', ')}`;
      }
    }
  }

  function removeFile() {
    worldFile = null;
    uploadProgress = 0;
  }

  function canProceedStep1(): boolean {
    return name.trim().length > 0;
  }

  function canProceedStep2(): boolean {
    return memoryMin <= memoryMax;
  }

  function canSubmit(): boolean {
    if (worldMode === 'import' && !worldFile) return false;
    return true;
  }

  function goStep(target: 1 | 2 | 3) {
    if (target === 2 && !canProceedStep1()) {
      error = 'Please enter a server name.';
      return;
    }
    if (target === 3 && !canProceedStep2()) {
      error = 'Minimum memory cannot exceed maximum memory.';
      return;
    }
    error = '';
    step = target;
  }

  async function handleSubmit(e: Event) {
    e.preventDefault();
    error = '';

    if (!canProceedStep1() || !canProceedStep2() || !canSubmit()) {
      error = 'Please complete all required fields.';
      return;
    }

    submitting = true;
    try {
      // 1. Create the server
      const server = await api.createServer({
        name,
        server_type: serverType,
        version: version || undefined,
        port,
        memory_min: memoryMin,
        memory_max: memoryMax,
        cpu_limit: cpuLimit,
        auto_start: autoStart,
      });

      // 2. Import world archive if selected
      if (worldMode === 'import' && worldFile) {
        uploadProgress = 30;
        try {
          await api.importWorld(server.id, worldFile, worldName || 'world');
          uploadProgress = 100;
        } catch (importErr: any) {
          // Server was created, but import failed — redirect anyway with warning
          console.error('World import failed:', importErr);
        }
      }

      goto(`/servers/${server.id}`);
    } catch (err: any) {
      error = err.detail || 'Failed to create server.';
    } finally {
      submitting = false;
    }
  }
</script>

<svelte:head>
  <title>Create Server — LokMC</title>
</svelte:head>

<div class="create-page">
  <!-- Page Header -->
  <div class="create-hero">
    <div class="hero-text">
      <h1 class="hero-title">Create New Server</h1>
      <p class="hero-subtitle">Configure, provision, and launch a Minecraft server instance.</p>
    </div>
  </div>

  <!-- Step Indicator -->
  <div class="step-track">
    {#each [
      { num: 1, label: 'Server Info' },
      { num: 2, label: 'Resources' },
      { num: 3, label: 'World Data' }
    ] as s}
      <button
        class="step-pill"
        class:active={step === s.num}
        class:completed={step > s.num}
        onclick={() => goStep(s.num as 1 | 2 | 3)}
        type="button"
      >
        <span class="step-num">
          {#if step > s.num}
            ✓
          {:else}
            {s.num}
          {/if}
        </span>
        <span class="step-label">{s.label}</span>
      </button>
      {#if s.num < 3}
        <div class="step-connector" class:done={step > s.num}></div>
      {/if}
    {/each}
  </div>

  {#if error}
    <div class="create-error" role="alert">
      <span>{error}</span>
      <button class="dismiss-btn" onclick={() => (error = '')} aria-label="Dismiss">×</button>
    </div>
  {/if}

  <form onsubmit={handleSubmit} class="create-form">
    <!-- Step 1: Server Information -->
    {#if step === 1}
      <section class="glass-card step-card">
        <div class="card-title-row">
          <span class="card-icon">🖥️</span>
          <div>
            <h2 class="card-heading">Server Information</h2>
            <p class="card-subheading">Basic identity and connection details.</p>
          </div>
        </div>

        <div class="form-grid">
          <div class="form-group">
            <label class="form-label" for="server-name">Server Name</label>
            <input
              id="server-name"
              class="glass-input"
              type="text"
              bind:value={name}
              required
              minlength={1}
              maxlength={128}
              placeholder="Survival SMP - Season 4"
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="server-type">Server Type</label>
            <select id="server-type" class="glass-input" bind:value={serverType}>
              <option value="java">Java Edition</option>
              <option value="bedrock">Bedrock Edition</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label" for="server-version">
              Version
              <span class="label-optional">(optional)</span>
            </label>
            <input
              id="server-version"
              class="glass-input"
              type="text"
              bind:value={version}
              placeholder="1.21.1"
            />
            <span class="form-hint">Leave blank for latest stable.</span>
          </div>

          <div class="form-group">
            <label class="form-label" for="server-port">Port</label>
            <input
              id="server-port"
              class="glass-input"
              type="number"
              bind:value={port}
              required
              min={1024}
              max={65535}
            />
          </div>
        </div>

        <div class="step-nav">
          <span></span>
          <button
            class="btn-glass-next"
            type="button"
            onclick={() => goStep(2)}
            disabled={!canProceedStep1()}
          >
            Continue →
          </button>
        </div>
      </section>
    {/if}

    <!-- Step 2: Resource Limits -->
    {#if step === 2}
      <section class="glass-card step-card">
        <div class="card-title-row">
          <span class="card-icon">⚙️</span>
          <div>
            <h2 class="card-heading">Resource Limits</h2>
            <p class="card-subheading">Memory, CPU, and auto-start configuration.</p>
          </div>
        </div>

        <div class="form-grid">
          <div class="form-group">
            <label class="form-label" for="memory-min">Min Memory (MB)</label>
            <input
              id="memory-min"
              class="glass-input"
              type="number"
              bind:value={memoryMin}
              required
              min={512}
              step={256}
            />
            <span class="form-hint">{(memoryMin / 1024).toFixed(1)} GB</span>
          </div>

          <div class="form-group">
            <label class="form-label" for="memory-max">Max Memory (MB)</label>
            <input
              id="memory-max"
              class="glass-input"
              type="number"
              bind:value={memoryMax}
              required
              min={512}
              step={256}
            />
            <span class="form-hint">{(memoryMax / 1024).toFixed(1)} GB</span>
          </div>

          <div class="form-group">
            <label class="form-label" for="cpu-limit">CPU Cores</label>
            <input
              id="cpu-limit"
              class="glass-input"
              type="number"
              bind:value={cpuLimit}
              required
              min={0.5}
              max={16}
              step={0.5}
            />
          </div>

          <div class="form-group checkbox-row">
            <input
              id="auto-start"
              type="checkbox"
              bind:checked={autoStart}
              class="glass-checkbox"
            />
            <label class="form-label" for="auto-start">
              Auto-start when panel launches
            </label>
          </div>
        </div>

        <div class="step-nav">
          <button class="btn-glass-back" type="button" onclick={() => goStep(1)}>
            ← Back
          </button>
          <button
            class="btn-glass-next"
            type="button"
            onclick={() => goStep(3)}
            disabled={!canProceedStep2()}
          >
            Continue →
          </button>
        </div>
      </section>
    {/if}

    <!-- Step 3: World Data -->
    {#if step === 3}
      <section class="glass-card step-card">
        <div class="card-title-row">
          <span class="card-icon">🌍</span>
          <div>
            <h2 class="card-heading">World Data</h2>
            <p class="card-subheading">Generate a fresh world or import an existing one.</p>
          </div>
        </div>

        <!-- World Mode Toggle -->
        <div class="mode-toggle">
          <button
            class="mode-btn"
            class:active={worldMode === 'fresh'}
            type="button"
            onclick={() => { worldMode = 'fresh'; worldFile = null; }}
          >
            <span class="mode-icon">✨</span>
            Generate Fresh World
          </button>
          <button
            class="mode-btn"
            class:active={worldMode === 'import'}
            type="button"
            onclick={() => { worldMode = 'import'; }}
          >
            <span class="mode-icon">📦</span>
            Import World Archive
          </button>
        </div>

        {#if worldMode === 'fresh'}
          <div class="fresh-world-info">
            <div class="info-icon-block">
              <span class="info-glyph">🗺️</span>
            </div>
            <div>
              <p class="info-title">Procedural Generation</p>
              <p class="info-desc">
                The server will generate a brand-new world using the default seed and terrain settings.
                You can customize world generation later via <code>server.properties</code>.
              </p>
            </div>
          </div>
        {:else}
          <!-- Import World Section -->
          <div class="import-section">
            <div class="form-group">
              <label class="form-label" for="world-name">World Folder Name</label>
              <input
                id="world-name"
                class="glass-input"
                type="text"
                bind:value={worldName}
                placeholder="world"
              />
              <span class="form-hint">Maps to <code>level-name</code> in server.properties.</span>
            </div>

            <!-- Drag & Drop Zone -->
            {#if !worldFile}
              <div
                class="dropzone"
                class:dragging={isDragging}
                role="button"
                tabindex="0"
                ondragover={handleDragOver}
                ondragleave={handleDragLeave}
                ondrop={handleDrop}
                onclick={() => document.getElementById('world-file-input')?.click()}
                onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') document.getElementById('world-file-input')?.click(); }}
              >
                <input
                  id="world-file-input"
                  type="file"
                  accept=".zip,.tar.gz,.tgz,.mcworld"
                  onchange={handleFileInput}
                  style="display: none;"
                />
                <div class="dropzone-content">
                  <span class="dropzone-icon">
                    {#if isDragging}
                      📥
                    {:else}
                      📁
                    {/if}
                  </span>
                  <p class="dropzone-title">
                    {#if isDragging}
                      Drop your world archive here
                    {:else}
                      Drag & drop world archive
                    {/if}
                  </p>
                  <p class="dropzone-hint">or click to browse — .zip, .tar.gz, .mcworld</p>
                </div>
              </div>
            {:else}
              <!-- Selected File Card -->
              <div class="file-card">
                <div class="file-info">
                  <span class="file-icon">🗂️</span>
                  <div>
                    <span class="file-name">{worldFile.name}</span>
                    <span class="file-size">{formatFileSize(worldFile.size)}</span>
                  </div>
                </div>
                <button
                  class="file-remove"
                  type="button"
                  onclick={removeFile}
                  aria-label="Remove file"
                >
                  ×
                </button>
              </div>

              {#if uploadProgress > 0 && uploadProgress < 100}
                <div class="upload-progress">
                  <div class="progress-track">
                    <div class="progress-fill" style="width: {uploadProgress}%"></div>
                  </div>
                  <span class="progress-label">Uploading... {uploadProgress}%</span>
                </div>
              {/if}
            {/if}
          </div>
        {/if}

        <!-- Final Actions -->
        <div class="step-nav">
          <button class="btn-glass-back" type="button" onclick={() => goStep(2)}>
            ← Back
          </button>
          <button
            class="btn-create"
            type="submit"
            disabled={submitting || !canSubmit() || !canProceedStep1()}
          >
            {#if submitting}
              <span class="micro-spinner"></span>
              {worldMode === 'import' ? 'Creating & Importing…' : 'Creating Server…'}
            {:else}
              🚀 Create Server
            {/if}
          </button>
        </div>
      </section>
    {/if}
  </form>
</div>

<style>
  .create-page {
    max-width: 780px;
    margin: 0 auto;
    padding: 0 8px;
  }

  /* Hero Header */
  .create-hero {
    margin-bottom: 24px;
  }

  .hero-title {
    font-size: 26px;
    font-weight: 900;
    color: var(--color-text-primary);
    margin: 0 0 4px 0;
    letter-spacing: -0.5px;
  }

  .hero-subtitle {
    font-size: 14px;
    color: var(--color-text-secondary);
    margin: 0;
  }

  /* Step Indicator Track */
  .step-track {
    display: flex;
    align-items: center;
    gap: 0;
    margin-bottom: 22px;
    padding: 14px 20px;
    background: var(--glass-bg);
    border: 1px solid var(--header-glass-border);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border-radius: 22px;
    box-shadow: var(--glass-shadow);
  }

  .step-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 9999px;
    border: none;
    background: transparent;
    color: var(--color-text-tertiary);
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    white-space: nowrap;
  }

  .step-pill.active {
    background: var(--pill-active-bg);
    color: var(--pill-active-text);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .step-pill.completed {
    color: var(--color-accent);
  }

  .step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    font-size: 11px;
    font-weight: 800;
    background: rgba(0, 0, 0, 0.06);
    color: inherit;
    transition: background 0.2s;
  }

  .step-pill.active .step-num {
    background: var(--color-accent);
    color: #fff;
  }

  .step-pill.completed .step-num {
    background: var(--color-accent);
    color: #fff;
  }

  .step-connector {
    flex: 1;
    height: 2px;
    background: rgba(255, 255, 255, 0.06);
    margin: 0 4px;
    border-radius: 2px;
    transition: background 0.3s;
  }

  .step-connector.done {
    background: var(--color-accent);
  }

  .step-label {
    display: inline;
  }

  @media (max-width: 520px) {
    .step-label { display: none; }
    .step-pill { padding: 6px 10px; }
  }

  /* Glass Card */
  .glass-card {
    background: var(--glass-bg);
    border: 1px solid var(--header-glass-border);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border-radius: 28px;
    box-shadow: var(--glass-shadow);
    padding: 28px 30px;
    display: flex;
    flex-direction: column;
    gap: 22px;
  }

  .step-card {
    animation: card-enter 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  }

  @keyframes card-enter {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .card-title-row {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .card-icon {
    font-size: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 16px;
    background: rgba(0, 0, 0, 0.04);
    border: 1px solid var(--sidebar-divider);
    flex-shrink: 0;
  }

  .card-heading {
    font-size: 19px;
    font-weight: 800;
    color: var(--color-text-primary);
    margin: 0 0 2px 0;
  }

  .card-subheading {
    font-size: 13px;
    color: var(--color-text-secondary);
    margin: 0;
  }

  /* Form Elements */
  .create-form {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
  }

  @media (max-width: 639px) {
    .form-grid { grid-template-columns: 1fr; }
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .form-label {
    font-size: 12px;
    font-weight: 700;
    color: var(--color-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .label-optional {
    font-weight: 500;
    text-transform: none;
    color: var(--color-text-tertiary);
    letter-spacing: 0;
  }

  .glass-input {
    padding: 10px 14px;
    border-radius: 14px;
    border: 1px solid var(--sidebar-divider);
    background: rgba(0, 0, 0, 0.04);
    color: var(--color-text-primary);
    font-size: 14px;
    font-weight: 500;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
    color-scheme: dark;
  }

  :global([data-theme="light"]) .glass-input {
    color-scheme: light;
  }

  .glass-input:focus {
    border-color: var(--color-accent);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
  }

  .glass-input::placeholder {
    color: var(--color-text-tertiary);
  }

  select.glass-input option {
    background: var(--color-bg-primary);
    color: var(--color-text-primary);
  }

  .form-hint {
    font-size: 11px;
    color: var(--color-text-tertiary);
  }

  .form-hint code {
    font-size: 11px;
    padding: 1px 5px;
    border-radius: 4px;
    background: rgba(0, 0, 0, 0.08);
    color: var(--color-accent);
  }

  .checkbox-row {
    flex-direction: row;
    align-items: center;
    gap: 10px;
    padding-top: 18px;
  }

  .glass-checkbox {
    width: 18px;
    height: 18px;
    accent-color: var(--color-accent);
    cursor: pointer;
  }

  .checkbox-row .form-label {
    text-transform: none;
    font-weight: 600;
    font-size: 13px;
    letter-spacing: 0;
    cursor: pointer;
    margin: 0;
  }

  /* Step Navigation */
  .step-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 8px;
  }

  .btn-glass-next,
  .btn-glass-back {
    padding: 9px 22px;
    border-radius: 9999px;
    border: 1px solid var(--sidebar-divider);
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .btn-glass-next {
    background: var(--color-accent);
    color: #fff;
    border-color: transparent;
  }

  .btn-glass-next:hover:not(:disabled) {
    background: var(--color-accent-hover);
    transform: translateY(-1px);
  }

  .btn-glass-next:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .btn-glass-back {
    background: transparent;
    color: var(--color-text-secondary);
  }

  .btn-glass-back:hover {
    background: rgba(0, 0, 0, 0.04);
  }

  /* World Mode Toggle */
  .mode-toggle {
    display: flex;
    gap: 10px;
  }

  .mode-btn {
    flex: 1;
    padding: 14px 18px;
    border-radius: 18px;
    border: 2px solid var(--sidebar-divider);
    background: rgba(0, 0, 0, 0.02);
    color: var(--color-text-secondary);
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .mode-btn.active {
    border-color: var(--color-accent);
    background: rgba(99, 102, 241, 0.08);
    color: var(--color-text-primary);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  }

  .mode-btn:hover:not(.active) {
    border-color: rgba(99, 102, 241, 0.3);
    background: rgba(0, 0, 0, 0.04);
  }

  .mode-icon {
    font-size: 20px;
  }

  @media (max-width: 520px) {
    .mode-toggle { flex-direction: column; }
  }

  /* Fresh World Info */
  .fresh-world-info {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 18px 20px;
    border-radius: 18px;
    background: rgba(59, 130, 246, 0.06);
    border: 1px solid rgba(59, 130, 246, 0.15);
  }

  .info-icon-block {
    flex-shrink: 0;
  }

  .info-glyph {
    font-size: 28px;
  }

  .info-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--color-text-primary);
    margin: 0 0 4px 0;
  }

  .info-desc {
    font-size: 13px;
    color: var(--color-text-secondary);
    margin: 0;
    line-height: 1.5;
  }

  .info-desc code {
    font-size: 12px;
    padding: 1px 5px;
    border-radius: 4px;
    background: rgba(0, 0, 0, 0.08);
    color: var(--color-accent);
  }

  /* Import Section */
  .import-section {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  /* Dropzone */
  .dropzone {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 160px;
    border: 2px dashed var(--sidebar-divider);
    border-radius: 22px;
    background: rgba(0, 0, 0, 0.02);
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .dropzone:hover {
    border-color: rgba(99, 102, 241, 0.4);
    background: rgba(99, 102, 241, 0.04);
  }

  .dropzone.dragging {
    border-color: var(--color-accent);
    background: rgba(99, 102, 241, 0.08);
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.12);
    transform: scale(1.01);
  }

  .dropzone-content {
    text-align: center;
    padding: 24px;
  }

  .dropzone-icon {
    font-size: 36px;
    display: block;
    margin-bottom: 10px;
  }

  .dropzone-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--color-text-primary);
    margin: 0 0 4px 0;
  }

  .dropzone-hint {
    font-size: 12px;
    color: var(--color-text-tertiary);
    margin: 0;
  }

  /* File Card */
  .file-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 18px;
    border-radius: 18px;
    background: rgba(34, 197, 94, 0.06);
    border: 1px solid rgba(34, 197, 94, 0.2);
    animation: card-enter 0.25s ease;
  }

  .file-info {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .file-icon {
    font-size: 24px;
  }

  .file-name {
    font-size: 13px;
    font-weight: 700;
    color: var(--color-text-primary);
    display: block;
  }

  .file-size {
    font-size: 11px;
    color: var(--color-text-tertiary);
  }

  .file-remove {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: none;
    background: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
  }

  .file-remove:hover {
    background: rgba(239, 68, 68, 0.2);
  }

  /* Upload Progress */
  .upload-progress {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .progress-track {
    height: 6px;
    background: rgba(0, 0, 0, 0.06);
    border-radius: 9999px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: var(--color-accent);
    border-radius: 9999px;
    transition: width 0.5s ease;
  }

  .progress-label {
    font-size: 11px;
    color: var(--color-text-tertiary);
  }

  /* Create Button */
  .btn-create {
    padding: 10px 26px;
    border-radius: 9999px;
    border: none;
    background: linear-gradient(135deg, var(--color-accent), #7c3aed);
    color: #fff;
    font-size: 14px;
    font-weight: 800;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .btn-create:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35);
  }

  .btn-create:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .micro-spinner {
    display: inline-block;
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

  /* Error Banner */
  .create-error {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 18px;
    margin-bottom: 8px;
    font-size: 13px;
    font-weight: 600;
    color: #ef4444;
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.18);
    border-radius: 16px;
    animation: card-enter 0.2s ease;
  }

  .dismiss-btn {
    background: none;
    border: none;
    color: #ef4444;
    font-size: 18px;
    font-weight: 700;
    cursor: pointer;
    padding: 0 4px;
    opacity: 0.6;
    transition: opacity 0.15s;
  }

  .dismiss-btn:hover {
    opacity: 1;
  }
</style>
