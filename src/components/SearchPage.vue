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

        <div class="ma2 flex-col right-options">

          <label-combobox
            title="ステータス"
            :items="statusItems"
            v-model="selectedStatus"
            />

          <label-combobox
            title="解決状況"
            :items="resolutionItems"
            v-model="selectedResolution"
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

.right-options {
  align-items: flex-start;
  flex-grow: 2;
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

import LabelCombobox from '@/components/LabelCombobox'

import {
	TARGET_PROJECTS
} from '../store/modules/mutation-types'

import projectTreeItem from '@/constants/projectTreeItem'
import mantisUrl from '@/constants/mantisUrl'

export default {

  data: () => ({
    searchTextFieldStyle: {
      borderRadius: "28px"
    },
    results: [],
    treeViewStyle: {
      overflowY: 'auto',
      width: '100%',
      height: '100%'
    },
    selectedStatus: undefined,
    statusItems: [
      "全て",
      "新規",
      "内容確認済",
      "担当者決定",
      "要追加情報",
      "調査中",
      "修正中",
      "要方向付け",
      "修正済",
      "解決済",
      "完了",
    ],
    selectedResolution: undefined,
    resolutionItems: [
      "全て",
      "対処中",
      "実装済",
      "差戻し",
      "再現不可",
      "二重登録",
      "変更不要",
      "原因の重複",
      "誤登録",
      "次版で対応",
      "次製品で対応",
    ],
  }),

  watch: {
    selectedStatus(to) {
      console.log(to)
    },
    selectedResolution(to) {
      console.log(to)
    }
  },

  computed: {
    mantisUrl() {
      return mantisUrl
    },
    selectedProject: {
      set(value) {
        console.log(value)
        this.$store.commit(TARGET_PROJECTS, value)
        localStorage.selectedProjects = value
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
    LabelCombobox,
  }
}
</script>
