<template>
  <div class='navigation bg-purple'>
    <div>
     Mantis Keyword Search System

      <div class="content">

      <v-text-field
        class="keyword-field"
        :style="searchTextFieldStyle"
        v-model="queryString"
        rounded
        background-color="grey"
        prepend-inner-icon="search"
        v-on:keyup.enter="onEnter"
        @focus="keywordFieldFocus = true"
        @blur="keywordFieldFocus = false"
      >
      </v-text-field>

      <span class="tooltiptext"
        :style="tooltipTextStyle"
        >
        例：CV2K -GUI
        <br>
        OTV "開発権限"
      </span>

      </div>

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

.content {
  position: relative;
}

.tooltiptext {
  border-radius: 4px;
  border: 1px solid #79589f;
  color: #79589f;
  background: #fff;
  font-weight: 600;
  line-height: 22px;
  width: 200px;
  top: 50px;
  left: 50px;

  padding: 4px 15px;
  visibility: hidden;
  font-size: 13px;
  justify-content: center;

  /* Position the tooltip */
  position: absolute;
  z-index: 1;
}

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

import { getInstance } from '../auth/index'

import {
  TARGET_PROJECTS,
  QUERY_STRING
} from '../store/modules/mutation-types'

import SearchMixin from '../mixins/search'
import projectTreeItem from '@/constants/projectTreeItem'

export default {
  name: 'navigation-header-bar',

  mixins: [ SearchMixin ],

  data: () => ({
    keywordFieldFocus: undefined,
    defaultItem: [
        205,115,143,220,154,144,146,151,142,134,135,163,184,162,217,168,167,177,176,180,178,181,182,183,193,191,194,195,196,199,197,200,201,202,187,185,188,189,190,165,166,164,212,213,214,208,222,221,156,226,153,223,155,224
    ],
    searchTextFieldStyle: {
      width: '400px'
    },
  }),
  computed: {

    tooltipTextStyle() {
      if(this.keywordFieldFocus && this.queryString.length == 0)
        return { visibility: 'visible' }
      return { visibility: 'hidden' }
    },

    queryString: {
      set(value) {
        this.$store.commit(QUERY_STRING, value)
      },
      get() {
        return this.$store.state.search_result.queryString
      }
    },

    searchOptions() {
      return this.$store.state.search_result.searchOptions
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

    setDefaultValue() {
      if(localStorage.selectedProjects &&
         localStorage.selectedProjects != '') {
        let a = localStorage.selectedProjects.split(',').
          map((s) => {
            return parseInt(s)
          })
        this.$store.commit(TARGET_PROJECTS, a)
      }
      else {
        this.$store.commit(TARGET_PROJECTS, this.defaultItem)
      }
    },

    onOptionClick() {
      this.$router.push({
        name: 'home',
      }).catch(() => {})
    },

    refresh(refresh) {
      const authService = getInstance()
      authService.refresh(refresh)
        .then((token) => {
        localStorage.token = token
      })
    },

    async onEnter() {
      console.log(this.queryString)
      console.log(this.projectString)
      console.log(this.searchOptions)

      if(localStorage.refresh)
        this.refresh(localStorage.refresh)

      this.$router.push({
        name: 'search',
        query: {
          q: this.queryString,
          p: this.projectString,
          ...this.searchOptions
        }
      }).catch(() => {})
    }
  },

  created() {
    this.setDefaultValue()
  },

  mounted() {
  }
}

</script>
