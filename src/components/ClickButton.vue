<template>

  <div class="flex">
    <button class="hk-button--secondary"
      @click="onClick"
      >
      {{ text }}
    </button>
  </div>

</template>

<style scoped>

</style>

<script>

export default {
  name: 'click-button',

  data: () => ({
  }),

  props: {
    text: String,
  },

  computed: {
  },

  mounted() {
  },

  methods: {
    onClick(e) {
      this.$emit('click')
      e.preventDefault()
    }
  }
}

</script>
