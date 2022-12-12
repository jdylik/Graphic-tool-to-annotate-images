import { createRouter, createWebHistory } from 'vue-router'
import Import_images from '../views/Import_images.vue'

const routes = [
  {
    path: '/',
    name: 'Import',
    component: Import_images
  },
  {
    path: '/edit',
    name: 'Edit',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Edit_images.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
