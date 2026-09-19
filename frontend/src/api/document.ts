import request from '@/utils/request'

import type { Document } from '@/types/document'

// 获取知识库中的文档
export const getDocuments = async (knowledgeBaseId: number) => {
  const res = request.get<Document[], Document[]>(`/knowledge-bases/${knowledgeBaseId}/documents`)

  return res
}

// 获取单个文档
export const getDocument = async (knowledgeBaseId: number, documentId: number) => {
  const res = request.get<Document, Document>(
    `/knowledge-bases/${knowledgeBaseId}/documents/${documentId}`,
  )

  return res
}

// 📌 删除文档
export async function deleteDocument(knowledgeBaseId: number, documentId: number) {
  return await request.delete(`/knowledge-bases/${knowledgeBaseId}/documents/${documentId}`)
}
