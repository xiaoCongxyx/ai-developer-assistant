<script setup lang="ts">
import { usePromptStore } from '@/stores/prompt'
import type { Prompt } from '@/types/prompt'
import type { FormRules, FormInstance } from 'element-plus'
import { ElMessage } from 'element-plus'
import { computed, nextTick, reactive, ref, watch } from 'vue'

const promptStore = usePromptStore()

const formRef = ref<FormInstance>()
const submitting = ref(false)
const visible = defineModel<boolean>()

const props = defineProps<{
  prompt?: Prompt | null
}>()

const form = reactive({
  name: '',
  description: '',
  content: '',
})

const isEditMode = computed(() => props.prompt !== null)

const dialogTitle = computed(() => (isEditMode.value ? '编辑 Prompt' : '新建 Prompt'))

const submitBtnText = computed(() => (isEditMode.value ? '保存修改' : '创建 Prompt'))

const rules: FormRules = {
  name: [
    {
      required: true,
      message: '请输入 Prompt 名称',
      trigger: 'blur',
    },
    {
      min: 1,
      max: 100,
      message: 'Prompt 名称长度应为 1-100 个字符',
      trigger: 'blur',
    },
  ],

  description: [
    {
      max: 500,
      message: '描述不能超过 500 个字符',
      trigger: 'blur',
    },
  ],

  content: [
    {
      required: true,
      message: '请输入 Prompt 内容',
      trigger: 'blur',
    },
  ],
}

function fillForm(prompt: Prompt) {
  form.name = prompt.name
  form.description = prompt.description
  form.content = prompt.content
}

function clearForm() {
  form.name = ''
  form.description = ''
  form.content = ''
}

async function handleSubmit() {
  if (!formRef.value) return

  const vaild = formRef.value.validate().catch(() => false)

  if (!vaild) return

  if (!form.name.trim()) {
    ElMessage.warning('Prompt 名称不能为空')
    return
  }

  if (!form.content.trim()) {
    ElMessage.warning('Prompt 内容不能为空')
    return
  }

  submitting.value = true
  try {
    if (isEditMode.value && props.prompt) {
      await promptStore.updatePrompt(props.prompt.id, {
        name: form.name.trim(),
        description: form.description.trim(),
        content: form.content.trim(),
      })

      ElMessage.success('Prompt 更新成功')
    } else {
      await promptStore.createPrompt({
        name: form.name.trim(),
        description: form.description.trim(),
        content: form.content.trim(),
      })

      ElMessage.success('Prompt 创建成功')
    }
    visible.value = false
  } catch (error) {
    console.error(isEditMode.value ? '修改 Prompt 失败：' : '创建 Prompt 失败：', error)

    ElMessage.error(
      isEditMode.value ? 'Prompt 修改失败，请稍后重试' : 'Prompt 创建失败，请稍后重试',
    )
  } finally {
    submitting.value = false
  }
}

function handleCancel() {
  if (submitting.value) return
  visible.value = false
}

async function resetForm() {
  await nextTick()

  formRef.value?.clearValidate()

  if (props.prompt) {
    fillForm(props.prompt)
  } else {
    clearForm()
  }
}

watch(
  () => [visible.value, props.prompt] as const,
  ([isVisible]) => {
    if (isVisible) {
      resetForm()
    }
  },
  { immediate: true },
)
</script>

<template>
  <el-dialog
    v-model="visible"
    :title="dialogTitle"
    width="640px"
    class="prompt-form-dialog"
    destroy-on-close
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-position="top" class="prompt-form">
      <el-form-item label="名称" prop="name">
        <el-input
          v-model="form.name"
          placeholder="例如：代码助手"
          maxlength="100"
          show-word-limit
          clearable
        />
      </el-form-item>

      <el-form-item label="描述" prop="description">
        <el-input
          v-model="form.description"
          placeholder="简单描述这个 Prompt 的用途"
          maxlength="500"
          show-word-limit
          clearable
        />
      </el-form-item>

      <el-form-item label="Prompt 内容" prop="content">
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
        <el-button :disabled="submitting" @click="handleCancel"> 取消 </el-button>

        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          {{ submitBtnText }}
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
