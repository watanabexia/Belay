import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import VueCookies from 'vue3-cookies'

import 'bootstrap/dist/css/bootstrap.css'
import "bootstrap-icons/font/bootstrap-icons.css";

import './assets/main.css'

const app = createApp(App)

app.use(router)
app.use(VueCookies)

import utilities from './plugins/utilities.js'
app.use(utilities)

app.mount('#app')
