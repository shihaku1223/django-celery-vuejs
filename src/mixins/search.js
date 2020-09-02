export default {
  methods: {
    searchKeyword(query) {
      return this.axios.get(`/search/?q=${query}`)
    },
  },
}
