import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import LoginPage from '../components/LoginPage.vue'
import SignupPage from '../components/SignupPage.vue'
import Dashboard from '../components/Dashboard.vue'
import ProfilePage from '../components/ProfilePage.vue'
import MessagePage from '../components/MessagePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      components: {
        LeftSidebar: HomePage,
      }
    },
    {
      path: '/login',
      name: 'Login',
      components: {
        LeftSidebar: LoginPage,
      }
    },
    {
      path: '/signup',
      name: 'Signup',
      components: {
        LeftSidebar: SignupPage,
      }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      components: {
        LeftSidebar: Dashboard,
        MainContent: MessagePage,
      }
    },
    {
      path: '/profile',
      name: 'Profile',
      components: {
        LeftSidebar: ProfilePage,
      }
    }
  ]
})

export default router
