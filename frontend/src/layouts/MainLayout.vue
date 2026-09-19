<script setup lang="ts">
import Header from '@/components/layout/Header.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
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
/* 全局布局容器：占满视口、不溢出 */
.main-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--el-bg-color-page);
}

/* 中间容器：Sidebar + 主内容横向排列 */
.container {
  flex: 1;
  display: flex;
  min-height: 0; /* ✅ 关键：解决 flex 子内容溢出问题 */
}

/* 主内容区：自适应、可滚动、统一内边距 */
.main-content {
  flex: 1;
  min-height: 0;
  padding: 24px 28px; /* 全局统一页面内边距 */
  background: var(--el-bg-color-page); /* ✅ 明暗自动适配 */
  overflow-y: auto;
}

/* ✅ 滚动条全局统一 */
.main-content::-webkit-scrollbar {
  width: 6px;
}
.main-content::-webkit-scrollbar-thumb {
  background: var(--el-border-color-darker);
  border-radius: 3px;
}
.main-content::-webkit-scrollbar-track {
  background: transparent;
}
</style>
