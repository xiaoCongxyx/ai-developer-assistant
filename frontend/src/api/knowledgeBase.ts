import request from "@/utils/request";

import type {
  KnowledgeBase,
  CreateKnowledgeBaseData,
  UpdateKnowledgeBaseData,
} from '@/types/knowledgeBase'

/** 获取全部知识库列表 */
export const getKnowledgeBases = async () => {
  return request.get<KnowledgeBase[], KnowledgeBase[]>('/knowledge-bases');
};

/** 获取单个知识库详情 */
export const getKnowledgeBase = async (knowledgeBaseId: number) => {
  return request.get<KnowledgeBase, KnowledgeBase>(`/knowledge-bases/${knowledgeBaseId}`);
};

/** 创建知识库 */
export const createKnowledgeBase = async (data: CreateKnowledgeBaseData) => {
  console.log(data);
  
  return request.post<KnowledgeBase, KnowledgeBase>('/knowledge-bases', data);
};

/** 更新知识库 */
export const updateKnowledgeBase = async (knowledgeBaseId: number, data: UpdateKnowledgeBaseData) => {
  return request.put<KnowledgeBase, KnowledgeBase>(`/knowledge-bases/${knowledgeBaseId}`, data);
};

/** 删除知识库 */
export const deleteKnowledgeBase = async (knowledgeBaseId: number) => {
  return request.delete<{ success: boolean }>(`/knowledge-bases/${knowledgeBaseId}`);
}