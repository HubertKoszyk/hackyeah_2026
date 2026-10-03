import { createRouter, createWebHistory } from 'vue-router'
import TrafficView from '../views/TrafficView.vue'
import ParkingView from '../views/ParkingView.vue'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/traffic',
    },
    {
      path: '/traffic',
      name: 'traffic',
      component: TrafficView,
    },
    {
      path: '/parking',
      name: 'parking',
      component: ParkingView,
    },
    {
      path: '/components',
      name: 'components',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router
