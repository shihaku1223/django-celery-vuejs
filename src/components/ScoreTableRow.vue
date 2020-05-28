<template>
  <div class="dt-row bg-lightest-silver ba b--silver w5"
    style="min-width: 50px;">
    <div class="dtc bg-lightest-silver ba b--silver"
      style="min-width: 50px;">
      <span v-if="text">
        {{ text }}
      </span>
      <a v-else
        :href='url'>
        {{ url }}
      </a>
    </div>
    <div class="dtc bg-lightest-silver ba b--silver"
      style="min-width: 50px;">
      {{ score }}
    </div>
  </div>

</template>

<style scoped>

</style>

<script>

export default {
  name: 'score-table-row',

  data: () => ({
  }),

  props: {
    text: String,
    url: String,
    score: String,
  },

  computed: {
  },

  mounted() {
  },
}

</script>
