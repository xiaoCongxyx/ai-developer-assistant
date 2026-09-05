import request from "@/utils/request";

import type { Prompt, CreatePromptData } from "@/types/prompt";

export async function getPrompts() {
  const response = await request.get<Prompt[], Prompt[]>('/prompts')

  return response
}

export async function createPrompt(data: CreatePromptData) {
  const response = await request.post<Prompt[], Prompt>('/prompts', data)

  return response
}