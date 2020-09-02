<template>
  <v-app>

  <div>
    <navigation-header-bar/>
    <router-view/>
  </div>

  </v-app>
</template>

<style scoped>

</style>

<script>

import NavigationHeaderBar from '@/components/NavigationHeaderBar'

export default {

  data: () => ({
  }),

  methods: {

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
