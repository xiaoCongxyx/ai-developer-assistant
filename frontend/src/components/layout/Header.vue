<script setup lang="ts">
import { Moon, Sunny, User, Setting, SwitchButton } from '@element-plus/icons-vue'
import { useThemeStore } from '@/stores/theme'
import logo from '@/assets/images/logo.png'

const themeStore = useThemeStore()
const isDark = themeStore.isDark

const toggleTheme = () => {
  themeStore.toggleTheme()
}
</script>

<template>
  <header class="header">
    <div class="header-left">
      <img :src="logo" alt="logo" class="logo" />
      <div class="app-info">
        <span class="app-name">AI Developer Assistant</span>
        <span class="app-version">V1.0</span>
      </div>
    </div>

    <div class="header-right">
      <el-button circle class="theme-btn" @click="toggleTheme">
        <el-icon>
          <Moon v-if="!isDark" />
          <Sunny v-else />
        </el-icon>
      </el-button>

      <el-dropdown trigger="click">
        <div class="user-info">
          <el-avatar :size="36" :src="logo" />
          <span class="user-name">XCXYX</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>
              <el-icon><User /></el-icon>
              个人资料
            </el-dropdown-item>
            <el-dropdown-item>
              <el-icon><Setting /></el-icon>
              系统设置
            </el-dropdown-item>
            <el-dropdown-item divided>
              <el-icon><SwitchButton /></el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<style scoped>
.header {
  height: 56px;
  padding: 0 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color-lighter);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.logo {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.app-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.app-name {
  font-size: 17px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  letter-spacing: 0.3px;
}

.app-version {
  padding: 2px 8px;
  font-size: 12px;
  border-radius: 10px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.theme-btn {
  color: var(--el-text-color-secondary);
  transition: all 0.2s ease;
}
.theme-btn:hover {
  color: var(--el-color-primary);
  background: var(--el-color-primary-light-9);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 10px;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.2s ease;
}
.user-info:hover {
  background: var(--el-fill-color-light);
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}
</style>
