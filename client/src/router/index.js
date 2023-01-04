import { createRouter, createWebHistory } from 'vue-router'
import Import_images from '../views/Import_images.vue'
import Login from '../views/LoggingView.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component:Login
  },
  {
    path: '/import',
    name: 'Import',
    component: Import_images,
    //beforeEnter:(to,from,next)=>{
    //  if (from.name === 'Login' && this.is_allowed_to_log_in === false)
     // {
     //   router.push('/login');}
    //}
  },
  {
    path: '/edit',
    name: 'Edit',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Edit_images.vue'),
    //beforeEnter:(to,from,next)=>{
    //  if (from.name === 'Login' && this.is_allowed_to_log_in === false)
    //  {
    //    router.push('/login');}
    //}
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
export default router
