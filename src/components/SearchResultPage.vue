<template>
	<div>
    <div class=message v-if="fetchedResult.length != 0">
      {{ searchResultMessage }}
    </div>
    <!--
    <button class="hk-button-sm--primary"
      @click="onClick">test
    </button>
    -->

    <DynamicScroller
      ref="scroller"
      class="scroller"
      :items="fetchedResult"
      :min-item-size="54"
      key-field="_id"
    >
      <template v-slot="{ item, index, active }">

        <DynamicScrollerItem
          :item="item"
          :active="active"
          :data-index="index"
          :title="`title${index}${active}`"
          key-field="_id"
        >
          <!--
          <div
            class="message"
            :style="{
              height: `30px`,
            }"
          >
            {{ item.id }}
          </div>

          -->

          <search-result-item
            :result="item"
            :key="index"
            :keywords="keywords"
            :targets="targets"
          />

        </DynamicScrollerItem>
      </template>
      <template #after>
        <div class="loading-circular"
          v-if="isFetching"
          >
          <v-progress-circular
            indeterminate
          ></v-progress-circular> 
        </div>
      </template>
    </DynamicScroller>  
</div>

</template>

<style scoped>
.scroller {
  height: 100%;
}

.message {
  padding: 10px 10px 9px;
  border-bottom: solid 1px #eee;
  justify-content: center;
  display: flex;
  align-items: center;
}

.loading-circular {
  padding: 10px 10px 9px;
  justify-content: center;
  display: flex;
  align-items: center;
}

</style>

<script>

import SearchMixin from '../mixins/search'
import { SEARCH_RESULT, QUERY_STRING } from '../store/modules/mutation-types'

import SearchResultItem from './SearchResultItem'

export default {

  data: () => ({
    perPageCount: 50,
    queryResult: [],
    keywords: [],
    fetchedResult: [],
    hitCount: undefined,
    scrollId: undefined,
    fetching: false,
    searchSources: [
      "id",
      "summary",
      "project",
      "reporter.real_name",
      "handler.real_name",
      "description",
      "steps_to_reproduce",
      "additional_information",
      "notes.text"
    ],
    targets: [
      "summary",
      "description",
      "steps_to_reproduce",
      "additional_information",
      "notes.text"
    ]
  }),

  mixins: [ SearchMixin ],

	computed: {

    pageLength() {
      return Math.ceil(this.searchResult.length/this.perPageCount)
    },

    searchResultMessage() {
      if(this.hitCount == 0)
        return `${this.query} に一致する情報は見つかりませんでした。`
      return `約${this.hitCount}件`
    },

    displayResult() {
      return this.fetchedResult
    },
    searchResult() {
      return this.$store.state.search_result.searchResult
    },
    isFetching() {
      return this.fetching
    }
	},

  watch: {
    query(to, from) {
      this.search(to, this.projects, this.searchSources)
    },
    projects(to, from) {
      this.search(this.query, to, this.searchSources)
    }
  },

  props: {
    query: {
      type: String
    },
    projects: {
      type: String
    }
  },

	methods: {
    async search(queryString, projects, targets) {
      let a =  queryString.trim().split(/\s+/)
      const regex = RegExp(/^-/);
      let keywords = a.filter((term) => {
        return !regex.test(term)
      })
      this.keywords = keywords.map((e) => {
        return e.replace(/\"/g, "")
      })

      this.fetching = true
      const response = await this.searchKeyword(
        queryString, projects, targets.join(','))
      this.fetching = false

      this.hitCount = response.data.total
      this.scrollId = response.data.scroll_id

      this.$store.dispatch(SEARCH_RESULT, response.data.result)
      this.appendResult()
    },

    scrollToBottom () {
      this.$refs.scroller.scrollToBottom()
    },

    async scrollNextResult() {
      if(this.scrollId === undefined)
        return
      if(this.fetching)
        return

      this.fetching = true
      try {
        let r = await this.scroll(this.scrollId)
        this.scrollId = r.data.scroll_id
        this.$store.dispatch(SEARCH_RESULT, r.data.result)
        this.appendResult()
      } catch(e) {
        console.log('scroll error', e)
      }

      this.fetching = false
    },

    onClick() {
      this.scrollNextResult()
    },

    appendResult() {
      if(this.searchResult === undefined)
        return

      if(this.searchResult === null)
        return

      if(this.searchResult.length == 0)
        return

      this.searchResult.forEach((result) => {
        this.fetchedResult.push({
          _id: this.fetchedResult.length + 1,
          ...result
        })
      })

      this.scrollToBottom()
    },

    handleScroll(ev) {
      let scrollBottomY = document.documentElement.scrollHeight -
        document.documentElement.clientHeight

      let diff = scrollBottomY - window.scrollY
      //let circular = this.$el.querySelector('.loading-circular')
      if(diff < scrollBottomY / 5) {
        console.log('fetching')
        this.scrollNextResult()
      }
    }
  },
  
  beforeUpdate() {
  },

  updated() {
  },

  created() {
    window.addEventListener('scroll', this.handleScroll);
  },

  destroyed() {
    window.removeEventListener('scroll', this.handleScroll);
  },

  mounted() {
    this.$store.commit(QUERY_STRING, this.query)
    this.search(this.query, this.projects, this.searchSources)
   },

  components: {
		SearchResultItem
  }
}
</script>
