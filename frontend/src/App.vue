<script setup lang="ts">
import { useChatStore } from '@/stores/chat';

const chatStore = useChatStore()
// 初始化会话列表
chatStore.initConversation()
</script>

<template>
  <router-view />
</template>

<style scoped></style>
