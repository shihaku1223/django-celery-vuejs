<template>
  <v-row
    no-gutters
  >
    <v-card-subtitle>
      {{ title }}
    </v-card-subtitle>
    <v-card-text>
      <text-highlight :queries="queries">{{ text }}</text-highlight>
    </v-card-text>
  </v-row>

</template>

<style scoped>

.v-card__subtitle {
  padding: 3px;
}
</style>



<script>
export default {

  props: [ 'queries', 'title', 'text' ],

  created() {
  },

  computed: {
  },

 
  updated() {
  },

  mounted() {
  }
}
</script>
