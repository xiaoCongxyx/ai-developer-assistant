<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'

import { usePromptStore } from '@/stores/prompt'
import PromptList from '@/components/prompt/PromptList.vue'
import PromptFormDialog from '@/components/prompt/PromptFormDialog.vue'
import type { Prompt } from '@/types/prompt'
import { ElMessage, ElMessageBox } from 'element-plus'

const promptStore = usePromptStore()

const { prompts, loading } = storeToRefs(promptStore)

const dialogVisible = ref(false)

const editingPrompt = ref<Prompt | null>(null)

const handleEdit = (prompt: Prompt) => {
  console.log('当前编辑 Prompt：', prompt)
  editingPrompt.value = prompt
  dialogVisible.value = true
}

const handleDelete = async (prompt: Prompt) => {
  if (prompt.is_default) {
    ElMessage.warning('默认 Prompt 不能删除，请先设置其他 Prompt 为默认')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除 Prompt「${prompt.name}」吗？删除后无法恢复。`,
      '删除 Prompt',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
      },
    )

    await promptStore.deletePrompt(prompt.id)

    ElMessage.success('删除成功')
  } catch (error) {
    // 用户点击取消时，不需要提示错误
    if (error === 'cancel' || error === 'close') {
      return
    }

    console.error('删除 Prompt 失败：', error)
    ElMessage.error('Prompt 删除失败，请稍后重试')
  }
}

const handleSetDefault = async (prompt: Prompt) => {
  if (prompt.is_default) return

  try {
    await promptStore.setDefaultPrompt(prompt.id)
    ElMessage.success(`「${prompt.name}」已设为默认 Prompt`)
  } catch (error) {
    console.error('设置默认 Prompt 失败：', error)
    ElMessage.error('设置默认 Prompt 失败，请稍后重试')
  }
}

const handleCreate = () => {
  editingPrompt.value = null
  dialogVisible.value = true
}

onMounted(() => {
  promptStore.fetchPrompts()
})
</script>

<template>
  <div class="prompt-view">
    <div class="page-header">
      <div class="header-left">
        <h2>Prompt 管理</h2>
        <p>管理 AI Assistant 使用的系统 Prompt</p>
      </div>
      <el-button type="primary" @click="handleCreate"> 新建 Prompt </el-button>
    </div>

    <PromptList
      :prompts="prompts"
      :loading="loading"
      @edit="handleEdit"
      @delete="handleDelete"
      @set-default="handleSetDefault"
    />

    <PromptFormDialog :prompt="editingPrompt" v-model="dialogVisible" />
  </div>
</template>

<style scoped>
.prompt-view {
  height: 100%;
  padding: 24px 28px;
  box-sizing: border-box;
  overflow-y: auto;
  background: var(--el-bg-color-page);
}

/* 页面头部 */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.header-left h2 {
  margin: 0 0 6px;
  font-size: 20px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.header-left p {
  margin: 0;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

/* 滚动条适配明暗 */
.prompt-view::-webkit-scrollbar {
  width: 6px;
}
.prompt-view::-webkit-scrollbar-thumb {
  background: var(--el-border-color-darker);
  border-radius: 3px;
}
.prompt-view::-webkit-scrollbar-track {
  background: transparent;
}
</style>
