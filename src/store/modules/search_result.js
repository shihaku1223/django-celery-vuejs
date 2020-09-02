import {
	SEARCH_RESULT,
	QUERY_STRING,
	TARGET_PROJECTS
} from './mutation-types'

export default {
  state: {
    queryString: undefined,
    searchResult: [],
    targetProjects: [],
  },

  mutations: {
    [SEARCH_RESULT] (state, result) {
      state.searchResult = result
    },
    [QUERY_STRING] (state, queryString) {
      state.queryString = queryString
    },
    [TARGET_PROJECTS] (state, projects) {
      state.targetProjects = projects
    },
  },
  actions: {
    [SEARCH_RESULT] ({ commit, state }, result) {
      commit(SEARCH_RESULT, result)
    },
  }
}
