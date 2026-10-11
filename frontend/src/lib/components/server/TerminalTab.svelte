<!--
  LokMC — TerminalTab
  Interactive live console stream, auto-scroll, command history, and quick macros.
-->
<script lang="ts">
  let {
    consoleLines = $bindable([]),
    onSendCommand = (cmd: string) => {}
  }: {
    consoleLines: string[];
    onSendCommand: (cmd: string) => void;
  } = $props();

  let commandInput = $state('');
  let commandHistory = $state<string[]>([]);
  let historyIndex = $state(-1);
  let autoScroll = $state(true);
  let consoleRef = $state<HTMLElement>();

  $effect(() => {
    if (consoleLines.length && autoScroll && consoleRef) {
      requestAnimationFrame(() => {
        if (consoleRef) {
          consoleRef.scrollTop = consoleRef.scrollHeight;
        }
      });
    }
  });

  function handleSubmit(e: Event) {
    e.preventDefault();
    const cmd = commandInput.trim();
    if (!cmd) return;

    commandHistory = [...commandHistory, cmd];
    historyIndex = commandHistory.length;
    commandInput = '';
    onSendCommand(cmd);
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'ArrowUp') {
      if (historyIndex > 0) {
        historyIndex--;
        commandInput = commandHistory[historyIndex] || '';
      }
    } else if (e.key === 'ArrowDown') {
      if (historyIndex < commandHistory.length - 1) {
        historyIndex++;
        commandInput = commandHistory[historyIndex] || '';
      } else {
        historyIndex = commandHistory.length;
        commandInput = '';
      }
    }
  }

  function setCommand(macro: string) {
    commandInput = macro;
  }
</script>

<section class="view-card terminal-card">
  <div class="terminal-toolbar">
    <div class="terminal-info">
      <span class="terminal-dot red"></span>
      <span class="terminal-dot yellow"></span>
      <span class="terminal-dot green"></span>
      <span class="terminal-title">STDOUT Console Stream — PID 4812</span>
    </div>
    <div class="terminal-actions">
      <label class="autoscroll-toggle">
        <input type="checkbox" bind:checked={autoScroll} />
        <span>Auto-scroll</span>
      </label>
      <button
        type="button"
        class="ghost-chip-btn"
        onclick={() => (consoleLines = [])}
      >
        Clear
      </button>
    </div>
  </div>

  <!-- Console Output Box -->
  <div class="terminal-screen" bind:this={consoleRef}>
    {#each consoleLines as line}
      <div
        class="console-row"
        class:row-warn={line.includes('WARN')}
        class:row-error={line.includes('ERROR')}
        class:row-cmd={line.startsWith('>')}
      >
        {line}
      </div>
    {/each}
    {#if consoleLines.length === 0}
      <div class="console-empty">Console buffer cleared. Ready for commands.</div>
    {/if}
  </div>

  <!-- Quick Command Chips -->
  <div class="quick-commands-bar">
    <span class="quick-label">QUICK MACROS:</span>
    <button class="macro-chip" onclick={() => setCommand('/tps')}>/tps</button>
    <button class="macro-chip" onclick={() => setCommand('/list')}>/list</button>
    <button class="macro-chip" onclick={() => setCommand('/save-all')}>/save-all</button>
    <button class="macro-chip" onclick={() => setCommand('/say Server announcement!')}>/say ...</button>
    <button class="macro-chip" onclick={() => setCommand('/whitelist on')}>/whitelist</button>
  </div>

  <!-- Command Input Bar -->
  <form class="terminal-prompt-form" onsubmit={handleSubmit}>
    <span class="prompt-caret">&gt;</span>
    <input
      type="text"
      class="prompt-input"
      bind:value={commandInput}
      onkeydown={handleKeydown}
      placeholder="Type a Minecraft server command (e.g. /tps, /say hello)..."
      autocomplete="off"
      spellcheck="false"
      aria-label="Minecraft console command"
    />
    <button type="submit" class="prompt-send-btn" disabled={!commandInput.trim()}>
      Send
    </button>
  </form>
</section>

<style>
  .terminal-card {
    padding: 0;
    overflow: hidden;
    background: rgba(14, 16, 22, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 28px;
    box-shadow: var(--glass-shadow);
  }

  .terminal-toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 18px;
    background: rgba(0, 0, 0, 0.3);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  }

  .terminal-info {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .terminal-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }

  .terminal-dot.red { background: #ef4444; }
  .terminal-dot.yellow { background: #f59e0b; }
  .terminal-dot.green { background: #22c55e; }

  .terminal-title {
    font-size: 12px;
    font-family: var(--font-mono);
    color: #94a3b8;
    margin-left: 6px;
  }

  .terminal-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .autoscroll-toggle {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: #94a3b8;
    cursor: pointer;
  }

  .ghost-chip-btn {
    background: rgba(255, 255, 255, 0.06);
    border: none;
    color: #cbd5e1;
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 6px;
    cursor: pointer;
  }

  .terminal-screen {
    height: 420px;
    overflow-y: auto;
    padding: 18px 20px;
    font-family: var(--font-mono);
    font-size: 13px;
    line-height: 1.6;
    color: #e2e8f0;
    display: flex;
    flex-direction: column;
    gap: 2px;
    background: transparent;
  }

  .console-row {
    word-break: break-all;
    white-space: pre-wrap;
  }

  .row-warn { color: #fcd34d; }
  .row-error { color: #f87171; }
  .row-cmd { color: #6ee7b7; font-weight: 700; }

  .console-empty {
    color: #64748b;
    font-style: italic;
    padding: 20px 0;
  }

  .quick-commands-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 18px;
    background: rgba(0, 0, 0, 0.2);
    border-top: 1px solid rgba(255, 255, 255, 0.04);
    overflow-x: auto;
  }

  .quick-label {
    font-size: 10px;
    font-weight: 700;
    color: #64748b;
    letter-spacing: 0.05em;
  }

  .macro-chip {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #93c5fd;
    font-family: var(--font-mono);
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.15s ease;
  }

  .macro-chip:hover {
    background: rgba(255, 255, 255, 0.12);
  }

  .terminal-prompt-form {
    display: flex;
    align-items: center;
    padding: 10px 18px;
    background: rgba(0, 0, 0, 0.35);
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    gap: 12px;
  }

  .prompt-caret {
    color: #4ade80;
    font-family: var(--font-mono);
    font-weight: 800;
    font-size: 16px;
  }

  .prompt-input {
    flex: 1;
    background: transparent;
    border: none;
    color: #ffffff;
    font-family: var(--font-mono);
    font-size: 13px;
    outline: none;
  }

  .prompt-input::placeholder {
    color: #64748b;
  }

  .prompt-send-btn {
    background: #3b82f6;
    color: #fff;
    border: none;
    font-size: 12px;
    font-weight: 700;
    padding: 6px 14px;
    border-radius: 8px;
    cursor: pointer;
  }

  .prompt-send-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
</style>
