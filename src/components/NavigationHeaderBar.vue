<template>
  <div class='navigation bg-purple'>
    <div>
     Mantis Keyword Search System

      <v-text-field
        :style="searchTextFieldStyle"
        rounded
        background-color="grey"
        prepend-inner-icon="search"
        v-on:keyup.enter="onEnter"
      ></v-text-field>
    </div>
  </div>
</template>

<style scoped>

.navigation {
  position: sticky;
  top: 0;
  color: white;
  z-index: 1;

  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 14px;
  font-family: "salesforce-sans", -apple-system, BlinkMacSystemFont, 'avenir next', avenir, helvetica, 'helvetica neue', ubuntu, roboto, noto, 'segoe ui', arial, sans-serif;
}

</style>

<script>

export default {
  name: 'navigation-header-bar',

  data: () => ({
    searchTextFieldStyle: {
      width: '400px'
    },
  }),
  computed: {
    headerStype() {
    }
  },
  methods: {
    onEnter() {
      console.log('enter')
    }
  }
}

</script>
