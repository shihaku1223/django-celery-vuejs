import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

import { authGuard } from '../auth/authGuard'

let About = {
  template: '<h2>About</h2>'
}

import CalcSimApp from '../CalcSimApp'
import SearchApp from '../SearchApp'
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
      path: '/calcsim',
      name: 'calcsim',
      component: CalcSimApp,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: '/mkss',
      component: SearchApp,
      children: [
        { path: '', name: 'mkss_home', component: SearchPage },
        { path: 'search', name: 'search', component: SearchResultPage,
          props: (route) => ({
            query: route.query.q,
            projects: route.query.p
          })
        },
      ],
      meta: {
        requiresAuth: true,
      },
    },
  ]

  const router = new Router({
    routes: routes
  })

  router.beforeEach(authGuard)

  return router
}


export { createRouter };
