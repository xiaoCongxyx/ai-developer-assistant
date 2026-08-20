<script setup lang="ts">
import Header from '@/components/layout/Header.vue'
import Sidebar from '@/components/layout/SiderBar.vue'
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
}

.container {
  flex: 1;
  display: flex;
}

.main-content {
  flex: 1;
  padding: var(--content-padding);
  background: var(--bg-page);
  overflow-y: auto;
}
</style>