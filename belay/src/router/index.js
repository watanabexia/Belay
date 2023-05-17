import { createRouter, createWebHistory } from 'vue-router'
import Ping from '../components/Ping.vue'
import HomePage from '../components/HomePage.vue'
import LoginPage from '../components/LoginPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomePage
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginPage
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping
    }
  ]
})

export default router
