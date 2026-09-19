<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'

defineEmits<{
  create: []
}>()
</script>

<template>
  <div class="knowledge-header">
    <div class="header-left">
      <h2 class="header-title">知识库管理</h2>
      <p class="header-desc">管理你的知识库，上传文档构建专属知识问答</p>
    </div>
    <el-button type="primary" @click="$emit('create')">
      <el-icon style="margin-right: 5px"><Plus /></el-icon>
      新建知识库
    </el-button>
  </div>
</template>

<style scoped>
.knowledge-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
  padding: 20px 24px;
  background: var(--el-bg-color);
  border-radius: 12px;
  border: 1px solid var(--el-border-color-lighter); /* ✅ 增加细边框、层次更清晰 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04); /* ✅ 柔和阴影、与卡片统一 */
}

.header-left {
  line-height: 1.4;
}

.header-title {
  margin: 0 0 6px;
  font-size: 20px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.header-desc {
  margin: 0;
  font-size: 14px;
  color: var(--el-text-color-secondary);
  line-height: 1.5; /* ✅ 行高微调、阅读更舒适 */
}
</style>
