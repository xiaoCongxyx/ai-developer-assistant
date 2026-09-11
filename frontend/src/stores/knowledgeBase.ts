import { ref } from 'vue'
import { defineStore } from 'pinia'

import type {
  CreateKnowledgeBaseData,
  KnowledgeBase,
  UpdateKnowledgeBaseData,
} from '@/types/knowledgeBase'

import {
  getKnowledgeBases,
  createKnowledgeBase as createKnowledgeBaseApi,
  updateKnowledgeBase as updateKnowledgeBaseApi,
  deleteKnowledgeBase as deleteKnowledgeBaseApi,
} from '@/api/knowledgeBase'

export const useKnowledgeBaseStore = defineStore('knowledgeBase', () => {
  // 知识库列表
  const knowledgeBases = ref<KnowledgeBase[]>([])

  // 📌 加载状态
  const loading = ref(false)

  // 获取知识库列表
  const fetchKnowledgeBases = async () => {
    loading.value = true

    try {
      knowledgeBases.value = await getKnowledgeBases()
    } catch (error) {
      console.error('获取知识库列表失败:', error)
      knowledgeBases.value = [] // 兜底清空
    } finally {
      loading.value = false
    }
  }

  // 创建知识库
  const createKnowledgeBase = async (data: CreateKnowledgeBaseData) => {
    try {
      const knowledgeBase = await createKnowledgeBaseApi(data)
      knowledgeBases.value.unshift(knowledgeBase)
      return knowledgeBase
    } catch (err) {
      console.error('[知识库] 创建失败：', err)
      throw err
    }
  }

  // 📌 更新知识库
  const updateKnowledgeBase = async (knowledgeBaseId: number, data: UpdateKnowledgeBaseData) => {
    try {
      const knowledgeBase = await updateKnowledgeBaseApi(knowledgeBaseId, data)

      const index = knowledgeBases.value.findIndex((v) => v.id === knowledgeBaseId)

      if (index !== -1) {
        knowledgeBases.value[index] = knowledgeBase
      }
      return knowledgeBase
    } catch (err) {
      console.error('[知识库] 更新失败：', err)
      throw err
    }
  }

  // 📌 删除知识库
  const deleteKnowledgeBase = async (knowledgeBaseId: number) => {
    try {
      await deleteKnowledgeBaseApi(knowledgeBaseId)
      // API 删除成功才移除本地项
      const index = knowledgeBases.value.findIndex((item) => item.id === knowledgeBaseId)
      if (index !== -1) {
        knowledgeBases.value.splice(index, 1)
      }
    } catch (err) {
      console.error('[知识库] 删除失败：', err)
      throw err
    }
  }

  return {
    knowledgeBases,
    loading,
    fetchKnowledgeBases,
    createKnowledgeBase,
    updateKnowledgeBase,
    deleteKnowledgeBase,
  }
})
