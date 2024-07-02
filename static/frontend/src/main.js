import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import axios from 'axios'


export const server = "https://shgplus.pythonanywhere.com"
axios.defaults.baseURL = server

createApp(App).use(store).use(router).mount('#app')
