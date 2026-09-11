<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

import KnowledgeHeader from '@/components/knowledge/KnowledgeHeader.vue'
import KnowledgeList from '@/components/knowledge/KnowledgeList.vue'
import KnowledgeFormDialog from '@/components/knowledge/KnowledgeFormDialog.vue'
import { useKnowledgeBaseStore } from '@/stores/knowledgeBase'
import type { CreateKnowledgeBaseData, UpdateKnowledgeBaseData } from '@/types/knowledgeBase'

const knowledgeBaseStore = useKnowledgeBaseStore()

// 📌 弹窗状态
const dialogVisible = ref(false)

// 📌 当前是否编辑模式
const isEdit = ref(false)

// 📌 当前编辑的知识库 ID
const editingId = ref<number | null>(null)

// 📌 表单初始数据
const formData = reactive({
  name: '',
  description: '',
})

// 📌 页面初始化时获取知识库
const fetchKnowledgeBases = async () => {
  try {
    await knowledgeBaseStore.fetchKnowledgeBases()
  } catch (error) {
    console.error(error)
    ElMessage.error('知识库加载失败')
  }
}

// 创建
const handleCreate = () => {
  console.log('点击了新建知识库')
  isEdit.value = false
  editingId.value = null

  formData.name = ''
  formData.description = ''

  dialogVisible.value = true
}

// 编辑
const handleEdit = (id: number) => {
  console.log('编辑知识库:', id)
  const knowledgeBase = knowledgeBaseStore.knowledgeBases.find((v) => v.id === id)

  if (!knowledgeBase) return

  isEdit.value = true
  editingId.value = id

  formData.name = knowledgeBase.name
  formData.description = knowledgeBase.description

  dialogVisible.value = true
}

// 提交
const handleSubmit = async (data: CreateKnowledgeBaseData | UpdateKnowledgeBaseData) => {
  try {
    if (isEdit.value && editingId.value !== null) {
      await knowledgeBaseStore.updateKnowledgeBase(editingId.value, data)

      ElMessage.success('知识库更新成功')
    } else {
      await knowledgeBaseStore.createKnowledgeBase(data)

      ElMessage.success('知识库创建成功')
    }
    dialogVisible.value = false
  } catch (error) {
    console.error(error)
    ElMessage.error('操作失败，请稍后重试')
  }
}

// 删除
const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('删除后，该知识库将无法继续使用。确定要删除吗？', '删除知识库', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await knowledgeBaseStore.deleteKnowledgeBase(id)
    ElMessage.success('删除成功')
  } catch (error) {
    // 用户主动点击取消，不属于异常
    if (error === 'cancel' || error === 'close') {
      return
    }
    console.error(error)
    ElMessage.error('删除失败，请稍后重试')
  }
}

onMounted(() => {
  fetchKnowledgeBases()
})
</script>

<template>
  <div class="knowledge-page">
    <KnowledgeHeader @create="handleCreate" />

    <KnowledgeList
      :items="knowledgeBaseStore.knowledgeBases"
      :loading="knowledgeBaseStore.loading"
      @edit="handleEdit"
      @delete="handleDelete"
    />

    <KnowledgeFormDialog
      v-model="dialogVisible"
      :is-edit="isEdit"
      :initial-data="formData"
      @submit="handleSubmit"
    />
  </div>
</template>

<style scoped>
.knowledge-page {
  height: 100%;
  padding: 24px;
  box-sizing: border-box;
  overflow-y: auto;
}
</style>
