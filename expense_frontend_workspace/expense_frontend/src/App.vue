<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import { ref, watch } from 'vue'
const route = useRoute()
const drawerOpen = ref(true)
watch(route, () => { /* close mobile drawer, if needed (future) */ })
</script>

<template>
  <div class="app-root">
    <aside class="sidebar" :class="{ open: drawerOpen }">
      <div class="logo-area">
        <span class="logo-icon">💸</span>
        <span class="brand-name">FinanceFlow</span>
      </div>
      <nav class="nav-links">
        <RouterLink to="/" class="nav-link" active-class="active" exact> Dashboard </RouterLink>
        <RouterLink to="/expenses" class="nav-link" active-class="active"> Expenses </RouterLink>
        <RouterLink to="/categories" class="nav-link" active-class="active"> Categories </RouterLink>
        <RouterLink to="/login" class="nav-link" active-class="active"> Login </RouterLink>
      </nav>
    </aside>
    <div class="main-view">
      <header class="topbar">
        <span class="topbar-title">
          <!-- Placeholder for contextual title -->
          <span v-if="route.name === 'dashboard'">Dashboard</span>
          <span v-else-if="route.name === 'expenses'">Expenses</span>
          <span v-else-if="route.name === 'categories'">Categories</span>
          <span v-else-if="route.name === 'login'">Sign In</span>
          <span v-else>FinanceFlow</span>
        </span>
        <span class="spacer"></span>
        <!-- Placeholder: Profile/user actions -->
        <button class="profile-btn" disabled>
          <span class="profile-avatar">👤</span>
        </button>
      </header>
      <main class="page-container">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped>
/* Theming */
:root {
  --primary: #1976d2;
  --accent: #ffb300;
  --secondary: #424242;
  --surface: #fff;
  --sidebar-bg: var(--primary);
  --sidebar-text: #fff;
  --sidebar-accent: var(--accent);
  --topbar-bg: #f7f9fc;
  --topbar-border: #e0e5ef;
  --main-bg: #fff;
}

/* Layout root */
.app-root {
  height: 100vh;
  display: flex;
  font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
  background: var(--main-bg);
}

/* Sidebar */
.sidebar {
  width: 240px;
  background: var(--sidebar-bg);
  color: var(--sidebar-text);
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px 0 rgba(33, 64, 120, 0.03);
  transition: width 0.2s;
  min-width: 200px;
}
.logo-area {
  display: flex;
  align-items: center;
  padding: 2.4rem 1rem 1rem 1.6rem;
  font-size: 1.5rem;
  font-weight: bold;
  gap: 0.7em;
}
.logo-icon {
  font-size: 2.1em;
}
.brand-name {
  letter-spacing: 0.03em;
}
.nav-links {
  display: flex;
  flex-direction: column;
  gap: 0.1em;
  margin: 2em 0;
}
.nav-link {
  color: var(--sidebar-text);
  text-decoration: none;
  padding: 0.8em 1.4em;
  border-radius: 6px 0 0 6px;
  margin-left: 0.5em;
  transition: background 0.13s, color 0.13s;
  font-size: 1.06em;
  font-weight: 500;
}
.nav-link.active,
.nav-link.router-link-active {
  background: var(--sidebar-accent);
  color: var(--secondary);
}

.main-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--main-bg);
  min-width: 0;
  min-height: 0;
}

.topbar {
  height: 56px;
  display: flex;
  align-items: center;
  background: var(--topbar-bg);
  border-bottom: 1px solid var(--topbar-border);
  padding: 0 2em;
  font-size: 1.17em;
  color: var(--primary);
  font-weight: 600;
  box-sizing: border-box;
  letter-spacing: 0.01em;
}
.spacer {
  flex: 1;
}
.profile-btn {
  background: none;
  border: none;
  cursor: pointer;
  border-radius: 50%;
  padding: 0.47em 0.8em;
  font-size: 1.2em;
  color: var(--primary);
  transition: background 0.12s;
}
.profile-avatar {
  font-size: 1.32em;
}

.page-container {
  flex: 1;
  padding: 2.4rem 2.3rem 2.2rem 2.7rem;
  background: var(--main-bg);
  overflow-y: auto;
}

/* Responsive: adapt sidebar for mobile/tablet in future */

/* Modern/minimal: avoid much chrome, subtle shadows only */

</style>
