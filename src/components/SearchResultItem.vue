<template>
  <v-card>
    <v-row
      no-gutters
    >
      <v-col
        cols="9"
      >
        <v-card
          outlined
        >
         {{ result.id }}
        </v-card>
      </v-col>

      <v-col
        cols="3"
      >
        <v-card
          outlined
        >
          {{ result.project.name + '/' +  result.handler.real_name }}
        </v-card>
      </v-col>
    </v-row>

    <highlight-text v-for="(item, index) in highlightTexts"
      v-show="item.text"
      :title="item.title"
      :text="item.text"
      :key="index"
      :queries="keywords"
    />

  </v-card>
</template>

<style scoped>

</style>

<script>

import HighlightText from '@/components/HighlightText'

export default {

  data:() => ({
    text: undefined,
  }),

  props: [ 'result', 'keywords', 'targets' ],

  created() {
  },

  computed: {
    highlightTexts() {
      return this.findKeywords(this.result, this.keywords)
    }
  },

  methods: {
    searchKeywordIndex(s, key) {
      if(typeof s !== "string") {
        return undefined
      }
      let reg = RegExp(key, 'i')
      if(reg.test(s)) {
        let index = reg.exec(s).index
        return index
      }

      return undefined
    },

    getPropertyByPath(obj, path) {
      path = path.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
      path = path.replace(/^\./, '');           // strip a leading dot
      let a = path.split('.');

      let text = ""

      for(let i = 0; i < a.length; i++) {
        let key = a[i]
        if(Array.isArray(obj)) {
          obj.forEach((e) => {
            if(key in e) {
              obj = e[key]
              text += obj
            }
          })
        }

        else if(key in obj) {
          obj = obj[key]
        } else {
          return
        }
      }
      if(text != "")
        return text
      return obj
    },

    findTextWithKeywords(target, keywords, highlightItemList) {
      let text = this.getPropertyByPath(this.result, target)

      let indices = keywords.map((keyword) => {
          return this.searchKeywordIndex(text, keyword)
        })
        .filter(index => index !== undefined)
        .sort((x, y) => {
          return x - y
        })

      if(indices.length > 0) {
        let begin = indices[0] - 10
        let last = indices[indices.length - 1]

        if(begin < 0)
          begin = 0

        highlightItemList.push({
          "title": target,
          "text": text.slice(begin, last + 300)
        })
      }
    },

    traversalObject(obj) {
      Object.keys(obj).forEach((key) => {
        console.log(key)
        this.traversalObject(obj[key])
      })
    },
    
    findKeywords(result, keywords) {
      
      let highlightItemList = []

      this.targets.forEach((target) => {
        this.findTextWithKeywords(target, keywords, highlightItemList)
      })

      return highlightItemList
    }
  },

  updated() {
  },

  mounted() {
  },
  components: {
    HighlightText,
  }
}
</script>
