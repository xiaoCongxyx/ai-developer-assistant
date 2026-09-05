<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'

import { usePromptStore } from '@/stores/prompt'
import PromptList from '@/components/prompt/PromptList.vue'
import PromptFormDialog from '@/components/prompt/PromptFormDialog.vue'
import type { Prompt } from '@/types/prompt'

const promptStore = usePromptStore()

const { prompts, loading } = storeToRefs(promptStore)

const dialogVisible = ref(false)

const editingPrompt = ref<Prompt | null>(null)

const handelEdit = (prompt: Prompt) => {
  console.log('当前编辑 Prompt：', prompt)
  editingPrompt.value = prompt
  dialogVisible.value = true
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
      <div>
        <h2>Prompt 管理</h2>
        <p>管理 AI Assistant 使用的系统 Prompt</p>
      </div>

      <el-button type="primary" @click="handleCreate"> 新建 Prompt </el-button>
    </div>

    <PromptList :prompts="prompts" :loading="loading" @edit="handelEdit" />

    <PromptFormDialog :prompt="editingPrompt" v-model="dialogVisible" />
  </div>
</template>

<style scoped>
.prompt-view {
  height: 100%;
  padding: 24px;
  box-sizing: border-box;
  overflow-y: auto;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0 0 8px;
  font-size: 22px;
}

.page-header p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
}
</style>
