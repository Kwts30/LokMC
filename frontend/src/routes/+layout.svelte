<!--
  LokMC — Root Layout

  Imports the design system CSS and wraps all routes.
  No shell here — the (app) layout group handles the sidebar/topbar.
-->
<script lang="ts">
  import '../styles/tokens.css';
  import '../styles/components.css';
  import '../styles/layout.css';

  let { children } = $props();
</script>

<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap"
    rel="stylesheet"
  />
</svelte:head>

{@render children()}
