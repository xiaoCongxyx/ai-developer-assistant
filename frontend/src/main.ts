import { createApp } from 'vue'
import { createPinia } from 'pinia'

import './assets/styles/reset.css'
import './assets/styles/variables.css'
import './assets/styles/global.css'

import 'highlight.js/styles/github.css'
import './assets/styles/markdown.css'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'


import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')
