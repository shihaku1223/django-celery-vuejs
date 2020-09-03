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

      <div class="dark-gray f4 normal mt0 bb b--silver" />
      <div class="flex">
        <button v-if="showOptionButton" class="hk-button-sm--primary"
          @click="onOptionClick">オプション
        </button>
      </div>
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

import SearchMixin from '../mixins/search'
import projectTreeItem from '@/constants/projectTreeItem'

export default {
  name: 'navigation-header-bar',

  mixins: [ SearchMixin ],

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
    projectString() {
      let projectNames = []
      let value = this.$store.state.search_result.targetProjects
      this.getSelectedProjectNames(this.items, value, projectNames)

      return projectNames.join()
    },
    items() {
      return projectTreeItem
    },
    showOptionButton() {
      return this.$route.name != "home"
    }
  },

  watch: {
    $route(to) {
    }
  },

  methods: {
    onOptionClick() {
      this.$router.push({
        name: 'home',
      }).catch(() => {})
    },

    async onEnter() {
      console.log(this.queryString)
      console.log(this.projectString)

      this.$router.push({
        name: 'search',
        query: {
          q: this.queryString,
          p: this.projectString
        }
      }).catch(() => {})
    }
  },

}

</script>
