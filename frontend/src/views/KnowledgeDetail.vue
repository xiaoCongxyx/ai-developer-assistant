<script setup lang="ts">
import { useDocumentStore } from '@/stores/document'
import { useKnowledgeBaseStore } from '@/stores/knowledgeBase'
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DocumentHeader from '@/components/document/DocumentHeader.vue'
import DocumentList from '@/components/document/DocumentList.vue'
import DocumentUploadDialog from '@/components/document/DocumentUploadDialog.vue'

const knowledgeBaseStore = useKnowledgeBaseStore()
const documentStore = useDocumentStore()
const route = useRoute()
const router = useRouter()

const uploadDialogVisible = ref(false)
const uploading = ref(false)
const initializing = ref(false) // 页面初始化加载状态

// 从 URL 获取知识库ID
const knowledgeBaseId = computed(() => {
  const val = Number(route.params.id)
  return val
})

// 当前知识库详情
const knowledgeBase = computed(() =>
  knowledgeBaseStore.knowledgeBases.find((item) => item.id === knowledgeBaseId.value),
)

// 返回列表
const handleBack = () => {
  router.push({ name: 'Knowledge' })
}

// 上传文档
const handleUpload = () => {
  uploadDialogVisible.value = true
}

const handleSubmit = async (file: File) => {
  if (!knowledgeBaseId.value) {
    ElMessage.error('知识库 ID 无效，请刷新页面重试')
    return
  }

  uploading.value = true
  console.log('上传文件File ==> ：', file)
  try {
    // 上传成功后 Store 已本地追加，无需重复拉取
    await documentStore.uploadDocument(knowledgeBaseId.value, file)

    ElMessage.success('文档上传成功，正在处理索引...')
    uploadDialogVisible.value = false

    await documentStore.fetchDocuments(knowledgeBaseId.value)
  } catch (error) {
    console.error(error)
    ElMessage.error('文档上传或处理失败')
  } finally {
    uploading.value = false
  }
}

// 初始化数据
const initialize = async () => {
  if (!knowledgeBaseId.value) {
    ElMessage.error('知识库 ID 无效')
    await router.replace({ name: 'Knowledge' })
    return
  }

  initializing.value = true
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
  } finally {
    initializing.value = false
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

// 路由 ID 变化时重新加载
watch(
  () => route.params.id,
  () => {
    initialize()
  },
)

onMounted(() => {
  initialize()
})
</script>

<template>
  <div class="knowledge-detail-page">
    <!-- 加载状态 -->
    <div v-if="initializing" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>

    <div v-else>
      <DocumentHeader :knowledge-base="knowledgeBase" @back="handleBack" @upload="handleUpload" />
      <section class="document-section">
        <DocumentList
          :items="documentStore.documents"
          :loading="documentStore.loading"
          @delete="handleDeleteDocument"
        />
        <DocumentUploadDialog
          v-model="uploadDialogVisible"
          :submitting="uploading"
          @submit="handleSubmit"
        />
      </section>
    </div>
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

.loading-container {
  padding: 32px;
}

.document-section {
  padding-top: 24px;
}
</style>
