<!--
  LokMC — ConfigTab
  Visual gameplay rules, sliders, and toggle cards.
-->
<script lang="ts">
  let {
    config = $bindable(),
    onSave = () => {}
  }: {
    config: any;
    onSave: () => void;
  } = $props();
</script>

<section class="view-card">
  <div class="card-header-flex">
    <div>
      <h2 class="section-heading">Gameplay Rules & World Options</h2>
      <p class="section-subheading">Visual toggle controls for game dynamics and spawn behaviors.</p>
    </div>
    <button class="btn-glass-action btn-primary-glass" onclick={onSave}>
      Save Config
    </button>
  </div>

  <div class="config-settings-grid">
    <!-- Game Mode -->
    <div class="config-block">
      <label for="cfg-gm" class="config-label">DEFAULT GAME MODE</label>
      <select id="cfg-gm" class="glass-select" bind:value={config.gamemode}>
        <option value="survival">Survival</option>
        <option value="creative">Creative</option>
        <option value="adventure">Adventure</option>
        <option value="spectator">Spectator</option>
      </select>
    </div>

    <!-- Difficulty -->
    <div class="config-block">
      <label for="cfg-diff" class="config-label">DIFFICULTY</label>
      <select id="cfg-diff" class="glass-select" bind:value={config.difficulty}>
        <option value="peaceful">Peaceful</option>
        <option value="easy">Easy</option>
        <option value="normal">Normal</option>
        <option value="hard">Hard</option>
      </select>
    </div>

    <!-- Sliders -->
    <div class="config-block">
      <div class="slider-label-row">
        <span class="config-label">MAX PLAYERS</span>
        <span class="slider-val">{config.maxPlayers}</span>
      </div>
      <input type="range" min="1" max="100" class="glass-slider" bind:value={config.maxPlayers} />
    </div>

    <div class="config-block">
      <div class="slider-label-row">
        <span class="config-label">VIEW DISTANCE (CHUNKS)</span>
        <span class="slider-val">{config.viewDistance}</span>
      </div>
      <input type="range" min="4" max="32" class="glass-slider" bind:value={config.viewDistance} />
    </div>
  </div>

  <div class="toggles-grid-row">
    <label class="toggle-card">
      <input type="checkbox" bind:checked={config.pvp} />
      <div class="toggle-card-body">
        <span class="t-title">Player vs Player (PvP)</span>
        <span class="t-desc">Allows damage between players</span>
      </div>
    </label>

    <label class="toggle-card">
      <input type="checkbox" bind:checked={config.flight} />
      <div class="toggle-card-body">
        <span class="t-title">Allow Flight</span>
        <span class="t-desc">Permits flight in survival</span>
      </div>
    </label>

    <label class="toggle-card">
      <input type="checkbox" bind:checked={config.nether} />
      <div class="toggle-card-body">
        <span class="t-title">Nether Dimension</span>
        <span class="t-desc">Enables portals and hell world</span>
      </div>
    </label>

    <label class="toggle-card">
      <input type="checkbox" bind:checked={config.onlineMode} />
      <div class="toggle-card-body">
        <span class="t-title">Online Mode (Mojang Auth)</span>
        <span class="t-desc">Verifies accounts with Mojang</span>
      </div>
    </label>
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

  .btn-primary-glass {
    background: var(--color-accent);
    color: #fff;
    border-color: transparent;
  }

  .btn-primary-glass:hover {
    background: var(--color-accent-hover);
  }

  .config-settings-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }

  .config-block {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .config-label {
    font-size: 10px;
    font-weight: 700;
    color: var(--color-text-tertiary);
    letter-spacing: 0.05em;
  }

  .glass-select {
    background: rgba(0, 0, 0, 0.04);
    border: 1px solid var(--sidebar-divider);
    border-radius: 12px;
    padding: 9px 14px;
    font-size: 13px;
    color: var(--color-text-primary);
    outline: none;
    cursor: pointer;
    color-scheme: dark;
  }

  :global([data-theme='light']) .glass-select {
    color-scheme: light;
  }

  .glass-select option {
    background-color: #1a1d2a;
    color: #e8eaf0;
    padding: 8px 12px;
  }

  :global([data-theme='light']) .glass-select option {
    background-color: #ffffff;
    color: #121316;
  }


  .slider-label-row {
    display: flex;
    justify-content: space-between;
  }

  .slider-val {
    font-size: 12px;
    font-weight: 700;
    color: var(--color-text-primary);
  }

  .glass-slider {
    width: 100%;
    accent-color: var(--color-accent);
  }

  .toggles-grid-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
  }

  .toggle-card {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px;
    border-radius: 16px;
    background: rgba(0, 0, 0, 0.02);
    border: 1px solid var(--sidebar-divider);
    cursor: pointer;
  }

  .toggle-card input {
    margin-top: 4px;
    accent-color: #22c55e;
  }

  .toggle-card-body {
    display: flex;
    flex-direction: column;
  }

  .t-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--color-text-primary);
  }

  .t-desc {
    font-size: 11px;
    color: var(--color-text-tertiary);
  }

  @media (max-width: 1200px) {
    .config-settings-grid {
      grid-template-columns: repeat(2, 1fr);
    }

    .toggles-grid-row {
      grid-template-columns: repeat(2, 1fr);
    }
  }
</style>
