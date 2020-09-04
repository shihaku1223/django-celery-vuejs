

import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.use(Vuetify)

const opts = {
  icons: {
    iconfont: 'md', // default - only for display purposes
  }
}

export default new Vuetify(opts)
