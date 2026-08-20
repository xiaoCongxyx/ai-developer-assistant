import { createRouter, createWebHistory } from 'vue-router'

import MainLayout from '@/layouts/MainLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: MainLayout,
      children: [
        {
          path: '',
          redirect: '/chat'
        },

        {
          path: '/chat',
          component: () => import('@/views/ChatView.vue')
        },

        {
          path: '/prompt',
          component: () => import('@/views/PromptView.vue')
        },

        {
          path: '/knowledge',
          component: () => import('@/views/KnowledgeView.vue')
        },

        {
          path: '/agent',
          component: () => import('@/views/AgentView.vue')
        },

        {
          path: '/settings',
          component: () => import('@/views/SettingsView.vue')
        }
      ]
    }    
  ],
})

export default router
