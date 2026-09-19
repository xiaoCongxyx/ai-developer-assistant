<script setup lang="ts">
import type { KnowledgeBase } from '@/types/knowledgeBase'
import { formatDateTime } from '@/utils/format'
import { ArrowDown, Clock, Delete, Edit } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const props = defineProps<{
  item: KnowledgeBase
}>()

const emit = defineEmits<{
  edit: [id: number]
  delete: [id: number]
}>()

const router = useRouter()

// 跳转详情页（按路由名解耦，路径变更无需改这里）
const handleOpen = () => {
  router.push({
    name: 'KnowledgeDetail',
    params: { id: props.item.id },
  })
}
</script>

<template>
  <el-card class="knowledge-card" shadow="hover" @click="handleOpen">
    <!-- 头部：名称/描述 + 操作菜单 -->
    <div class="card-header">
      <div class="card-info">
        <h3 class="card-title">{{ item.name }}</h3>
        <p class="card-desc">
          {{ item.description || '暂无描述' }}
        </p>
      </div>

      <!-- 下拉操作：双重阻止冒泡 → 不触发卡片跳转 -->
      <el-dropdown @click.stop trigger="click">
        <el-button @click.stop text class="action-btn">
          操作
          <el-icon class="el-icon--right"><ArrowDown /></el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="emit('edit', item.id)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-dropdown-item>
            <el-dropdown-item divided class="danger-action" @click="emit('delete', item.id)">
              <el-icon><Delete /></el-icon>
              删除
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

    <!-- 底部：创建时间 -->
    <div class="card-footer">
      <el-icon class="footer-icon"><Clock /></el-icon>
      创建时间：{{ formatDateTime(item.created_at) }}
    </div>
  </el-card>
</template>

<style scoped>
/* 卡片容器：统一规格、hover 动效 */
.knowledge-card {
  min-height: 160px;
  padding: 20px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid var(--el-border-color-lighter);
  background: var(--el-bg-color);
}

/* hover 反馈：边框变色 + 轻微上浮 */
.knowledge-card:hover {
  border-color: var(--el-color-primary-light-5);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
}

/* 头部布局 */
.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

/* 信息区：防止挤压、优先收缩 */
.card-info {
  min-width: 0;
  flex: 1;
}

/* 标题：单行省略、层级清晰 */
.card-title {
  margin: 0 0 8px;
  font-size: 16px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--el-text-color-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 描述：最多两行省略、明暗适配 */
.card-desc {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: var(--el-text-color-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* 操作按钮：柔和 hover */
.action-btn {
  color: var(--el-text-color-secondary);
  padding: 4px 8px;
  font-size: 14px;
  border-radius: 6px;
}
.action-btn:hover {
  color: var(--el-color-primary);
  background-color: var(--el-color-primary-light-9);
}

/* 删除项：红色警示 */
:deep(.danger-action) {
  color: var(--el-color-danger);
}

/* 底部分隔线 + 时间 */
.card-footer {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color-lighter);
  color: var(--el-text-color-secondary);
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.footer-icon {
  font-size: 14px;
  opacity: 0.75;
}
</style>
