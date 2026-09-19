<script setup lang="ts">
import { useDocumentStore } from '@/stores/document'
import { useKnowledgeBaseStore } from '@/stores/knowledgeBase'
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DocumentHeader from '@/components/document/DocumentHeader.vue'
import DocumentList from '@/components/document/DocumentList.vue'

const knowledgeBaseStore = useKnowledgeBaseStore()
const documentStore = useDocumentStore()
const route = useRoute()
const router = useRouter()

// 从 URL 获取知识库ID
const knowledgeBaseId = computed(() => Number(route.params.id))

// 当前知识库详情
const knowledgeBase = computed(() =>
  knowledgeBaseStore.knowledgeBases.find((item) => item.id === knowledgeBaseId.value),
)

// 返回列表
const handleBack = () => {
  router.push({ name: 'Knowledge' })
}

// 上传文档（待后续扩展）
const handleUpload = () => {
  ElMessage.info('上传功能开发中...')
}

// 初始化数据
const initialize = async () => {
  try {
    if (knowledgeBaseStore.knowledgeBases.length === 0) {
      await knowledgeBaseStore.fetchKnowledgeBases()
    }
    if (!knowledgeBase.value) {
      ElMessage.error('知识库不存在')
      await router.replace({ name: 'Knowledge' })
      return
    }
    await documentStore.fetchDocuments(knowledgeBaseId.value)
  } catch (err) {
    console.error('[页面初始化失败]', err)
    ElMessage.error('页面加载失败，请稍后重试')
  }
}

const handleDeleteDocument = async (documentId: number) => {
  console.log('删除文档')
  try {
    await ElMessageBox.confirm(
      '删除文档后，其相关内容和向量数据也将无法继续使用，确定要删除吗？',
      '删除文档',
      {
        type: 'warning',
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
      },
    )
    await documentStore.deleteDocument(knowledgeBaseId.value, documentId)

    ElMessage.success('文档删除成功')
    await documentStore.fetchDocuments(knowledgeBaseId.value)
  } catch (error) {
    if (error === 'cancel' || error === 'close') {
      return
    }

    console.error(error)
    ElMessage.error('文档删除失败')
  }
}

onMounted(() => {
  initialize()
})
</script>

<template>
  <div class="knowledge-detail-page">
    <DocumentHeader :knowledge-base="knowledgeBase" @back="handleBack" @upload="handleUpload" />
    <section class="document-section">
      <DocumentList
        :items="documentStore.documents"
        :loading="documentStore.loading"
        @delete="handleDeleteDocument"
      />
    </section>
  </div>
</template>

<style scoped>
.knowledge-detail-page {
  height: 100%;
  padding: 28px 32px 36px;
  box-sizing: border-box;
  overflow-y: auto;
  background: var(--el-bg-color-page);
}

.document-section {
  padding-top: 24px;
}
</style>
