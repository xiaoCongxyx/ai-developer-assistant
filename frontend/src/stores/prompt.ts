import { defineStore } from "pinia";
import { ref } from "vue";

import type { CreatePromptData, Prompt, UpdatePromptData } from "@/types/prompt";
import { getPrompts, createPrompt as createPromptApi, updatePrompt as updatePromptApi, deletePrompt as deletePromptApi } from "@/api/prompt";

export const usePromptStore = defineStore('prompt', () => {
  // Prompt 列表
  const prompts = ref<Prompt[]>([])

  // 加载状态
  const loading = ref(false)

  // 获取 Prompt 列表
  const fetchPrompts = async () => {
    loading.value = true

    try {
      prompts.value = await getPrompts()
      
    } finally {
      loading.value = false
    }

  }

  // 创建 prompt
  const createPrompt = async (data: CreatePromptData) => {
    const prompt = await createPromptApi(data)

    prompts.value.unshift(prompt)
  }

  //  更新 prompt
  const updatePrompt = async (promptId: number, data: UpdatePromptData) => {
    const prompt = await updatePromptApi(promptId, data)

    const index = prompts.value.findIndex(v => v.id === promptId)

    if(index !== -1) {
      prompts.value[index] = prompt
    }

    return prompt
  }

  // 删除 prompt
  const deletePrompt = async (promptId: number) => {
    await deletePromptApi(promptId)

    const index = prompts.value.findIndex(
      item => item.id === promptId,
    )

    if (index !== -1) {
      prompts.value.splice(index, 1)
    }

  }

  return {
    prompts,
    loading,
    fetchPrompts,
    createPrompt,
    updatePrompt,
    deletePrompt
  }
})