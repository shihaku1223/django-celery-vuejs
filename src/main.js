// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

import axios from 'axios'
import VueAxios from 'vue-axios'
import { axiosConfig } from '@/config'

import Loading from 'vue-loading-overlay'
import 'vue-loading-overlay/dist/vue-loading.css'
Vue.use(Loading)

import SearchApp from './SearchApp'
import { createStore } from '@/store/index'
import { createRouter } from './router'

import vuetify from '@/plugins/vuetify'
import '@/css/app.css'

Vue.config.productionTip = false

Vue.use(VueAxios, axios.create(axiosConfig))

const router = createRouter()
const store = createStore()

/* eslint-disable no-new */
new Vue({
  vuetify,
  el: '#app',
  store: store,
  router: router,
  components: { SearchApp },
  template: '<SearchApp/>',

  created: () => {
    console.log('created')
  }
})
