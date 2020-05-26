import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)


let About = {
  template: '<h2>About</h2>'
}

let createRouter = () => {
  const routes = [
    { path: '/about', name: 'about', component: About },
  ]

  const router = new Router({
    routes
  })

  return router
}


export { createRouter };
