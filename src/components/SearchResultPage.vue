<template>
	<div>
		<v-list>
			<search-result-item v-for="(result, index) in displayResult"
				:result="result"
				:key="index"
			/>
		</v-list>

		<v-pagination
			v-model="page"
			:length="pageLength">
		</v-pagination>
</div>

</template>

<script>

import SearchMixin from '../mixins/search'
import { SEARCH_RESULT, QUERY_STRING } from '../store/modules/mutation-types'

import SearchResultItem from './SearchResultItem'

export default {

  data: () => ({
		perPageCount: 30,
		page: 1,
    queryResult: []
  }),

  mixins: [ SearchMixin ],

	computed: {
		pageLength() {
			return Math.ceil(this.searchResult.length/this.perPageCount)
		},
		displayResult() {
			let begin = this.perPageCount * (this.page - 1)
			return this.searchResult.slice(begin, begin + this.perPageCount)
		},
		searchResult() {
			return this.$store.state.search_result.searchResult
		}
	},

	watch: {
		query(to, from) {
			this.search(to)
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
		async search(queryString, projects) {
      const response = await this.searchKeyword(queryString, projects)
      this.$store.dispatch(SEARCH_RESULT, response.data.result)
		},
	},
  mounted() {
    this.$store.commit(QUERY_STRING, this.query)
		this.search(this.query, this.projects)
  },

  components: {
		SearchResultItem
	}
}
</script>
