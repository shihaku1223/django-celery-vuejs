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
    targets: [
      "summary",
      "description",
      "steps_to_reproduce",
      "additional_information"
    ]
  }),

  props: [ 'result', 'keywords' ],

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

    findTextWithKeywords(target, keywords, highlightItemList) {

      let indices = keywords.map((keyword) => {
          return this.searchKeywordIndex(this.result[target], keyword)
        })
        .filter(index => index !== undefined)
        .sort()

      if(indices.length > 0) {
        let begin = indices[0] - 10
        let last = indices[indices.length - 1]

        if(begin < 0)
          begin = 0

        highlightItemList.push({
          "title": target,
          "text": this.result[target].slice(begin, last + 300)
        })
      }
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
