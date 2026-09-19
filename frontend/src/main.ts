import { createApp } from 'vue'
import { createPinia } from 'pinia'

import './assets/styles/reset.css'
import './assets/styles/variables.css'
import './assets/styles/global.css'

import 'highlight.js/styles/github.css'
import './assets/styles/markdown.css'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import 'element-plus/theme-chalk/dark/css-vars.css' // 引入 EP 暗色基础变量
import '@/assets/styles/theme.css' // 你的自定义主题变量，放后面覆盖


import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')
