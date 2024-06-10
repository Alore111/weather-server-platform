import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import axios from 'axios';
import 'element-plus/dist/index.css'

const app = createApp(App)


// app.config.globalProperties.$serverUrl = 'https://wv-server-test.2ndtool.top'
app.config.globalProperties.$serverUrl = 'http://127.0.0.1:9001'

app.use(router)
app.use(ElementPlus)

app.mount('#app')
