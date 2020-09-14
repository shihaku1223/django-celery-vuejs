import {
	SEARCH_RESULT,
	QUERY_STRING,
	TARGET_PROJECTS,
  UPDATE_SEARCH_OPTIONS,
} from './mutation-types'

export default {
  state: {
    queryString: undefined,
    searchResult: [],
    targetProjects: [],
    searchOptions: undefined,
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
    [UPDATE_SEARCH_OPTIONS] (state, option) {
      state.searchOptions = option
    },
  },
  actions: {
    [SEARCH_RESULT] ({ commit, state }, result) {
      commit(SEARCH_RESULT, result)
    },
    [UPDATE_SEARCH_OPTIONS] ({ commit, state }, option ) {
      commit(UPDATE_SEARCH_OPTIONS, option)
    },
  }
}
