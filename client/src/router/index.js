import { createRouter, createWebHistory } from 'vue-router'
import Import_images from '../views/Import_images.vue'
import Login from '../views/LoggingView.vue'
import Logout from '../views/Logout.vue'
import {app} from '../main.js';
import Export from "@/views/Export";

const routes = [
  {
    path: '/login',
    name: 'Login',
    component:Login,
    beforeEnter:(to,from,next)=>{
      if (from.name === 'Import' || from.name === 'Edit')
      {
        router.push('/import');
      }
      else
      {
        next();
      }
    }
  },
  {
    path: '/import',
    name: 'Import',
    component: Import_images,
    beforeEnter:(to,from,next)=>{
      if (from.name === 'Login' && app.config.globalProperties.$is_allowed_to_log_in.value === false)
      {
        router.push('/login');
      }
      else
      {
        next();
      }
    }
  },
  {
    path: '/edit',
    name: 'Edit',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Edit_images.vue'),
    beforeEnter:(to,from,next)=>{
      if (to.name === 'Login')
      {
        router.push('/edit');
      }
      if (from.name === 'Login' && app.config.globalProperties.$is_allowed_to_log_in.value === false)
      {
       router.push('/login');
      }
      else
      {
        next();
      }
    }
  },
  {
    path:'/logout',
    name:'Logout',
    component: Logout,
    beforeEnter:(to,from,next)=>{
      if (from.name === 'Login')
      {
       router.push('/login');
      }
      else
      {
        next();
      }
    }
  },
     {
    path:'/export',
    name:'Export',
    component: Export,
    beforeEnter:(to,from,next)=>{
      if (from.name === 'Export')
      {
       router.push('/export');
      }
      else
      {
        next();
      }
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
export default router
