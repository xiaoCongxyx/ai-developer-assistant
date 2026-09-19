<script setup lang="ts">
import type { KnowledgeBase } from '@/types/knowledgeBase'
import KnowledgeCard from './KnowledgeCard.vue'

defineProps<{
  items: KnowledgeBase[]
  loading: boolean
}>()

const emit = defineEmits<{
  edit: [id: number]
  delete: [id: number]
}>()
</script>

<template>
  <div v-loading="loading" element-loading-text="加载中..." class="knowledge-list-wrapper">
    <!-- 空状态 -->
    <el-empty
      v-if="!loading && items.length === 0"
      description="暂无知识库，点击「新建知识库」开始创建"
    />

    <!-- 流式卡片网格 -->
    <div v-else class="knowledge-list">
      <KnowledgeCard
        v-for="item in items"
        :key="item.id"
        :item="item"
        @edit="emit('edit', $event)"
        @delete="emit('delete', $event)"
      />
    </div>
  </div>
</template>

<style scoped>
/* 容器：预留最小高度、避免空状态抖动 */
.knowledge-list-wrapper {
  min-height: 320px;
  margin-bottom: 28px;
}

/* 响应式网格：自动填充、最小280px、等宽拉伸 */
.knowledge-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px; /* ✅ 与全局间距统一、疏密更舒适 */
}

/* ✅ 适配小屏幕：≤640px 单列显示 */
@media (max-width: 640px) {
  .knowledge-list {
    grid-template-columns: minmax(240px, 1fr);
    gap: 16px;
  }
}
</style>
