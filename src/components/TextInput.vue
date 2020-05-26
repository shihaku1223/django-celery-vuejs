<template>

  <input class="hk-input" :placeholder="placeHolder" />

</template>

<style scoped>

</style>

<script>

export default {
  name: 'text-input',

  data: () => ({
  }),

  props: {
    isActive: {
      type: Boolean,
      default: false,
    },
    placeHolder: String,
    href: {
      type: String,
      default: "#hello"
    }
  },

  computed: {
  },

  methods: {
    onClick(e) {
      this.$emit('click')
      e.preventDefault()
    }
  }
}

</script>
