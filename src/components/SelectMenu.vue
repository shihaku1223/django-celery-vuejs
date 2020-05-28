<template>

  <select class="hk-select"
    ref="select"
    @change="onChange"
    :value="value"
  >
    <option v-for="(option, index) in options"
      :value="option.value">
      {{ option.text }}
    </option>
  </select>

</template>

<style scoped>

</style>

<script>

export default {
  name: 'select-menu',

  data: () => ({
    selected: "summary"
  }),

  props: {
    options: Array,
    value: String
  },

  computed: {
  },

  mounted() {
  },

  methods: {
    onChange() {
      this.$emit('input', this.$refs.select.value)
    }
  }
}

</script>
