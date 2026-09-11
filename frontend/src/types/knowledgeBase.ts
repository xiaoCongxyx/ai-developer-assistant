export interface KnowledgeBase {
  id: number
  name: string
  description: string
  created_at: string
  updated_at: string
}

export interface CreateKnowledgeBaseData {
  name: string
  description: string
}

export interface UpdateKnowledgeBaseData {
  name: string
  description: string
}