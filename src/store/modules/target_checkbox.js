import { SAVE_CHECKEDNAMES } from './mutation-types'

export default {
  state: {
    checkedNames: [],
  },

  mutations: {
    [SAVE_CHECKEDNAMES] (state, checkedNames) {
      state.checkedNames = checkedNames
    },
  },
  actions: {
    [SAVE_CHECKEDNAMES] ({ commit, state }, data) {
      console.log(data)
      commit(SAVE_CHECKEDNAMES, data)
    },
  }
}
