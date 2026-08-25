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
          path: 'chat',
          name: 'Chat',
          component: () => import('@/views/ChatView.vue')
        },

        {
          path: 'prompt',
          name: 'Prompt',
          component: () => import('@/views/PromptView.vue')
        },

        {
          path: 'knowledge',
          name: 'Knowledge',
          component: () => import('@/views/KnowledgeView.vue')
        },

        {
          path: 'agent',
          name: 'Agent',
          component: () => import('@/views/AgentView.vue')
        },

        {
          path: 'settings',
          name: 'Settings',
          component: () => import('@/views/SettingsView.vue')
        }
      ]
    }    
  ],
})

export default router
