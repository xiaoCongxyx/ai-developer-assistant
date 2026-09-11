<script setup lang="ts">
defineEmits<{
  create: []
}>()
</script>

<template>
  <div class="knowledge-header">
    <div>
      <h2>Knowledge Base</h2>
      <p>管理你的知识库</p>
    </div>

    <el-button type="primary" @click="$emit('create')"> 新建知识库 </el-button>
  </div>
</template>

<style scoped>
.knowledge-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.knowledge-header h2 {
  margin: 0 0 6px;
  font-size: 20px;
  font-weight: 600;
}

.knowledge-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
}
</style>
