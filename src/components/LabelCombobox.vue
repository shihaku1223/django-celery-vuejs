<template>
  <div class="w-100 flex">
    <text-label
      style="width: 100px"
      :text="title" />
    <div class="combobox">
      <v-combobox
        ref="input"
        :items="items"
        v-model="select"
        @input="update"
        outlined
        dense
      />
  </div>
  </div>

</template>

<style scoped>

.combobox {
  width: 200px;
}

</style>


<script>

import TextLabel from '@/components/TextLabel'

export default {

  data: () => ({
    select: undefined
  }),

  props: [ 'title', 'items'],

  methods: {
    update() {
      this.$emit('input', this.select)
    }
  },

  created() {
    this.select = this.items[0]
    this.$emit('input', this.select)
  },

  components: {
    TextLabel,
  }
}
</script>

