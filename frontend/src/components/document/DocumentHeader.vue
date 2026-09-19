<script setup lang="ts">
import { ArrowLeft, Upload } from '@element-plus/icons-vue'

interface KnowledgeBaseInfo {
  name: string
  description?: string
}

defineProps<{
  knowledgeBase: KnowledgeBaseInfo | null | undefined
}>()

const emit = defineEmits<{
  back: []
  upload: []
}>()
</script>

<template>
  <header class="detail-header">
    <!-- 左侧：返回 + 知识库信息 -->
    <div class="header-left">
      <el-button text @click="emit('back')">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <div v-if="knowledgeBase" class="knowledge-info">
        <h2 class="kb-name">{{ knowledgeBase.name }}</h2>
        <p class="kb-desc">
          {{ knowledgeBase.description || '暂无描述' }}
        </p>
      </div>
    </div>

    <!-- 右侧：上传文档 -->
    <el-button type="primary" @click="emit('upload')">
      <el-icon style="margin-right: 5px"><Upload /></el-icon>
      上传文档
    </el-button>
  </header>
</template>

<style scoped>
/* 头部容器：下分隔线 */
.detail-header {
  display: flex;
  align-items: center; /* ✅ 垂直居中对齐，更整齐 */
  justify-content: space-between;
  padding: 0 0 20px; /* ✅ 间距微调，更紧凑协调 */
  margin-bottom: 0; /* ✅ 移除额外间距，由分隔线自然分隔 */
  border-bottom: 1px solid var(--el-border-color-lighter);
}

/* 左侧区域：返回 + 信息横向排列 */
.header-left {
  display: flex;
  align-items: center; /* ✅ 垂直居中，与按钮对齐更自然 */
  gap: 16px; /* ✅ 统一全局间距标准 */
}

/* 知识库信息区 */
.knowledge-info {
  line-height: 1.5;
  padding-top: 0; /* ✅ 移除微调偏移，对齐更精准 */
}

/* 知识库名称：页面主标题 */
.kb-name {
  margin: 0 0 6px;
  font-size: 22px; /* ✅ 略缩小，与全局标题层级协调 */
  font-weight: 600;
  color: var(--el-text-color-primary);
  line-height: 1.3; /* ✅ 更舒适的行高 */
}

/* 知识库描述：弱化显示 */
.kb-desc {
  margin: 0;
  font-size: 14px;
  color: var(--el-text-color-secondary);
  line-height: 1.5;
}
</style>
