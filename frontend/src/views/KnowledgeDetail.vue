<script setup lang="ts">
import { useDocumentStore } from '@/stores/document'
import { useKnowledgeBaseStore } from '@/stores/knowledgeBase'
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
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

// 文档处理状态轮询定时器
// 📌 必懂：保存定时器 ID，后续才能停止轮询。
const pollingTimer = ref<ReturnType<typeof setInterval> | null>(null)
// 防止重复启动轮询
const polling = ref(false)
// 轮询间隔：3 秒
const POLLING_INTERVAL = 3000

// 从 URL 获取知识库ID
const knowledgeBaseId = computed(() => {
  const val = Number(route.params.id)
  return val
})

// 当前知识库详情
const knowledgeBase = computed(() =>
  knowledgeBaseStore.knowledgeBases.find((item) => item.id === knowledgeBaseId.value),
)

/**
 * 停止文档处理状态轮询
 * 统一清理轮询定时器，防止内存泄漏
 * 所有停止逻辑统一调用这个方法，避免遗漏清理定时器。
 */
const stopPolling = () => {
  if (pollingTimer.value !== null) {
    clearInterval(pollingTimer.value)
    pollingTimer.value = null
  }
  polling.value = false
}

/**
 * 启动轮询：仅在有处理中任务时运行
 * 开始轮询文档处理状态
 * 上传接口成功只代表文件已上传，
 * 不代表文档已经完成解析、分块、向量化和入库。
 * 这是典型的异步任务状态同步场景。
 */
const startPolling = () => {
  // 知识库 ID 无效时，不启动轮询
  if (!knowledgeBaseId.value) {
    return
  }

  // 已经在轮询时，不重复创建定时器
  if (polling.value) {
    return
  }

  // 没有待处理文档时，不需要轮询
  if (!documentStore.hasProcessingDocuments()) {
    return
  }

  polling.value = true

  pollingTimer.value = setInterval(async () => {
    try {
      // 路由发生变化后，不再继续请求旧知识库
      if (!knowledgeBaseId.value) {
        stopPolling()
        return
      }

      await documentStore.fetchDocuments(knowledgeBaseId.value)

      // 当前知识库中的任务全部结束
      if (!documentStore.hasProcessingDocuments()) {
        stopPolling()
      }
    } catch (error) {
      console.error('[文档状态轮询失败]', error)

      // 暂时不因为一次网络异常就停止轮询。
      // 下一次轮询会尝试重新获取。
    }
  }, POLLING_INTERVAL)
}

// 返回列表
const handleBack = () => {
  router.push({ name: 'Knowledge' })
}

// 上传文档
const handleUpload = () => {
  uploadDialogVisible.value = true
}

// 提交上传文档
const handleSubmit = async (file: File) => {
  if (!knowledgeBaseId.value) {
    ElMessage.error('知识库 ID 无效，请刷新页面重试')
    return
  }

  uploading.value = true
  console.log('上传文件File ==> ：', file)
  try {
    // ========== 测试用：模拟失败 START ==========
    // 取消下面注释，就能看到失败状态和重试按钮
    // throw new Error('模拟：文件处理失败')
    // ========== 测试用：模拟失败 END ==========

    // 上传成功后 Store 已本地追加，无需重复拉取
    await documentStore.uploadDocument(knowledgeBaseId.value, file)

    ElMessage.success('文档上传成功，正在处理索引...')
    uploadDialogVisible.value = false

    // 重新获取服务端数据，确保状态是最新的
    await documentStore.fetchDocuments(knowledgeBaseId.value)

    // 如果存在 pending / processing 文档，则启动轮询
    startPolling()
  } catch (err) {
    console.error('[上传文档失败]', err)
    ElMessage.error('文档上传或处理失败')

    // 👉 手动把最新一条文档改成失败状态 测试用：模拟失败
    // const lastDoc = documentStore.documents.at(-1)
    // if (lastDoc) {
    //   lastDoc.status = 'failed'
    //   lastDoc.error_message = err instanceof Error ? err.message : '未知错误'
    // }

    // ElMessage.error('上传失败，请重试')
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

const handleRetry = async (documentId: number) => {
  if (!knowledgeBaseId.value) return

  try {
    await documentStore.retryDocument(knowledgeBaseId.value, documentId)

    ElMessage.success('已重新提交文档处理任务')
    // 重启轮询确保状态实时同步
    stopPolling()
    await documentStore.fetchDocuments(knowledgeBaseId.value)
    startPolling()
  } catch (error) {
    console.error('文档重试失败:', error)

    ElMessage.error('文档重试失败，请稍后再试')

    await documentStore.fetchDocuments(knowledgeBaseId.value)
  }
}

// 路由 ID 变化时重新加载
watch(
  () => route.params.id,
  async () => {
    // 切换知识库前，先清理旧知识库的轮询
    stopPolling()

    await initialize()
  },
)

onMounted(() => {
  initialize()
})

// 🏢 企业实践：组件卸载时必须清理定时器
onUnmounted(() => {
  stopPolling()
})
</script>

<template>
  <div class="knowledge-detail-page">
    <!-- 加载骨架屏 -->
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
          @retry="handleRetry"
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
