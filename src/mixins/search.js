export default {
  methods: {
    searchKeyword(query, projects, targets) {
      return this.axios.get(`/search/?q=${query}&p=${projects}&s=${targets}`)
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
