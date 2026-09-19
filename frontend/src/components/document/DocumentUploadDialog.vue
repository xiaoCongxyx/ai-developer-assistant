<script lang="ts" setup>
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage, type UploadFile, type UploadUserFile } from 'element-plus'
import { ref, watch } from 'vue'

const props = defineProps<{
  modelValue: boolean
  submitting: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  submit: [file: File]
}>()

// 选中的原始文件
const selectedFile = ref<File | null>(null)
// 绑定 el-upload 的文件列表，手动控制清空
const fileList = ref<UploadUserFile[]>([])

const allowedExtensions = ['.pdf', '.txt', '.md']
const maxFileSize = 10 * 1024 * 1024

// 弹窗打开/关闭时：同时重置选中文件 + 展示列表
watch(
  () => props.modelValue,
  (isOpen) => {
    if (isOpen) {
      selectedFile.value = null
      fileList.value = [] // ✅ 清空展示列表
    }
  },
)

// 文件变更：校验+存储
const handleFileChange = (file: UploadFile, uploadFiles: UploadUserFile[]) => {
  // 用户删除文件时同步清空
  if (uploadFiles.length === 0) {
    selectedFile.value = null
    return
  }

  const rawFile = file.raw as File
  if (!rawFile) return

  const filename = rawFile.name.toLowerCase()
  const isAllowed = allowedExtensions.some((ext) => filename.endsWith(ext))
  if (!isAllowed) {
    ElMessage.error('仅支持 PDF、TXT、Markdown 文件')
    fileList.value = [] // 清空错误展示
    return
  }

  if (rawFile.size > maxFileSize) {
    ElMessage.error('文件大小不能超过 10 MB')
    fileList.value = [] // 清空超限展示
    return
  }

  selectedFile.value = rawFile
}

const handleClose = () => {
  if (props.submitting) return
  selectedFile.value = null
  fileList.value = [] // ✅ 手动清空
  emit('update:modelValue', false)
}

const handleSubmit = () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }
  emit('submit', selectedFile.value)
}
</script>

<template>
  <el-dialog
    :model-value="modelValue"
    title="上传文档"
    width="480px"
    :close-on-click-modal="false"
    :before-close="handleClose"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <el-upload
      v-model:file-list="fileList"
      drag
      :auto-upload="false"
      :show-file-list="true"
      :limit="1"
      accept=".pdf,.txt,.md"
      :on-change="handleFileChange"
      :on-exceed="() => ElMessage.warning('一次只能选择一个文件')"
    >
      <el-icon class="el-icon--upload">
        <UploadFilled />
      </el-icon>
      <div class="el-upload__text">将文件拖到此处，或 <em>点击选择</em></div>
      <template #tip>
        <div class="el-upload__tip">支持 PDF、TXT、Markdown，最大 10 MB</div>
      </template>
    </el-upload>

    <template #footer>
      <el-button :disabled="submitting" @click="handleClose"> 取消 </el-button>
      <el-button type="primary" :loading="submitting" @click="handleSubmit"> 开始上传 </el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.el-upload__tip {
  color: var(--text-secondary);
  font-size: 12px;
  margin-top: 8px;
}
.el-upload {
  width: 100%;
}
</style>
