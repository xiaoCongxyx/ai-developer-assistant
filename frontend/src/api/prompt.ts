import request from "@/utils/request";

import type { Prompt, CreatePromptData, UpdatePromptData } from "@/types/prompt";

export async function getPrompts() {
  const response = await request.get<Prompt[], Prompt[]>('/prompts')

  return response
}

export async function createPrompt(data: CreatePromptData) {
  const response = await request.post<Prompt, Prompt>('/prompts', data)

  return response
}

export async function updatePrompt(promptId: number, data: UpdatePromptData) {
  const response = await request.put<Prompt, Prompt>(`/prompts/${promptId}`, data)

  return response
}

export async function deletePrompt(promptId: number) {
  const response = await request.delete(`/prompts/${promptId}`)

  return response
}