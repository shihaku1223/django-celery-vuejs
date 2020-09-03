<template>
  <v-card>
    {{ result.id }}
    <v-card-text>
      {{ result.description }}
    </v-card-text>
  </v-card>
</template>


<script>
export default {

  props: [ 'result' ],

  mounted() {
    console.log(this.result)
  }
}
</script>
