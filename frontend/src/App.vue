<script setup lang="ts">
import { useChatStore } from '@/stores/chat'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()
themeStore.initTheme() // 读取上次主题

const chatStore = useChatStore()
// 初始化会话列表
chatStore.initConversation()
</script>

<template>
  <router-view />
</template>

<style scoped></style>
