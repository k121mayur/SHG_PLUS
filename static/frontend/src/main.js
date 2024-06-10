import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import axios from 'axios'


export const server = "http://127.0.0.1:5000"
axios.defaults.baseURL = server

createApp(App).use(store).use(router).mount('#app')
