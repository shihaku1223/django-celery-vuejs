import { getInstance } from '../auth/index'

export default {
  methods: {
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('refresh')

      const authService = getInstance()
      authService.logout()

      this.$router.go(this.$router.currentRoute)
    },

    refresh(refresh) {
      const authService = getInstance()
      authService.refresh(refresh)
        .then((token) => {
        localStorage.token = token
      })
    },
  },
}
