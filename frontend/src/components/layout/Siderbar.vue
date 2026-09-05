<script setup lang="ts">
import { ChatDotRound, DocumentAdd, Reading, Platform, Setting } from '@element-plus/icons-vue'

import ConversationList from '../sidebar/ConversationList.vue'

const menus = [
  {
    path: '/chat',
    title: 'Chat',
    icon: ChatDotRound,
  },
  {
    path: '/prompt',
    title: 'Prompt',
    icon: DocumentAdd,
  },
  {
    path: '/knowledge',
    title: 'Knowledge',
    icon: Reading,
  },
  {
    path: '/agent',
    title: 'Agent',
    icon: Platform,
  },
  {
    path: '/settings',
    title: 'Settings',
    icon: Setting,
  },
]
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-logo">🤖 Assistant</div>

    <!-- 会话列表 -->
    <ConversationList v-if="$route.path.startsWith('/chat')" />

    <!-- 功能菜单 -->

    <div class="menu-wrapper">
      <el-menu router default-active="/chat" class="menu">
        <el-menu-item v-for="item in menus" :key="item.path" :index="item.path">
          <el-icon>
            <component :is="item.icon" />
          </el-icon>

          <span>
            {{ item.title }}
          </span>
        </el-menu-item>
      </el-menu>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border-color);
}

.sidebar-logo {
  height: var(--header-height);
  display: flex;
  align-items: center;
  padding: 0 20px;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 1px solid var(--border-light);
}

.menu-wrapper {
  margin-top: auto;
  padding-bottom: 20px;
}

:deep(.el-menu) {
  border-right: none;
  background: transparent;
}

:deep(.el-menu-item) {
  height: 44px;
  margin: 6px 12px;

  border-radius: var(--radius);

  color: var(--sidebar-text);

  transition: all 0.2s ease;
}

:deep(.el-menu-item:hover) {
  background: var(--bg-sidebar-hover);
  color: var(--sidebar-text-hover);
}

:deep(.el-menu-item.is-active) {
  background: var(--bg-sidebar-active);
  color: var(--sidebar-text-active);
  font-weight: 600;
}

:deep(.el-icon) {
  margin-right: 10px;
  font-size: 16px;
}
</style>
