<template>
  <div>
    <navigation-header-bar/>

    <div class='container'>
      <div class='content'>

        <div class="w-100 flex">
          <text-label text='Mantis Url' />
          <text-input v-model="mantisUrl"
            readonly=true
            placeHolder='mantis ticket id'
            style="width: 500px"
            />
        </div>

        <div class="f4 normal mt0 mb4 pv2" />
       
        <div class="w-100 flex flex-row">
          <div class="flex flex-column h2 ma2"
            style="min-width: 300px"
            >

            <text-label text='Target Project' />
            <text-input v-model="projectName"
              placeHolder='target project name'/>
          </div>
          <div class="flex flex-column h2 ma2"
            style="min-width: 150px"
            >
            <text-label
              style="min-width: 150px"
              text='Target Column' />

            <div class="w-100 flex h2 ma2">
              <checkbox-label v-for="(option, index) in columnOptions"
                class="ma2"
                :key="index"
                :text="option.text"
                :value="option.value"
              />
            </div>
          </div>
        </div>


        <div class="dark-gray f4 normal mt0 mb4 pv4 bb b--silver" />
        <div class="w-100 flex">
          <div class="flex flex-column"
            style="min-width: 150px"
            >
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
          </div>

          <div class="flex flex-column"
            style="min-width: 150px"
            >
            <text-label text='Mantis Ticket Id' />
            <text-label text='Text Phrase' />
          </div>
          <div class="w-100 flex flex-column">
            <text-input v-model="mantisId"
              class="h2 ma2"
              placeHolder='mantis ticket id'
              style="width: 100px"
              :readonly="this.method != 'id'"
              />
            <text-input v-model="textPhrase"
              class="h2 ma2"
              placeHolder='text phrase'
              style="width: 500px"
              :readonly="this.method != 'text'"
              />
          </div>
        </div>


        <div class="dark-gray f4 normal mt0 mb4 pv4 bb b--silver" />

        <div class="w-100 flex flex-row">
          <div class="flex flex-row"
              style="width: 300px;">
            <text-label text='Ticket Number to Show' />
            <text-input
              v-model="numberToShow"
              style="width: 50px;"/>
          </div>
          
          <click-button class="h2 ma2"
            text='search'
            @click='onClick'/>
        </div>

        <div class="dark-gray f4 normal mt0 mb1 pv1" />

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
import CheckboxLabel from '@/components/CheckboxLabel'

export default {

  data: () => ({
    taskData: 'Hello',
    projectName: 'CV2KApp窓口,OTV_PF',
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
    defaultCheckedNames: [
      'description'
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
          if(p.data.status == "failed") {
            clearInterval(intervalId)
            if(p.data.message != '') {
              reject(p.data.message)
            }
            reject("Task " + task_id + " failed")
          }
        }, 3000)
      })
    },

    sendTaskRequest(projectName) {

      let selected = this.getSelectedColumn()

      if(selected.length == 0) {
        return Promise.reject('Please select target to calculate.')
      }

      let postData = {
        mantisId: parseInt(this.mantisId),
        projectName: projectName,
        textPhrase: this.textPhrase,
        numberToShow: parseInt(this.numberToShow),
        mantisUrl: this.mantisUrl,
        method: this.method,
        column: selected,
      }
      return this.axios.post('/calcsim', postData)
      //return Promise.resolve('test')
    },

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

    async onClick(e) {
      let loader = this.$loading.show()
      this.results = []
      console.log('calculate button click')
      console.log(this.mantisId)
      console.log(this.projectName.split(','))
      console.log(this.textPhrase)
      console.log(this.mantisUrl)

      let projectNameList = this.projectName.split(',')
      let requests = projectNameList.map(async (name) => {
          let r = await this.sendTaskRequest(name)
          return this.waitForTaskSuccess(r.data.task_id)
      })

      let tasks = undefined
      try {
        tasks = await Promise.all(requests)
      } catch(err) {
        loader.hide()
        alert(err)
        return
      }

      let result = tasks[0].result

      let numberToShow = parseInt(this.numberToShow)

      let i
      let size = tasks.length
      for(i = 1; i < size; i++) {
        let arr = tasks[i].result
        let l = arr.length
        let j = 0
        let last = 0
        let k = 0

        while(j < l) {
          k = last
          while(k < result.length && k < numberToShow) {

            if(parseFloat(arr[j].score) > parseFloat(result[k].score)) {
              result.splice(k, 0, arr[j])
              last = k + 1
              break
            }
            k++
          }
          if(k >= result.length) {
            let a = arr.slice(j, arr.length)
            result = [...result, ...a]
            break
          }
          j++
        }
      }
      this.results = result.slice(0, numberToShow)
      loader.hide()
    }
  },

  mounted() {
    this.$store.commit('SAVE_CHECKEDNAMES', this.defaultCheckedNames)
  },

  components: {
    NavigationHeaderBar,
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
