<template>

  <div>
    <navigation-header-bar v-if="isAuthenticated"/>
    <router-view/>
  </div>
</template>

<style scoped>

</style>

<script>

import NavigationHeaderBar from '@/components/NavigationHeaderBar'

import { getInstance } from './auth/index'

export default {

  data: () => ({
  }),

  methods: {
  },

  computed: {
    isAuthenticated() {
      const authService = getInstance()
      return authService.isAuthenticated
    }
  },

  watch: {

  },

  mounted() {
  },

  components: {
    NavigationHeaderBar,
  }
}
</script>
