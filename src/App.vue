<template>
  <div>
    <navigation-header-bar/>

    <div class='container'>
      <div class='content'>

        <div class="w-100 flex">
          <text-label text='Mantis Url' />
          <text-input v-model="mantisUrl"
            placeHolder='mantis ticket id'
            style="width: 500px"
            />
        </div>

        <div class="dark-gray f4 normal mt0 mb4 pv4 bb b--silver" />
        <div class="w-100 flex">
          <text-label text='Mantis Ticket Id' />
          <text-input v-model="mantisId"
            placeHolder='mantis ticket id'
            style="width: 100px"
            />

          <text-label text='Text Phrase' />
          <text-input v-model="textPhrase"
            placeHolder='text phrase'
            style="width: 500px"
            />
        </div>

        <div class="dark-gray f4 normal mt0 mb4 pv4 bb b--silver" />
       
        <div class="w-100 flex">
          <text-label text='Target Project' />
          <text-input v-model="projectName"
            placeHolder='target project name'/>

          <text-label text='Target Column' />
          <select-menu
            v-model="selected"
            :options="columnOptions" />
          
        </div>

        <div class="dark-gray f4 normal mt0 mb4 pv4 bb b--silver" />

        <div class="w-100 flex">
          <text-label text='Ticket Number to Show' />
          <text-input
            v-model="numberToShow"
            style="width: 50px;"/>

          <div>
            <input type="radio"
              v-model='method'
              id="byIdCheckBox"
              name="method"
              value="id">
            <label for="vehicle1"> By Id</label><br>

            <input type="radio"
              v-model='method'
              id="byTextCheckBox"
              name="method"
              value="text">
            <label for="vehicle2"> By text phrase</label><br>
          </div>
          <click-button
            text='calculate'
            @click='onClick'/>
        </div>

        <!-- table -->
        <div class="dt bg-lightest-silver ba b--silver"
          style="width: 100%;">

          <score-table-row
            text="Mantis Ticket Url"
            score="Score"/>

          <score-table-row v-for="(result, index) in results"
            :key="index"
            :url="result.href"
            :score="result.score"
          />
        </div>
      </div>
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
  overflow-y: scroll;
  width: 100%;
  height: calc(100vh - 70px);
}

</style>

<script>

import NavigationHeaderBar from '@/components/NavigationHeaderBar'
import SideBar from '@/components/SideBar'
import TextInput from '@/components/TextInput'
import ClickButton from '@/components/ClickButton'
import TextLabel from '@/components/TextLabel'
import ScoreTableRow from '@/components/ScoreTableRow'
import SelectMenu from '@/components/SelectMenu'

export default {

  data: () => ({
    taskData: 'Hello',
    projectName: 'CV2K_App',
    mantisUrl: 'http://10.156.2.84/mantis/ipf3/app',
    mantisId: '46914',
    textPhrase: 'ユーザー設定画面を操作中に、モダコンの接続が切 れて',
    method: 'id',
    results: [],
    columnOptions: [
      { value: 'summary', text: '要約' },
      { value: 'description', text: '詳細' },
      { value: 'steps_to_reproduce', text: '再現方法' },
    ],
    selected: 'description',
    numberToShow: '130'
  }),

  methods: {
    waitForTaskSuccess(task_id) {
      return new Promise( (resolve, reject) => {
        const intervalId = setInterval( async () => {
          const p = await this.axios.get(`/calcsim/${task_id}`)
          if(p.data.status == "success") {
            clearInterval(intervalId)
            resolve(p.data)
          }
        }, 3000)
      })
    },

    async onClick(e) {
      let loader = this.$loading.show()

      this.results = []
      console.log('calculate button click')
      console.log(this.mantisId)
      console.log(this.projectName)
      console.log(this.textPhrase)
      console.log(this.mantisUrl)

      let postData = {
        mantisId: parseInt(this.mantisId),
        projectName: this.projectName,
        textPhrase: this.textPhrase,
        numberToShow: parseInt(this.numberToShow),
        mantisUrl: this.mantisUrl,
        method: this.method,
        column: this.selected,
      }

      const p = await this.axios.post('/calcsim', postData)
      const task_id = p.data.task_id
      const task = await this.waitForTaskSuccess(task_id)
      this.results = task.result
      loader.hide()
    }
  },

  components: {
    NavigationHeaderBar,
    SideBar,
    TextInput,
    ClickButton,
    TextLabel,
    ScoreTableRow,
    SelectMenu,
  }
}
</script>
