import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import VueCookies from 'vue3-cookies'

import 'bootstrap/dist/css/bootstrap.css'

import './assets/main.css'

const app = createApp(App)

app.use(router)
app.use(VueCookies)

import apiKeyCheck from './plugins/apiKeyCheck.js'
app.use(apiKeyCheck)

import axios from 'axios'
const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:5000/api',
    withCredentials: true
})
app.config.globalProperties.$axios = axiosInstance

app.mount('#app')
