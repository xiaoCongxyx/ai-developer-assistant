<script setup lang="ts">
import Header from '@/components/layout/Header.vue'
import Sidebar from '@/components/layout/Siderbar.vue'
</script>

<template>
  <div class="main-layout">
  <Header />

  <div class="container">
    <Sidebar />
    
    <main class="main-content">
      <router-view />
    </main>
  </div>
  </div>
</template>

<style scoped>
.main-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.container {
  flex: 1;
  display: flex;
  min-height: 0;
}

.main-content {
  flex: 1;
  min-height: 0;
  padding: var(--content-padding);
  background: var(--bg-page);
  overflow-y: auto;
}
</style>