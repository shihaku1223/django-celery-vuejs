import { SEARCH_RESULT, QUERY_STRING } from './mutation-types'

export default {
  state: {
    queryString: undefined,
    searchResult: [],
  },

  mutations: {
    [SEARCH_RESULT] (state, result) {
      state.searchResult = result
    },

    [QUERY_STRING] (state, queryString) {
      state.queryString = queryString
    },
  },
  actions: {
    [SEARCH_RESULT] ({ commit, state }, result) {
      commit(SEARCH_RESULT, result)
    },
  }
}
