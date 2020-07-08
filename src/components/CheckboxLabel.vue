<template>
  <div>
    <input type="checkbox"
      ref="input"
      :id="`checkbox_${value}`"
      v-model="checkedNames"
      :value="value">
    <label :for="`checkbox_${value}`">{{ text }}</label><br>
  </div>
</template>

<script>

export default {
  name: 'checkbox-label',

  data: () => ({
  }),

  props: {
    text: String,
    value: String,
  },

  computed: {
    checkedNames: {
      get() {
        return this.$store.state.target_checkbox.checkedNames
      },
      set(value) {
        this.$store.commit('SAVE_CHECKEDNAMES', value)
        localStorage.checkedNames = value
      }
    }
  },

  mounted() {
    
  },

  methods: {
  }
}

</script>
