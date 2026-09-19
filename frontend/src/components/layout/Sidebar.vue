<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ChatDotRound, DocumentAdd, Reading, Platform, Setting } from '@element-plus/icons-vue'
import ConversationList from '../sidebar/ConversationList.vue'

const route = useRoute()

// ✅ 智能匹配：父级路径也高亮（/knowledge/1 → 高亮 /knowledge）
const defaultActive = computed(() => {
  const path = route.path
  if (path.startsWith('/knowledge/')) return '/knowledge'
  if (path.startsWith('/chat/')) return '/chat'
  if (path.startsWith('/prompt/')) return '/prompt'
  if (path.startsWith('/agent/')) return '/agent'
  if (path.startsWith('/settings/')) return '/settings'
  return path
})

const menus = [
  {
    path: '/chat',
    title: '对话聊天',
    icon: ChatDotRound,
  },
  {
    path: '/prompt',
    title: '提示词管理',
    icon: DocumentAdd,
  },
  {
    path: '/knowledge',
    title: '知识库管理',
    icon: Reading,
  },
  {
    path: '/agent',
    title: '智能体',
    icon: Platform,
  },
  {
    path: '/settings',
    title: '系统设置',
    icon: Setting,
  },
]
</script>

<template>
  <aside class="sidebar">
    <!-- Logo 区域 -->
    <div class="sidebar-logo">🤖 AI Assistant</div>

    <!-- 会话列表：仅聊天页面显示 -->
    <ConversationList v-if="route.path.startsWith('/chat')" />

    <!-- 功能菜单 -->
    <nav class="menu-wrapper">
      <el-menu :default-active="defaultActive" router class="menu">
        <el-menu-item v-for="item in menus" :key="item.path" :index="item.path">
          <el-icon>
            <component :is="item.icon" />
          </el-icon>
          <span>{{ item.title }}</span>
        </el-menu-item>
      </el-menu>
    </nav>
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
  padding: 0 24px;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 1px solid var(--border-light);
  letter-spacing: 0.3px;
}

.menu-wrapper {
  flex: 1; /* ✅ 占满剩余空间，菜单靠上、不挤底部 */
  padding: 16px 12px 24px;
}

:deep(.el-menu) {
  border-right: none;
  background: transparent;
}

:deep(.el-menu-item) {
  height: 44px;
  margin: 4px 0;
  padding: 0 16px !important;
  border-radius: var(--radius);
  color: var(--sidebar-text);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
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

:deep(.el-menu-item .el-icon) {
  margin-right: 10px;
  font-size: 17px;
}
</style>
