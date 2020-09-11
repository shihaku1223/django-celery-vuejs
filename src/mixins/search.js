export default {
  methods: {
    searchKeyword(query, projects, targets, options) {
      if(projects === undefined)
        projects = ""

      return this.axios.post(
          `/search/?q=${query}&p=${projects}&s=${targets}`,
          options)
    },

    scroll(scroll_id) {
      return this.axios.get(`/search/${scroll_id}`)
    },

    getSelectedProjectNames(itemList, selectedItems, projectNames) {
      if (itemList.length == 0)
        return

      for(let i = 0; i < itemList.length; i++) {
        let item = itemList[i]

        if(selectedItems.includes(item.id)) {
          projectNames.push(item.name)    
        }

        if(item.children !== undefined) {
          let result = this.getSelectedProjectNames(
            item.children, selectedItems, projectNames)
        }
      }
    },
  },
}
