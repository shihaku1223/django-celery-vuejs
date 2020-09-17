<template>
  <div class="w-100 flex">
    <text-label
      style="width: 100px"
      :text="title" />
    <div class="combobox">
      <v-combobox
        ref="input"
        :items="items"
        v-model="internalSelect"
        multiple
        outlined
        dense
      />
  </div>
  </div>

</template>

<style scoped>

.combobox {
  width: auto;
}

</style>


<script>

import TextLabel from '@/components/TextLabel'

export default {


  props: [ 'title', 'items', 'value'],

  computed: {
    internalSelect: {
      get() {
        return this.value
      },
      set(to) {
        this.$emit('input', to)
      },
    },
  },

  methods: {
    update() {
    }
  },

  created() {
  },

  mounted() {
  },

  components: {
    TextLabel,
  }
}
</script>

