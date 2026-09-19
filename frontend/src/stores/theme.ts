import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(false)

  // ✅ 修复：classList 只操作类名，属性用 dataset
  const applyTheme = (dark: boolean) => {
    isDark.value = dark
    if (dark) {
      document.documentElement.classList.add('dark')
      document.documentElement.dataset.theme = 'dark' // ✅ 正确写法
    } else {
      document.documentElement.classList.remove('dark')
      document.documentElement.removeAttribute('data-theme') // ✅ 正确写法
    }
  }

  // 切换明暗
  const toggleTheme = () => {
    const next = !isDark.value
    localStorage.setItem('theme', next ? 'dark' : 'light')
    applyTheme(next)
  }

  // 初始化：优先本地存储 → 否则跟随系统
  const initTheme = () => {
    const saved = localStorage.getItem('theme')
    if (saved === 'dark') return applyTheme(true)
    if (saved === 'light') return applyTheme(false)

    // 未手动设置 → 跟随系统偏好
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    applyTheme(prefersDark)
  }

  return { isDark, initTheme, toggleTheme }
})