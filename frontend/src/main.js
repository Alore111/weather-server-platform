import './assets/main.css'
import { createPinia } from 'pinia'
import { IndexBar, IndexAnchor, Cell, Button } from 'vant';

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import axios from 'axios';
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'vant/lib/index.css';

export const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.config.globalProperties.$serverUrl = 'http://127.0.0.1:9001'
// app.config.globalProperties.$serverUrl = 'https://wv-server-test.2ndtool.top'

app.use(router)
app.use(ElementPlus)
app.use(ElementPlus)
app.use(IndexBar);
app.use(IndexAnchor);
app.use(Cell);
app.use(Button)
app.use(createPinia())

app.mount('#app')
