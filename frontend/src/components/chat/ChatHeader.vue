<script setup lang="ts">
</script>

<template>
  <div class="chat-header">
    <h2>AI Chat</h2>

    <el-button>
      New Chat
    </el-button>
  </div>
</template>

<style scoped>
.chat-header {
  height: 60px;

  padding: 0 20px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  border-bottom: 1px solid var(--border-light);

  background: var(--bg-card);
}

h2 {
  font-size: 18px;
  font-weight: 600;
}
</style>