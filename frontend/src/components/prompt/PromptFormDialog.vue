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

// ✅ 完整验证规则（含去空格校验）
const rules: FormRules = {
  name: [
    { required: true, message: '请输入 Prompt 名称', trigger: 'blur' },
    { min: 1, max: 100, message: '名称长度 1-100 字符', trigger: 'blur' },
    {
      validator: (_, val: string) => !!val.trim(),
      message: 'Prompt 名称不能为空',
      trigger: 'blur',
    },
  ],
  description: [{ max: 500, message: '描述不能超过 500 字符', trigger: 'blur' }],
  content: [
    { required: true, message: '请输入 Prompt 内容', trigger: 'blur' },
    {
      validator: (_, val: string) => !!val.trim(),
      message: 'Prompt 内容不能为空',
      trigger: 'blur',
    },
  ],
}

// 回填表单
function fillForm(prompt: Prompt) {
  form.name = prompt.name
  form.description = prompt.description
  form.content = prompt.content
}

// 清空表单
function clearForm() {
  form.name = ''
  form.description = ''
  form.content = ''
}

// ✅ 修复：正确的异步验证流程
async function handleSubmit() {
  if (!formRef.value) return

  // 1. 内置验证
  try {
    await formRef.value.validate()
  } catch {
    return // 验证失败，Element 已自动提示
  }

  submitting.value = true
  try {
    // 2. 统一去首尾空格
    const payload = {
      name: form.name.trim(),
      description: form.description.trim(),
      content: form.content.trim(),
    }

    // 3. 分流：新建 / 编辑
    if (isEditMode.value && props.prompt) {
      await promptStore.updatePrompt(props.prompt.id, payload)
      ElMessage.success('Prompt 更新成功')
    } else {
      await promptStore.createPrompt(payload)
      ElMessage.success('Prompt 创建成功')
    }

    visible.value = false // 成功关闭弹窗
  } catch (error) {
    console.error(isEditMode.value ? '修改失败：' : '创建失败：', error)
    ElMessage.error(isEditMode.value ? '修改失败，请稍后重试' : '创建失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

// 取消（提交中禁止取消）
function handleCancel() {
  if (submitting.value) return
  visible.value = false
}

// 重置/回填
async function resetForm() {
  await nextTick()
  formRef.value?.clearValidate()
  props.prompt ? fillForm(props.prompt) : clearForm()
}

// 打开弹窗自动重置/回填
watch(
  [() => visible.value, () => props.prompt],
  ([isVisible]) => {
    if (isVisible) resetForm()
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
        <el-button :disabled="submitting" @click="handleCancel">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          {{ submitBtnText }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
/* 表单整体间距 */
.prompt-form {
  padding-top: 4px;
}

.prompt-form :deep(.el-form-item) {
  margin-bottom: 20px;
}
.prompt-form :deep(.el-form-item:last-child) {
  margin-bottom: 0;
}

/* 标签样式 */
.prompt-form :deep(.el-form-item__label) {
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

/* 输入框基础高度 */
.prompt-form :deep(.el-input__wrapper) {
  min-height: 40px;
  border-radius: 8px;
}

/* Prompt 正文编辑器 */
.prompt-content-input :deep(.el-textarea__inner) {
  min-height: 240px;
  padding: 14px 16px;
  border-radius: 8px;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace;
  font-size: 13px;
  line-height: 1.7;
  color: var(--el-text-color-regular);
  background: var(--el-fill-color-light);
  resize: vertical;
  transition: background 0.2s ease;
}

/* 底部按钮区 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 8px;
}
</style>
