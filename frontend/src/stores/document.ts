import { defineStore } from 'pinia'
import { ref } from 'vue'

import type { Document } from '@/types/document'

import { getDocuments, deleteDocument as deleteDocumentApi } from '@/api/document'

export const useDocumentStore = defineStore('document', () => {
  // 当前知识库中的文档
  const documents = ref<Document[]>([])
  // 列表家在状态
  const loading = ref(false)

  // 获取文档列表
  const fetchDocuments = async (knowledgeBaseId: number) => {
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
    try {
      await deleteDocumentApi(knowledgeBaseId, documentId)
      const index = documents.value.findIndex((v) => v.id === documentId)
      if (index !== -1) {
        documents.value.splice(index, 1)
      }
    } catch (error) {
      console.error('[文档删除] 失败：', error)
      throw error
    }
  }

  return {
    documents,
    loading,
    fetchDocuments,
    deleteDocument,
  }
})
