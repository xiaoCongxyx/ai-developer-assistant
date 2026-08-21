<script setup lang="ts">
import { User } from '@element-plus/icons-vue';

import type { Message } from '@/types/chat';

const msgProps = defineProps<{
  message: Message
}>()

</script>

<template>
<div
  class="message"
  :class="message.role"
>
  <div class="bubble">
    {{ message.content }}
  </div>
</div>
</template>

<style scoped>
.message {
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.bubble {
  max-width: 70%;

  padding: 12px 16px;

  border-radius: 12px;

  line-height: 1.6;

  word-break: break-word;
}

.user .bubble {
  background: var(--color-primary);
  color: white;
}

.assistant .bubble {
  background: white;

  border: 1px solid var(--border-color);
}

</style>