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
    summary: undefined,
    description: undefined,
    steps_to_reproduce: undefined,
    additional_information: undefined,
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
    isIncludes(s, key) {
      if(typeof s !== "string") {
        console.log('s not string')
        return undefined
      }
      let reg = RegExp(key, 'i')
      if(reg.test(s)) {
        let index = reg.exec(s).index
        if(index - 10 >= 0)
          return s.slice(index - 10, index + 300)
        return s.slice(index, index + 300)
      }

      return undefined
    },
    findKeywords(result, keywords) {
      
      let textList = []
      let summary = undefined
      let description = undefined
      let additional_information = undefined
      let steps_to_reproduce = undefined

      keywords.forEach((keyword) => {
        summary = this.isIncludes(result.summary, keyword)
        description = this.isIncludes(result.description, keyword)
        additional_information =
          this.isIncludes(result.additional_information, keyword)
        steps_to_reproduce = this.isIncludes(result.steps_to_reproduce, keyword)
      })

      textList.push({ "title": "summary", "text": summary })
      textList.push({ "title": "description", "text": description })
      textList.push({
        "title": "additional_information",
        "text": additional_information })
      textList.push({
        "title": "steps_to_reproduce",
        "text": steps_to_reproduce})

      return textList
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
