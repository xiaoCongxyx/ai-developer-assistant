<script setup lang="ts">
import { Moon, Sunny } from '@element-plus/icons-vue'
import logo from '@/assets/images/logo.png'

const isDark = false
</script>

<template>
  <header class="header">
    <div class="header-left">
      <img :src="logo" alt="logo" class="logo" />

      <div class="app-info">
        <span class="app-name">
          AI Developer Assistant
        </span>

        <span class="app-version">
          V1.0
        </span>
      </div>
    </div>

    <div class="header-right">
      <el-button circle>
        <el-icon>
          <Moon v-if="!isDark" />
          <Sunny v-else />
        </el-icon>
      </el-button>

      <el-dropdown trigger="click">
        <div class="user-info">
          <el-avatar
            :size="36"
            :src="logo"
          />

          <span class="user-name">
            XCXYX
          </span>
        </div>

        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>
              Profile
            </el-dropdown-item>

            <el-dropdown-item>
              Settings
            </el-dropdown-item>

            <el-dropdown-item divided>
              Logout
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
  padding: 0 24px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  background: var(--bg-page);
  border-bottom: 1px solid var(--border-color);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.app-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.app-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.app-version {
  padding: 2px 8px;

  font-size: 12px;

  border-radius: 12px;

  background: #ecf5ff;
  color: #409eff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;

  cursor: pointer;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}
</style>