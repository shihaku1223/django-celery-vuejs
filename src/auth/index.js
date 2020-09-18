let instance
import Vue from 'vue'

export const getInstance = () => instance

export const useAuth = () => {

  if(instance)
    return instance

  instance = new Vue({
    data() {
      return {
        isAuthenticated: false
      }
    },

    methods: {

      async login(auth) {
        try {
          let r = await this.axios.post('auth/token/', auth)
          this.isAuthenticated = true
          return Promise.resolve(r.data)
        } catch(e) {
          console.log(e)
          return Promise.reject(e.response.data.detail)
        }
      },

      async refresh(token) {
        try {
          let r = await this.axios.post('auth/token/refresh/',
            { 'refresh': token })
          this.isAuthenticated = true
          return Promise.resolve(r.data.access)
        } catch(e) {
          console.log(e)
          return Promise.reject(e.response.data.detail)
        }
      },

      async verify(token) {
        try {
          let r = await this.axios.post('auth/token/verify/',
            { 'token': token })
          this.isAuthenticated = true
          return Promise.resolve()
        } catch(e) {
          return Promise.reject(e.response.data.detail)
        }
      }
    },

    created() {
      console.log('AuthPlugin created')
    },
  })

  return instance
}

export const AuthPlugin = {
  install(Vue, options) {
    Vue.prototype.$auth = useAuth()
  }
}
