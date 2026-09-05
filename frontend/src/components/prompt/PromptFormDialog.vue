<script setup lang="ts">
import { usePromptStore } from '@/stores/prompt'
import { ElMessage } from 'element-plus'
import { reactive, ref } from 'vue'

const promptStore = usePromptStore()

const submitting = ref(false)
const visible = defineModel<boolean>()

const form = reactive({
  name: '',
  description: '',
  content: '',
})

async function handleSubmit() {
  if (!form.name.trim()) {
    ElMessage.warning('请输入 Prompt 名称')
    return
  }
  if (!form.content.trim()) {
    ElMessage.warning('请输入 Prompt 内容')
    return
  }

  submitting.value = true

  try {
    await promptStore.createPrompt({
      name: form.name.trim(),
      description: form.description.trim(),
      content: form.content.trim(),
    })

    ElMessage.success('Prompt 创建成功')
    visible.value = false
    submitting.value = false
  } catch (error) {
    console.error('创建 Prompt 失败：', error)

    ElMessage.error('Prompt 创建失败')
  } finally {
    submitting.value = false
  }
}

function handleCancel() {
  visible.value = false
}
</script>

<template>
  <el-dialog
    v-model="visible"
    title="新建 Prompt"
    width="640px"
    class="prompt-form-dialog"
    destroy-on-close
  >
    <el-form :model="form" label-position="top" class="prompt-form">
      <!-- 名称 -->
      <el-form-item label="名称">
        <el-input
          v-model="form.name"
          placeholder="例如：代码助手"
          maxlength="100"
          show-word-limit
        />
      </el-form-item>

      <!-- 描述 -->
      <el-form-item label="描述">
        <el-input
          v-model="form.description"
          placeholder="简单描述这个 Prompt 的用途"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <!-- Prompt 内容 -->
      <el-form-item label="Prompt 内容">
        <el-input
          v-model="form.content"
          type="textarea"
          :rows="12"
          placeholder="请输入系统 Prompt 内容..."
          resize="vertical"
          class="prompt-content-input"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleCancel"> 取消 </el-button>

        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          创建 Prompt
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.prompt-form {
  padding-top: 8px;
}

.prompt-form :deep(.el-form-item) {
  margin-bottom: 20px;
}

.prompt-form :deep(.el-form-item:last-child) {
  margin-bottom: 0;
}

.prompt-form :deep(.el-form-item__label) {
  margin-bottom: 8px;
  font-weight: 500;
}

.prompt-form :deep(.el-input__wrapper) {
  min-height: 40px;
}

.prompt-content-input :deep(.el-textarea__inner) {
  min-height: 240px !important;

  padding: 12px;

  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace;

  font-size: 13px;
  line-height: 1.6;

  resize: vertical;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
