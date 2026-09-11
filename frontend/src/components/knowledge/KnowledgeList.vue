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
  <div v-loading="loading" class="knowledge-list-wrapper">
    <el-empty v-if="!loading && items.length === 0" description="暂无知识库" />

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
.knowledge-list-wrapper {
  min-height: 300px;
}

.knowledge-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}
</style>
