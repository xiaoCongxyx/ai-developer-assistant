import request from '@/utils/request'

import type { Document } from '@/types/document'

/**
 * 获取指定知识库下的所有文档
 * @param knowledgeBaseId 知识库 ID
 */
export const getDocuments = async (knowledgeBaseId: number) => {
  const res = await request.get<Document[], Document[]>(
    `/knowledge-bases/${knowledgeBaseId}/documents`,
  )

  return res
}

/**
 * 获取单个文档详情
 * @param knowledgeBaseId 知识库 ID
 * @param documentId 文档 ID
 */
export const getDocument = async (knowledgeBaseId: number, documentId: number) => {
  const res = await request.get<Document, Document>(
    `/knowledge-bases/${knowledgeBaseId}/documents/${documentId}`,
  )

  return res
}

/**
 * 删除文档
 * @param knowledgeBaseId 知识库 ID
 * @param documentId 文档 ID
 */
export const deleteDocument = async (knowledgeBaseId: number, documentId: number) => {
  return await request.delete(`/knowledge-bases/${knowledgeBaseId}/documents/${documentId}`)
}

/**
 * 批量删除文档
 * @param knowledgeBaseId 知识库 ID
 * @param documentIds 文档 ID 集合
 */
export const batchDeleteDocuments = async (knowledgeBaseId: number, documentIds: number[]) => {
  return await request.post(
    `/knowledge-bases/${knowledgeBaseId}/documents/batch-delete`,
    documentIds,
  )
}

/**
 * 上传文档
 * @param knowledgeBaseId 知识库 ID
 * @param file 待上传文件对象
 * @param onProgress 可选：进度回调 (0~100)
 * @param signal 可选：AbortSignal 用于取消上传
 */
export const uploadDocument = async (knowledgeBaseId: number, file: File) => {
  const formData = new FormData()
  // 文件上传必须使用 multipart/form-data。
  formData.append('file', file)

  const res = await request.post<Document, Document>(
    `/knowledge-bases/${knowledgeBaseId}/documents/upload`,
    formData,
  )

  return res
}

/**
 * 重新上传
 * @param knowledgeBaseId 知识库 ID
 * @param documentId 文档 ID
 */
export const retryDocument = async (knowledgeBaseId: number, documentId: number) => {
  const res = request.post<Document, Document>(
    `/knowledge-bases/${knowledgeBaseId}/documents/${documentId}/retry`,
  )
  return res
}
