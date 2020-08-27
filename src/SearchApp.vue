<template>
  <v-app>

  <div>
    <navigation-header-bar/>

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

        <div class="dark-gray f4 normal mt0 mb4 pv4 bb b--silver" />

        <!-- table -->
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
    searchTextFieldStyle: {
      borderRadius: "28px"
    },
    mantisUrl: 'http://10.156.2.84/mantis/ipf3/app',
    results: [],
    selectedProject: [],
    treeViewStyle: {
      overflowY: 'auto',
      width: '100%',
      height: '100%'
    },
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

    getSelectedProjectNames(itemList, projectNames) {
      if (itemList.length == 0)
        return

      for(let i = 0; i < itemList.length; i++) {
        let item = itemList[i]

        if(this.selectedProject.includes(item.id)) {
          projectNames.push(item.name)    
        }

        if(item.children !== undefined) {
          let result = this.getSelectedProjectNames(item.children, projectNames)
        }
      }
    },
  },

  watch: {

  },

  mounted() {
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
