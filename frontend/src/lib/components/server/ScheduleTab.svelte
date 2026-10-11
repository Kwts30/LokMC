<!--
  LokMC — ScheduleTab
  Automated scheduled cron tasks, task toggles, and countdown timers.
-->
<script lang="ts">
  let {
    schedules = $bindable([]),
    onAddTask = () => {}
  }: {
    schedules: any[];
    onAddTask: () => void;
  } = $props();
</script>

<section class="view-card">
  <div class="card-header-flex">
    <div>
      <h2 class="section-heading">Scheduled Automations</h2>
      <p class="section-subheading">Cron tasks, scheduled backup sweeps, and restart windows.</p>
    </div>
    <button class="btn-glass-action" onclick={onAddTask}>
      + Add Scheduled Task
    </button>
  </div>

  <div class="schedules-grid">
    {#each schedules as item}
      <div class="schedule-card" class:disabled={!item.enabled}>
        <div class="schedule-top">
          <div>
            <h3 class="schedule-name">{item.name}</h3>
            <span class="cron-badge"><code>{item.cron}</code> • Next: {item.nextRun}</span>
          </div>
          <label class="switch-toggle" aria-label="Toggle task {item.name}">
            <input type="checkbox" bind:checked={item.enabled} />
            <span class="switch-slider"></span>
          </label>
        </div>
        <p class="schedule-task-desc">{item.task}</p>
      </div>
    {/each}
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

  .schedules-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }

  .schedule-card {
    background: rgba(0, 0, 0, 0.02);
    border: 1px solid var(--sidebar-divider);
    border-radius: 20px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    transition: opacity 0.2s ease, background 0.2s ease;
  }

  .schedule-card.disabled {
    opacity: 0.6;
  }

  .schedule-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .schedule-name {
    font-size: 15px;
    font-weight: 700;
    color: var(--color-text-primary);
    margin: 0 0 4px 0;
  }

  .cron-badge {
    font-size: 11px;
    color: var(--color-text-tertiary);
  }

  .cron-badge code {
    background: rgba(0, 0, 0, 0.04);
    padding: 1px 4px;
    border-radius: 4px;
    font-family: var(--font-mono);
  }

  .schedule-task-desc {
    font-size: 12px;
    color: var(--color-text-secondary);
    margin: 0;
  }

  .switch-toggle {
    position: relative;
    display: inline-block;
    width: 42px;
    height: 24px;
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

  @media (max-width: 900px) {
    .schedules-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
