<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
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
  initialData: () => ({
    name: '',
    description: '',
  }),
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  submit: [data: CreateKnowledgeBaseData | UpdateKnowledgeBaseData]
}>()

// 📌 表单引用，用于调用 Element Plus Form 校验
const formRef = ref()

// 📌 防止用户重复提交
const submitting = ref(false)

// 📌 表单数据
const form = reactive({
  name: '',
  description: '',
})

// 📌 根据当前模式动态显示标题
const dialogTitle = computed(() => (props.isEdit ? '编辑知识库' : '新建知识库'))

// 📌 表单校验规则
const rules = {
  name: [
    {
      required: true,
      message: '请输入知识库名称',
      trigger: 'blur',
    },
    {
      min: 1,
      max: 100,
      message: '知识库名称长度应为 1-100 个字符',
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
}

// 📌 弹窗打开时同步初始数据
watch(
  () => props.modelValue,
  (visible) => {
    if (!visible) {
      return
    }

    form.name = props.initialData.name
    form.description = props.initialData.description

    // 清除上一次打开弹窗时留下的校验状态
    formRef.value?.clearValidate()
  },
)

// 关闭弹窗
const handleClose = () => {
  emit('update:modelValue', false)
}

// 提交表单
const handleSubmit = async () => {
  if (submitting.value) {
    return
  }

  // 📌 提交之前先执行前端表单校验
  const valid = await formRef.value?.validate()

  if (!valid) {
    return
  }

  const data = {
    name: form.name.trim(),
    description: form.description.trim(),
  }

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
          placeholder="简单描述这个知识库的用途，例如：用于存放 Python、FastAPI 相关学习资料"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose"> 取消 </el-button>

        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          {{ isEdit ? '保存修改' : '创建知识库' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.knowledge-form {
  padding-top: 4px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

:deep(.el-form-item) {
  margin-bottom: 22px;
}

:deep(.el-form-item:last-child) {
  margin-bottom: 0;
}

:deep(.el-form-item__label) {
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-primary);
}

:deep(.el-input__wrapper) {
  min-height: 40px;
}

:deep(.el-textarea__inner) {
  line-height: 1.6;
  resize: vertical;
}
</style>
