<script lang="ts">
  interface Player {
    username: string;
    uuid: string;
    ping: number;
    isOp: boolean;
    onlineTime: string;
  }

  interface Props {
    players: Player[];
    onShowToast: (msg: string) => void;
  }

  let { players = $bindable(), onShowToast }: Props = $props();

  function toggleOp(player: Player) {
    player.isOp = !player.isOp;
    onShowToast(`Updated OP status for ${player.username}`);
  }

  function kickPlayer(username: string) {
    onShowToast(`Kicked player ${username}`);
  }

  function banPlayer(username: string) {
    onShowToast(`Banned player ${username}`);
  }
</script>

<section class="view-card" aria-label="Player management">
  <div class="card-header-flex">
    <div>
      <h2 class="section-heading">Active Players & Permissions</h2>
      <p class="section-subheading">Kick, ban, operator elevation, and whitelist roster.</p>
    </div>
    <button class="btn-glass-action" onclick={() => onShowToast('Whitelist refreshed.')}>
      Whitelist Settings
    </button>
  </div>

  <div class="players-cards-grid">
    {#each players as p}
      <div class="player-card">
        <div class="player-avatar">
          <div class="mc-head">
            {p.username[0].toUpperCase()}
          </div>
        </div>
        <div class="player-info">
          <div class="p-name-row">
            <span class="p-name">{p.username}</span>
            {#if p.isOp}
              <span class="op-badge">OP</span>
            {/if}
          </div>
          <span class="p-meta">Ping: {p.ping}ms • Online: {p.onlineTime}</span>
        </div>
        <div class="player-actions">
          <button
            class="player-action-btn"
            title={p.isOp ? 'Remove OP' : 'Make OP'}
            onclick={() => toggleOp(p)}
          >
            {p.isOp ? 'De-OP' : 'OP'}
          </button>
          <button
            class="player-action-btn warn"
            onclick={() => kickPlayer(p.username)}
          >
            Kick
          </button>
          <button
            class="player-action-btn danger"
            onclick={() => banPlayer(p.username)}
          >
            Ban
          </button>
        </div>
      </div>
    {/each}
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

  .players-cards-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
  }

  .player-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 18px;
    border-radius: 18px;
    background: rgba(0, 0, 0, 0.02);
    border: 1px solid var(--sidebar-divider);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .player-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  }

  :global([data-theme='dark']) .player-card {
    background: rgba(255, 255, 255, 0.03);
    border-color: rgba(255, 255, 255, 0.08);
  }

  .mc-head {
    width: 38px;
    height: 38px;
    border-radius: 8px;
    background: #6366f1;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 16px;
  }

  .player-info {
    flex: 1;
  }

  .p-name-row {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .p-name {
    font-size: 14px;
    font-weight: 700;
    color: var(--color-text-primary);
  }

  .op-badge {
    background: rgba(234, 179, 8, 0.15);
    color: #ca8a04;
    font-size: 9px;
    font-weight: 800;
    padding: 1px 6px;
    border-radius: 4px;
  }

  .p-meta {
    font-size: 11px;
    color: var(--color-text-tertiary);
  }

  .player-actions {
    display: flex;
    gap: 6px;
  }

  .player-action-btn {
    background: none;
    border: 1px solid var(--sidebar-divider);
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    color: var(--color-text-secondary);
    transition: all 0.15s ease;
  }

  .player-action-btn:hover {
    color: var(--color-text-primary);
    border-color: var(--color-text-primary);
  }

  .player-action-btn.warn:hover {
    color: #f59e0b;
    border-color: #f59e0b;
  }

  .player-action-btn.danger:hover {
    color: #ef4444;
    border-color: #ef4444;
  }

  @media (max-width: 900px) {
    .players-cards-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
