<template>
  <div class='container'>
    <div class='content'>
      <div class="w-100 flex flex-row">
        <div class="flex ma2"
          style="min-width: 300px"
        >
        <text-label
          style="width: 200px"
          text='Mantis Url' />

        <text-input v-model="mantisUrl"
          readonly=true
          placeHolder='mantis ticket id'
          style="width: 500px"
          />
        </div>
      </div>

      <div class="dark-gray f4 normal mt0 bb b--silver" />
       
      <div class="w-100 flex flex-row">
        <div class="flex ma2"
          style="min-width: 300px"
        >

        <text-label
          style="width: 200px"
          text='Target Project' />
          <v-treeview
            v-model="selectedProject"
            :style="treeViewStyle"
            selectable
            selected-color="red"
            :items="items"
          />
        </div>
      </div>
      <div class="dark-gray f4 normal mt0 mb4 pv4 bb b--silver" />
      <!-- table -->
    </div>
  </div>
</template>

<style scoped>

.container {
  width: 100%;
  display: flex;
}

.content {
  position: relative;
  //overflow-y: scroll;
  width: 100%;
}

</style>

<script>

import SideBar from '@/components/SideBar'
import TextInput from '@/components/TextInput'
import ClickButton from '@/components/ClickButton'
import TextLabel from '@/components/TextLabel'
import ScoreTableRow from '@/components/ScoreTableRow'
import SelectMenu from '@/components/SelectMenu'
import CheckboxLabel from '@/components/CheckboxLabel'

import {
	TARGET_PROJECTS
} from '../store/modules/mutation-types'

import projectTreeItem from '@/constants/projectTreeItem'

export default {

  data: () => ({
    searchTextFieldStyle: {
      borderRadius: "28px"
    },
    mantisUrl: 'http://10.156.2.84/mantis/ipf3/app',
    results: [],
    treeViewStyle: {
      overflowY: 'auto',
      width: '100%',
      height: '100%'
    },
  }),

  computed: {
    selectedProject: {
      set(value) {
        this.$store.commit(TARGET_PROJECTS, value)
      },
      get() {
        return this.$store.state.search_result.targetProjects
      }
    },
    items() {
      return projectTreeItem
    }
  },

  methods: {

    getSelectedColumn() {
      let checkedNames = this.$store.state.target_checkbox.checkedNames
      let m = checkedNames.length
      let column = []
      if(m == 1)
        return checkedNames[0]

      if(checkedNames.includes('summary'))
        column.push('s')
      if(checkedNames.includes('description'))
        column.push('d')
      if(checkedNames.includes('steps_to_reproduce'))
        column.push('s')

      return column.join("_")
    },
  },

  mounted() {
  },

  components: {
    SideBar,
    TextInput,
    ClickButton,
    TextLabel,
    ScoreTableRow,
    SelectMenu,
    CheckboxLabel,
  }
}
</script>
