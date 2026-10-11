<!--
  LokMC — BackupTab
  Storage meter, snapshot creation, backup archive management,
  and world archive import for existing servers.
-->
<script lang="ts">
  import { api } from '$lib/api';

  let {
    serverId,
    serverStatus = 'stopped',
    backups = $bindable([]),
    isCreatingBackup = false,
    onTriggerBackup = () => {},
    onRestore = (name: string) => {},
    onDownload = (name: string) => {},
    onShowToast = (msg: string) => {}
  }: {
    serverId: number;
    serverStatus?: string;
    backups: any[];
    isCreatingBackup?: boolean;
    onTriggerBackup?: () => void;
    onRestore?: (name: string) => void;
    onDownload?: (name: string) => void;
    onShowToast?: (msg: string) => void;
  } = $props();

  // Import world state
  let showImportModal = $state(false);
  let importFile = $state<File | null>(null);
  let importWorldName = $state('world');
  let importing = $state(false);
  let isDragging = $state(false);

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
    if (files && files.length > 0 && isValidArchive(files[0])) {
      importFile = files[0];
    }
  }

  function handleFileInput(e: Event) {
    const input = e.target as HTMLInputElement;
    if (input.files && input.files.length > 0 && isValidArchive(input.files[0])) {
      importFile = input.files[0];
    }
  }

  async function handleImport() {
    if (!importFile) return;
    importing = true;
    try {
      const result = await api.importWorld(serverId, importFile, importWorldName || 'world');
      onShowToast(`World imported: ${result.files_extracted} files extracted into '${result.world_name}'`);
      showImportModal = false;
      importFile = null;
      importWorldName = 'world';
    } catch (err: any) {
      onShowToast(err.detail || 'World import failed.');
    } finally {
      importing = false;
    }
  }

  function openImportModal() {
    if (serverStatus === 'running') {
      onShowToast('Stop the server before importing a world.');
      return;
    }
    showImportModal = true;
  }

  function closeImportModal() {
    showImportModal = false;
    importFile = null;
    importWorldName = 'world';
  }
</script>

<section class="view-card">
  <div class="card-header-flex">
    <div>
      <h2 class="section-heading">Snapshot & Backup Archives</h2>
      <p class="section-subheading">Automated tarball snapshots of world saves and configuration files.</p>
    </div>
    <div class="header-actions">
      <button
        class="btn-glass-action btn-import-glass"
        onclick={openImportModal}
        type="button"
      >
        📦 Import World
      </button>
      <button
        class="btn-glass-action btn-primary-glass"
        disabled={isCreatingBackup}
        onclick={onTriggerBackup}
      >
        {#if isCreatingBackup}
          <span class="micro-spinner"></span> Creating...
        {:else}
          Create Snapshot Now
        {/if}
      </button>
    </div>
  </div>

  <!-- Backup Storage Gauge -->
  <div class="backup-meter-block">
    <div class="meter-info">
      <span>Storage Used: <strong>2.48 GB</strong> of 50.0 GB</span>
      <span class="meter-pct">5%</span>
    </div>
    <div class="meter-track">
      <div class="meter-fill" style="width: 5%;"></div>
    </div>
  </div>

  <!-- Backups List -->
  <div class="backups-list">
    {#each backups as bk}
      <div class="backup-row-item">
        <div class="backup-meta">
          <span class="backup-file-icon">💾</span>
          <div>
            <span class="backup-file-name">{bk.name}</span>
            <span class="backup-subtext">{bk.size} • Created {bk.date}</span>
          </div>
        </div>
        <div class="backup-actions">
          <span class="bk-tag {bk.type.toLowerCase()}">{bk.type}</span>
          <button class="ghost-btn-sm" onclick={() => onRestore(bk.name)}>Restore</button>
          <button class="ghost-btn-sm" onclick={() => onDownload(bk.name)}>Download</button>
        </div>
      </div>
    {/each}
  </div>
</section>

<!-- Import World Modal Overlay -->
{#if showImportModal}
  <div class="modal-overlay" onclick={closeImportModal} role="presentation">
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <div class="modal-card" onclick={(e) => e.stopPropagation()} role="dialog" aria-modal="true" aria-label="Import World Archive" tabindex="-1">
      <div class="modal-header">
        <h3 class="modal-title">📦 Import World Archive</h3>
        <button class="modal-close" onclick={closeImportModal} aria-label="Close">×</button>
      </div>

      <div class="modal-body">
        <div class="modal-form-group">
          <label class="modal-label" for="import-world-name">World Folder Name</label>
          <input
            id="import-world-name"
            class="modal-input"
            type="text"
            bind:value={importWorldName}
            placeholder="world"
          />
          <span class="modal-hint">Maps to <code>level-name</code> in server.properties.</span>
        </div>

        {#if !importFile}
          <div
            class="modal-dropzone"
            class:dragging={isDragging}
            role="button"
            tabindex="0"
            ondragover={handleDragOver}
            ondragleave={handleDragLeave}
            ondrop={handleDrop}
            onclick={() => document.getElementById('import-file-input')?.click()}
            onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') document.getElementById('import-file-input')?.click(); }}
          >
            <input
              id="import-file-input"
              type="file"
              accept=".zip,.tar.gz,.tgz,.mcworld"
              onchange={handleFileInput}
              style="display: none;"
            />
            <span class="dz-icon">{isDragging ? '📥' : '📁'}</span>
            <p class="dz-title">{isDragging ? 'Drop here' : 'Drag & drop world archive'}</p>
            <p class="dz-hint">.zip, .tar.gz, .mcworld</p>
          </div>
        {:else}
          <div class="modal-file-card">
            <div class="mf-info">
              <span class="mf-icon">🗂️</span>
              <div>
                <span class="mf-name">{importFile.name}</span>
                <span class="mf-size">{formatFileSize(importFile.size)}</span>
              </div>
            </div>
            <button class="mf-remove" onclick={() => { importFile = null; }} aria-label="Remove">×</button>
          </div>
        {/if}
      </div>

      <div class="modal-footer">
        <button class="btn-modal-cancel" onclick={closeImportModal} type="button">Cancel</button>
        <button
          class="btn-modal-import"
          onclick={handleImport}
          disabled={!importFile || importing}
          type="button"
        >
          {#if importing}
            <span class="micro-spinner"></span> Importing…
          {:else}
            🚀 Import
          {/if}
        </button>
      </div>
    </div>
  </div>
{/if}

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

  .header-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
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

  .btn-primary-glass {
    background: var(--color-accent);
    color: #fff;
    border-color: transparent;
  }

  .btn-primary-glass:hover {
    background: var(--color-accent-hover);
  }

  .btn-import-glass {
    background: rgba(168, 85, 247, 0.1);
    color: #a855f7;
    border-color: rgba(168, 85, 247, 0.2);
  }

  .btn-import-glass:hover {
    background: rgba(168, 85, 247, 0.18);
  }

  .micro-spinner {
    display: inline-block;
    width: 12px;
    height: 12px;
    border: 2px solid currentColor;
    border-top-color: transparent;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .backup-meter-block {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 14px 18px;
    background: rgba(0, 0, 0, 0.02);
    border: 1px solid var(--sidebar-divider);
    border-radius: 18px;
  }

  .meter-info {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    color: var(--color-text-secondary);
  }

  .meter-track {
    height: 8px;
    background: rgba(0, 0, 0, 0.06);
    border-radius: 9999px;
    overflow: hidden;
  }

  .meter-fill {
    height: 100%;
    background: #3b82f6;
    border-radius: 9999px;
  }

  .backups-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .backup-row-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 18px;
    border-radius: 16px;
    background: rgba(0, 0, 0, 0.02);
    border: 1px solid var(--sidebar-divider);
  }

  .backup-meta {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .backup-file-icon {
    font-size: 20px;
  }

  .backup-file-name {
    font-size: 13px;
    font-weight: 700;
    color: var(--color-text-primary);
    display: block;
  }

  .backup-subtext {
    font-size: 11px;
    color: var(--color-text-tertiary);
  }

  .backup-actions {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .bk-tag {
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 9999px;
    text-transform: uppercase;
  }

  .bk-tag.scheduled { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
  .bk-tag.manual { background: rgba(168, 85, 247, 0.1); color: #a855f7; }

  .ghost-btn-sm {
    background: none;
    border: 1px solid var(--sidebar-divider);
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    color: var(--color-text-secondary);
  }

  /* ── Modal Overlay ────────────────────────────────────── */
  .modal-overlay {
    position: fixed;
    inset: 0;
    z-index: 1000;
    background: rgba(0, 0, 0, 0.55);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    animation: overlay-in 0.2s ease;
  }

  @keyframes overlay-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .modal-card {
    width: 100%;
    max-width: 480px;
    background: var(--glass-bg);
    border: 1px solid var(--header-glass-border);
    backdrop-filter: var(--glass-blur);
    -webkit-backdrop-filter: var(--glass-blur);
    border-radius: 24px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.4);
    display: flex;
    flex-direction: column;
    animation: modal-enter 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    overflow: hidden;
  }

  @keyframes modal-enter {
    from { opacity: 0; transform: translateY(16px) scale(0.97); }
    to { opacity: 1; transform: translateY(0) scale(1); }
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px 12px;
  }

  .modal-title {
    font-size: 18px;
    font-weight: 800;
    color: var(--color-text-primary);
    margin: 0;
  }

  .modal-close {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: none;
    background: rgba(0, 0, 0, 0.06);
    color: var(--color-text-secondary);
    font-size: 18px;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
  }

  .modal-close:hover {
    background: rgba(239, 68, 68, 0.12);
    color: #ef4444;
  }

  .modal-body {
    padding: 8px 24px 16px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .modal-form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .modal-label {
    font-size: 12px;
    font-weight: 700;
    color: var(--color-text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .modal-input {
    padding: 10px 14px;
    border-radius: 14px;
    border: 1px solid var(--sidebar-divider);
    background: rgba(0, 0, 0, 0.04);
    color: var(--color-text-primary);
    font-size: 14px;
    font-weight: 500;
    outline: none;
    transition: border-color 0.2s;
  }

  .modal-input:focus {
    border-color: var(--color-accent);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
  }

  .modal-hint {
    font-size: 11px;
    color: var(--color-text-tertiary);
  }

  .modal-hint code {
    font-size: 11px;
    padding: 1px 5px;
    border-radius: 4px;
    background: rgba(0, 0, 0, 0.08);
    color: var(--color-accent);
  }

  /* Modal Dropzone */
  .modal-dropzone {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 130px;
    border: 2px dashed var(--sidebar-divider);
    border-radius: 18px;
    background: rgba(0, 0, 0, 0.02);
    cursor: pointer;
    transition: all 0.25s ease;
    text-align: center;
    padding: 20px;
  }

  .modal-dropzone:hover {
    border-color: rgba(99, 102, 241, 0.4);
  }

  .modal-dropzone.dragging {
    border-color: var(--color-accent);
    background: rgba(99, 102, 241, 0.06);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  }

  .dz-icon { font-size: 30px; margin-bottom: 8px; }
  .dz-title { font-size: 13px; font-weight: 700; color: var(--color-text-primary); margin: 0 0 4px 0; }
  .dz-hint { font-size: 11px; color: var(--color-text-tertiary); margin: 0; }

  .modal-file-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    border-radius: 14px;
    background: rgba(34, 197, 94, 0.06);
    border: 1px solid rgba(34, 197, 94, 0.18);
    animation: tab-fade 0.2s ease;
  }

  .mf-info { display: flex; align-items: center; gap: 12px; }
  .mf-icon { font-size: 22px; }
  .mf-name { font-size: 13px; font-weight: 700; color: var(--color-text-primary); display: block; }
  .mf-size { font-size: 11px; color: var(--color-text-tertiary); }
  .mf-remove {
    width: 26px; height: 26px; border-radius: 50%; border: none;
    background: rgba(239, 68, 68, 0.1); color: #ef4444;
    font-size: 14px; font-weight: 700; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: background 0.2s;
  }
  .mf-remove:hover { background: rgba(239, 68, 68, 0.2); }

  .modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding: 12px 24px 20px;
  }

  .btn-modal-cancel {
    padding: 8px 18px;
    border-radius: 9999px;
    border: 1px solid var(--sidebar-divider);
    background: transparent;
    color: var(--color-text-secondary);
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
  }

  .btn-modal-import {
    padding: 8px 22px;
    border-radius: 9999px;
    border: none;
    background: linear-gradient(135deg, #a855f7, #6366f1);
    color: #fff;
    font-size: 13px;
    font-weight: 800;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s ease;
  }

  .btn-modal-import:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(168, 85, 247, 0.3);
  }

  .btn-modal-import:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
