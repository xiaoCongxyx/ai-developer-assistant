export type DocumentStatus =
  | 'pending'
  | 'processing'
  | 'completed'
  | 'failed'

export interface Document {
  id: number
  knowledge_base_id: number
  name: string
  file_type: string
  file_path: string
  file_size: number
  status: DocumentStatus
  error_message: string | null
  created_at: string
  updated_at: string
}