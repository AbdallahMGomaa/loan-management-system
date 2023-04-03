// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
      },
      {
        path: 'login/',
        name: 'Login',
        component: () => import('@/views/Login.vue')
      },
      {
        path: 'admin/',
        name: 'admin',
        component: () => import('@/views/Admin.vue'),
      },
      {
        path: 'provider/',
        name: 'provider',
        component: () => import('@/views/Provider.vue')
      },
      {
        path: 'customer/',
        name: 'customer',
        component: () => import('@/views/Customer.vue')
      },
      {
        path: 'employee/',
        name: 'employee',
        component: () => import('@/views/Employee.vue')
      }
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
