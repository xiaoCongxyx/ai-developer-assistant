// 代表数据库中已经存在的Prompt
export interface Prompt {
  id: number
  name: string
  description: string
  content: string
  is_default: boolean
}

// 创建不需要id和is_default 由后端负责生成处理
export interface CreatePromptData {
  name: string
  description: string
  content: string
}

export interface UpdatePromptData {
  name: string
  description: string
  content: string
}