<template>
  <div class='navigation bg-purple'>
    <div>
     Mantis Keyword Search System

      <v-text-field
        :style="searchTextFieldStyle"
        v-model="queryString"
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

import { QUERY_STRING } from '../store/modules/mutation-types'

export default {
  name: 'navigation-header-bar',

  data: () => ({
    searchTextFieldStyle: {
      width: '400px'
    },
  }),
  computed: {
    queryString: {
      set(value) {
        this.$store.commit(QUERY_STRING, value)
      },
      get() {
        return this.$store.state.search_result.queryString
      }
    },
  },
  methods: {
    async onEnter() {
      console.log(this.queryString)

      this.$router.push({
        name: 'search',
        query: {
          q: this.queryString
        }
      }).catch(() => {})
    }
  },
}

</script>
