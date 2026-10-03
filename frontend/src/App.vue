<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppSidebar from './components/layout/AppSidebar.vue'
</script>

<template>
  <div class="app-layout">
    <!-- Left Navigation Bar (visible across all pages) -->
    <AppSidebar />

    <!-- Main View Content -->
    <main class="main-viewport">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  width: 100vw;
  height: 100vh;
  display: flex;
  overflow: hidden;
  background-color: #f8fafc;
}

.main-viewport {
  flex: 1;
  height: 100vh;
  overflow-y: auto;
  position: relative;
}
</style>
