import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)


let About = {
  template: '<h2>About</h2>'
}

import SearchPage from '@/components/SearchPage'
import SearchResultPage from '@/components/SearchResultPage'

let createRouter = () => {
  const routes = [
    { path: '/about', name: 'about', component: About },
    { path: '/', name: 'home', component: SearchPage },
    {
      path: '/search',
      name: 'search',
      component: SearchResultPage,
      props: (route) => ({ query: route.query.q })
    },
  ]

  const router = new Router({
    routes: routes
  })

  return router
}


export { createRouter };
