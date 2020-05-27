<template>

  <input class="hk-input"
    ref="input"
    :value="value"
    :placeholder="placeHolder"
    @input="update"/>

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
    },
    value:String
  },

  computed: {
  },

  methods: {
    update() {
      this.$emit('input', this.$refs.input.value)
    }
  }
}

</script>
