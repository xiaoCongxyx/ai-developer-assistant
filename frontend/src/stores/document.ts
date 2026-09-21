import { defineStore } from 'pinia'
import { ref } from 'vue'

import type { Document } from '@/types/document'

import { getDocuments, deleteDocument as deleteDocumentApi, uploadDocument as uploadDocumentApi , retryDocument as retryDocumentApi} from '@/api/document'

export const useDocumentStore = defineStore('document', () => {
  // 当前知识库中的文档
  const documents = ref<Document[]>([])
  // 列表家在状态
  const loading = ref(false)

  // 安全校验 ID
  const isValidId = (id: number): boolean => {
    return Number.isInteger(id) && id > 0
  }

  // 获取文档列表
  const fetchDocuments = async (knowledgeBaseId: number) => {
    if (!isValidId(knowledgeBaseId)) {
      throw new Error('知识库 ID 无效')
    }

    loading.value = true

    try {
      documents.value = await getDocuments(knowledgeBaseId)
    } catch (error) {
      console.error(error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 删除文档
  const deleteDocument = async (knowledgeBaseId: number, documentId: number) => {

    if (!isValidId(knowledgeBaseId) || !isValidId(documentId)) {
      throw new Error('ID 参数无效')
    }

    try {
      await deleteDocumentApi(knowledgeBaseId, documentId)
      // 乐观更新：本地直接移除
      const index = documents.value.findIndex((doc) => doc.id === documentId)
      if (index !== -1) {
        documents.value.splice(index, 1)
      }
    } catch (error) {
      console.error('[删除文档] 失败：', error)
      throw error
    }
  }

  /**
   * 判断当前是否存在正在处理的文档
   *
   * pending 和 processing 都表示后端任务尚未结束。
   *
   * 状态判断集中在 Store 中，避免页面组件重复编写业务规则。
   */
  const hasProcessingDocuments = (): boolean => {
    return documents.value.some(
      (document) =>
        document.status === 'pending' ||
        document.status === 'processing',
    )
  }

  /**
   * 上传文档
   * 成功后插入列表顶部，即时展示
   * @param knowledgeBaseId 知识库 ID
   * @param file 待上传文件
   */
  const uploadDocument = async (knowledgeBaseId: number, file: File):Promise<Document> => {
    if (!isValidId(knowledgeBaseId)) {
      throw new Error('知识库 ID 无效')
    }
    const document = await uploadDocumentApi(
      knowledgeBaseId,
      file,
    )
  
    documents.value.unshift(document)
  
    return document
  }

  /**
   * 重试失败文档
   * 流程：校验 → 请求 → 本地状态同步 → 异常兜底
  */
  const retryDocument = async (knowledgeBaseId: number, documentId: number):Promise<Document> => {
    // 1. 参数校验 —— 拦截非法请求
    if (!isValidId(knowledgeBaseId) || !isValidId(documentId)) {
      throw new Error('无效的知识库 ID 或文档 ID')
    }

    // 2. 发起请求并同步本地状态
    const updatedDocument = await retryDocumentApi(knowledgeBaseId, documentId)

    // 直接找到引用更新
    const target = documents.value.find(item => item.id === documentId)
    if (target) {
      // 全量覆盖，与后端保持一致
      Object.assign(target, updatedDocument)
    }

    return updatedDocument
  }


  return {
    documents,
    loading,
    fetchDocuments,
    deleteDocument,
    uploadDocument,
    hasProcessingDocuments,
    retryDocument
  }
})
