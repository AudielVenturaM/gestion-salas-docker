import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/rooms/:id',
      name: 'RoomDetail',
      component: () => import('../views/RoomDetailView.vue')
    }
  ]
})

export default router
