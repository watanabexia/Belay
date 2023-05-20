import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import LoginPage from '../components/LoginPage.vue'
import SignupPage from '../components/SignupPage.vue'
import ChannelList from '../components/ChannelList.vue'
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
        MainContent: HomePage,
      }
    },
    {
      path: '/login',
      name: 'Login',
      components: {
        MainContent: LoginPage,
      }
    },
    {
      path: '/signup',
      name: 'Signup',
      components: {
        MainContent: SignupPage,
      }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      components: {
        LeftSidebar: ChannelList,
        MainContent: Dashboard,
      }
    },
    {
      path: '/profile',
      name: 'Profile',
      components: {
        LeftSidebar: ChannelList,
        MainContent: ProfilePage,
      }
    },
    {
      path: `/channel/:channelId`,
      name: 'Channel',
      components: {
        LeftSidebar: ChannelList,
        MainContent: MessagePage,
      }
    },
    {
      path: `/channel/:channelId/thread/:messageId`,
      name: 'Thread',
      components: {
        LeftSidebar: ChannelList,
        MainContent: MessagePage,
      }
    }
  ]
})

export default router
