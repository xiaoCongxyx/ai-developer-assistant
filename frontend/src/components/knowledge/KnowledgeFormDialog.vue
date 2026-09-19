<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import type { CreateKnowledgeBaseData, UpdateKnowledgeBaseData } from '@/types/knowledgeBase'

interface Props {
  modelValue: boolean
  isEdit: boolean
  initialData?: {
    name: string
    description: string
  }
}

const props = withDefaults(defineProps<Props>(), {
  initialData: () => ({ name: '', description: '' }),
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  submit: [data: CreateKnowledgeBaseData | UpdateKnowledgeBaseData]
}>()

// ✅ 补全类型、消除 TS 警告
const formRef = ref<FormInstance>()
const submitting = ref(false)

// 表单数据
const form = reactive({
  name: '',
  description: '',
})

// 动态标题与按钮文字
const dialogTitle = computed(() => (props.isEdit ? '编辑知识库' : '新建知识库'))
const submitText = computed(() => (props.isEdit ? '保存修改' : '创建知识库'))

// ✅ 完整校验规则（含去空校验）
const rules: FormRules = {
  name: [
    { required: true, message: '请输入知识库名称', trigger: 'blur' },
    { min: 1, max: 100, message: '名称长度 1-100 字符', trigger: 'blur' },
    {
      validator: (_, val: string) => !!val.trim(),
      message: '知识库名称不能为空',
      trigger: 'blur',
    },
  ],
  description: [{ max: 500, message: '描述不能超过 500 字符', trigger: 'blur' }],
}

// ✅ 弹窗打开/数据变更时同步回填
watch(
  [() => props.modelValue, () => props.initialData],
  ([visible]) => {
    if (!visible) return
    form.name = props.initialData.name
    form.description = props.initialData.description
    formRef.value?.clearValidate() // 清除上一次残留报错
  },
  { deep: true }, // 监听对象内部变化
)

// 关闭弹窗
const handleClose = () => {
  if (submitting.value) return // 提交中禁止关闭
  emit('update:modelValue', false)
}

// ✅ 修复：正确的异步验证流程
const handleSubmit = async () => {
  if (submitting.value) return

  // 1. 执行 Element Plus 内置验证
  try {
    await formRef.value?.validate()
  } catch {
    return // 验证失败，Element 已自动提示
  }

  // 2. 清洗数据
  const data = {
    name: form.name.trim(),
    description: form.description.trim(),
  }

  // 3. 提交（交给父组件处理 API）
  submitting.value = true
  try {
    emit('submit', data)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <el-dialog
    :model-value="modelValue"
    :title="dialogTitle"
    width="520px"
    :close-on-click-modal="false"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-position="top" class="knowledge-form">
      <el-form-item label="知识库名称" prop="name">
        <el-input
          v-model="form.name"
          placeholder="例如：Python 后端开发"
          maxlength="100"
          show-word-limit
          clearable
        />
      </el-form-item>

      <el-form-item label="知识库描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="5"
          placeholder="例如：用于存放 Python、FastAPI 相关学习资料"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button :disabled="submitting" @click="handleClose">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          {{ submitText }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.knowledge-form {
  padding-top: 4px;
}

/* 表单项间距 */
:deep(.el-form-item) {
  margin-bottom: 22px;
}
:deep(.el-form-item:last-child) {
  margin-bottom: 0;
}

/* 标签统一 */
:deep(.el-form-item__label) {
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--el-text-color-primary); /* ✅ EP 变量、明暗自动适配 */
}

/* 输入框统一样式 */
:deep(.el-input__wrapper) {
  min-height: 40px;
  border-radius: 8px;
}
:deep(.el-textarea__inner) {
  line-height: 1.6;
  resize: vertical;
  border-radius: 8px;
}

/* 按钮区 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 8px;
}
</style>
