import { createRouter, createWebHistory } from 'vue-router'
import loginView from '../views/LoginView.vue'

const routes = [
  {
    path: '/',
    name: 'login',
    component: loginView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    }
  }, 

  {
    path: '/dashboard',
    name: 'login',
    component: loginView
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
