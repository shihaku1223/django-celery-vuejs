import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import { authGuard } from '../auth/authGuard'

let About = {
  template: '<h2>About</h2>'
}

import SearchPage from '@/components/SearchPage'
import SearchResultPage from '@/components/SearchResultPage'
import Login from '@/components/Login'

let createRouter = () => {
  const routes = [
    {
      path: '/login',
      name: 'login',
      component: Login,
      props: true,
    },
    {
      path: '/',
      name: 'home',
      component: SearchPage,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/search',
      name: 'search',
      component: SearchResultPage,
      meta: {
        requiresAuth: true,
      },
      props: (route) => ({
        query: route.query.q,
        projects: route.query.p
      })
    },
  ]

  const router = new Router({
    routes: routes
  })

  router.beforeEach(authGuard)

  return router
}


export { createRouter };
