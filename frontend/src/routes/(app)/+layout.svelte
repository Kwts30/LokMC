<!--
  LokMC — Main Application Shell Layout
  Features the default floating glassmorphic header matching the user's design reference.
-->
<script lang="ts">
  import { page } from '$app/stores';
  import { api } from '$lib/api';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import Header from '$lib/components/Header.svelte';

  let { children } = $props();
  let userProfile: any = $state(null);

  onMount(async () => {
    if (!api.isAuthenticated) {
      try {
        const status = await api.needsSetup();
        if (status.needs_setup) {
          goto('/login');
          return;
        }
      } catch {
        // Backend daemon offline — enable fallback local session to preview UI seamlessly
        if (!localStorage.getItem('lokmc_access_token')) {
          api.setTokens('dev_demo_token', 'dev_demo_refresh');
        }
      }
    }

    try {
      userProfile = await api.getProfile();
    } catch {
      userProfile = { username: 'Administrator', is_superuser: true };
    }
  });
</script>

<div class="lokmc-app-shell">
  <!-- Default Floating Glassmorphic Header -->
  <Header />

  <!-- Main Scrollable Content Area -->
  <main class="lokmc-main-stage" id="main-content">
    {@render children()}
  </main>
</div>

<style>
  .lokmc-app-shell {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: var(--color-bg-base);
    color: var(--color-text-primary);
    position: relative;
    overflow-x: hidden;
  }

  .lokmc-main-stage {
    flex: 1;
    display: flex;
    flex-direction: column;
    width: 100%;
    box-sizing: border-box;
  }
</style>
