<script setup lang="ts">
import type { KnowledgeBase } from '@/types/knowledgeBase'

defineProps<{
  item: KnowledgeBase
}>()

const emit = defineEmits<{
  edit: [id: number]
  delete: [id: number]
}>()
</script>

<template>
  <el-card class="knowledge-card" shadow="hover">
    <div class="card-header">
      <div class="card-info">
        <h3>{{ item.name }}</h3>

        <p>
          {{ item.description || '暂无描述' }}
        </p>
      </div>

      <el-dropdown>
        <el-button text> 操作 </el-button>

        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="emit('edit', item.id)"> 编辑 </el-dropdown-item>

            <el-dropdown-item divided class="danger-action" @click="emit('delete', item.id)">
              删除
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

    <div class="card-footer">创建时间：{{ item.created_at }}</div>
  </el-card>
</template>

<style scoped>
.knowledge-card {
  min-height: 160px;
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}
:deep(.danger-action) {
  color: var(--el-color-danger);
}

.card-info {
  min-width: 0;
}

.card-info h3 {
  margin: 0 0 8px;
  font-size: 16px;
  font-weight: 600;
}

.card-info p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

.card-footer {
  margin-top: 24px;
  padding-top: 12px;
  border-top: 1px solid var(--border-light);
  color: var(--text-secondary);
  font-size: 12px;
}
</style>
