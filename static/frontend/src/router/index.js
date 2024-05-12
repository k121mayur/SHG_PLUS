import { createRouter, createWebHistory } from 'vue-router'
import loginView from '../views/LoginView.vue'
import dashboardView from '../views/dashboardView.vue'
import dataEntryView from '../views/dataEntryView.vue'
import newGroupEntry from '../views/newGroupEntry.vue'

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
    name: 'dashboard',
    component: dashboardView
  },

  {
    path: '/dataEntry',
    name: 'dataEntry',
    component: dataEntryView
  },

  {
    path: '/newGroup',
    name: 'newGroup',
    component: newGroupEntry
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
