<template>
  <v-app>

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
          <div class="flex ma2"
            style="min-width: 300px"
            >

            <text-label text='Target Project' />
            <v-treeview
              :style="treeViewStyle"
              selectable
              selected-color="red"
              :items="items"
            />
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

  </v-app>
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
    defaultCheckedNames: [
      'description'
    ],
    selected: 'description',
    treeViewStyle: {
      overflowY: 'auto',
      width: '100%',
      height: '200px'
    },
    numberToShow: '130',
      items: [
        {
          id: 113,
          name: 'CV2K製品',
          children: [
            { id: 205, name: 'CV2KApp窓口' },
            { id: 115, name: 'CV2K_App' },
            { id: 106, name: 'CV2K_App_内部課題',
              children: [
                { id: 144, name: 'CV2K_App_ドメイン間シーケンス試験' },
                { id: 146, name: 'CV2K_App_ドメイン間シーケンス試験_アナスコ' },
                { id: 151, name: 'CV2K_APP_一覧系試験' },
                { id: 142, name: 'CV2K_Arch_QA' },
              ]
            },
            { id: 133, name: 'CV2K_CP',
              children: [
                { id: 134, name: 'CV2K-CP1-RTL' },
                { id: 135, name: 'CV2K-CP2-RTL' },
              ]
            },
            { id: 143, name: 'CV2K_DP' },
            { id: 220, name: 'IPF3CV品提' },
            { id: 154, name: 'IPF3CV本体PF検証' },
            { id: 158, name: 'IPF3CV生試',
              children: [
                { id: 160, name: '01_V字設計レイヤ',
                  children: [
                    { id: 169, name: 'サブシステム',
                      children: [
                        { id: 172, name: 'AP_ACT_生試',
                          children: [
                            { id: 180, name:'コンポーネント単体_AP_ACT' },
                            { id: 179, name:'コンポーネント結合_AP_ACT',
                              children: [
                                { id: 181, name: 'RTL_AP_ACT'},
                                { id: 182, name: 'SWシステム_AP_ACT'},
                                { id: 183, name: 'SW結合_AP_ACT'},
                              ],
                            },
                            { id: 178, name: 'サブシステム結合_AP_ACT' },
                          ]
                        },
                        { id: 174, name: 'CP_PFSW_生試',
                          children: [
                            { id: 193, name: 'コンポーネント単体_CP_PFSW' },
                            { id: 192, name: 'コンポーネント結合_CP_PFSW',
                              children: [
                                { id: 194, name: 'RTL_CP_PFSW' },
                                { id: 195, name: 'SWシステム_CP_PFSW' },
                                { id: 196, name: 'SW結合_CP_PFSW' },
                              ]
                            },
                            { id: 191, name: 'サブシステム結合_CP_PFSW' },
                          ],
                        },
                        { id: 175, name: 'CR_生試',
                          children: [
                            { id: 199, name: 'コンポーネント単体_CR' },
                            { id: 198, name: 'コンポーネント結合_CR',
                              children: [
                                { id: 200, name: 'RTL_CR' },
                                { id: 201, name: 'SWシステム_CR' },
                                { id: 202, name: 'SW結合_CR' },
                              ]
                            },
                            { id: 197, name: 'サブシステム結合_CR' }
                          ]
                        },
                        { id: 173, name: 'DP_生試',
                          children: [
                            { id: 187, name: 'コンポーネント単体_DP' },
                            { id: 186, name: 'コンポーネント結合_DP',
                              children: [
                                { id: 188, name: 'RTL_DP' },
                                { id: 189, name: 'SWシステム_DP' },
                                { id: 190, name: 'SW結合_DP' },
                              ]
                            },
                            { id: 185, name: 'サブシステム結合_DP' }
                          ]
                        },
                        { id: 177, name: 'メカ_生試' },
                        { id: 176, name: '電源_生試' },
                      ]
                    },
                    { id: 168, name: '製品結合' },
                    { id: 167, name: '製品要求仕様' },
                  ]
                },
                { id: 159, name: '02_商品レイヤ',
                  children: [
                    { id: 165, name: 'リスマネ' },
                    { id: 166, name: '取り説' },
                    { id: 164, name: '商品規格' },
                  ]
                },
                { id: 163, name: '03_白河工程' },
                { id: 184, name: '04_会津工程' },
                { id: 162, name: '05_仕様変更' },
                { id: 161, name: '06_SWICT',
                  children: [
                    { id: 211, name: 'V2.10以降',
                      children: [
                        { id: 212, name: 'アプリ' },
                        { id: 213, name: '機能UI' },
                        { id: 214, name: '通信' },
                      ]
                    },
                  ]
                },
                { id: 217, name: '07_課題管理' },
              ]
            },
          ],
        },
        { id: 147, name: 'IPF-3 OTV製品',
          children: [
            { id: 149, name: 'OTV_App',
              children: [
                { id: 208, name: 'OTV_App_SOMED_RTC' },
                { id: 222, name: 'OTV_LS' },
                { id: 221, name: 'OTV_PF' },
              ]
            },
            { id: 148, name: 'OTV_App_内部タスク',
              children: [
                { id: 156, name: 'OTV_Arch_QA' },
                { id: 226, name: 'OTV_PF_内部タスク' },
                { id: 153, name: 'OTV_要件_QA' },
                { id: 223, name: 'OTV_通信仕様_QA' },
                { id: 155, name: 'OTV_開発_備忘録' },
                { id: 224, name: 'OTV_開発試験_QA' },
              ]
            },
          ]
        },
        { id: 145, name: 'Sample_Env' },
        { id: 203, name: 'sandbox_integ' },
        { id: 123, name: 'Simulator',
          children: [
            { id: 124, name: 'Simulator_offshore' },
            { id: 125, name: 'Simulator_QA' },
            { id: 126, name: 'Simulator_課題' },
            { id: 129, name: 'Simulator_障害' },
          ]
        },
        { id: 225, name: 'test_SOMED_RTC' },
        { id: 72, name: 'VE2製品試験',
          children: [
            { id: 14, name: 'App',
              children: [
                { id: 59, name: 'VE2_QA' },
                { id: 2, name: 'VE2_内部課題' },
                { id: 15, name: 'VE2_障害',
                  children: [
                    { id: 62, name: 'VE2_全体',
                      children: [
                        { id: 63, name: 'OffShore 全体' },
                      ]
                    },
                  ]
                },
              ]
            },
            { id: 95, name: 'CP' },
          ],
        },
        { id: 21, name: 'ツール',
          children: [
            { id: 41, name: 'C++Test' },
            { id: 22, name: 'Genware',
              children: [
                { id: 23, name: 'OffShore Genware' }
              ]
            },
          ]
        },
        { id: 157, name: '教育用testPJ' }
      ],
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
    },
    setDefaultValue() {
      if(localStorage.method)
        this.method = localStorage.method

      if(localStorage.projectName)
        this.projectName = localStorage.projectName

      if(localStorage.textPhrase === '')
        this.textPhrase = ''
      else if(localStorage.textPhrase) {
        this.textPhrase = localStorage.textPhrase
      }

      if(localStorage.mantisId)
        this.mantisId = localStorage.mantisId

      if(localStorage.numberToShow)
        this.numberToShow = localStorage.numberToShow

      if(localStorage.checkedNames) {
        this.$store.commit('SAVE_CHECKEDNAMES',
          localStorage.checkedNames.split(','))
      }
      else
        this.$store.commit('SAVE_CHECKEDNAMES',
          this.defaultCheckedNames)
    },
  },

  watch: {
    projectName: (val) => {
      localStorage.projectName = val
    },
    textPhrase: (val) => {
      if(val === '') {
        localStorage.textPhrase = ''
      }
      else
        localStorage.textPhrase = val
    },
    method: (val) => {
      localStorage.method = val
    },
    numberToShow: (val) => {
      localStorage.numberToShow = val
    },
    mantisId: (val) => {
      localStorage.mantisId = val
    },
  },

  mounted() {
    this.setDefaultValue()
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
