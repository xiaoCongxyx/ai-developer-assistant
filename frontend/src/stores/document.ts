import { defineStore } from 'pinia'
import { ref } from 'vue'

import type { Document } from '@/types/document'

import { getDocuments, deleteDocument as deleteDocumentApi, uploadDocument as uploadDocumentApi } from '@/api/document'

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

  return {
    documents,
    loading,
    fetchDocuments,
    deleteDocument,
    uploadDocument
  }
})
