<template>
  <div>
    <navigation-header-bar/>
    <div class='container'>
      <side-bar/>
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
        </div>

        <div class="dark-gray f4 normal mt0 mb4 pv4 bb b--silver" />

        <div class="w-100 flex">
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
  width: calc(100% - 240px);
  height: calc(100vh - 70px);
}

</style>

<script>

import NavigationHeaderBar from '@/components/NavigationHeaderBar'
import SideBar from '@/components/SideBar'
import TextInput from '@/components/TextInput'
import ClickButton from '@/components/ClickButton'
import TextLabel from '@/components/TextLabel'

export default {

  data: () => ({
    taskData: 'Hello',
    projectName: 'CV2K_App',
    mantisUrl: 'http://10.156.2.84/mantis/ipf3/app',
    mantisId: '46914',
    textPhrase: 'ユーザー設定画面を操作中に、モダコンの接続が切 れて',
    method: 'id',
  }),

  methods: {
    async onClick(e) {
      console.log('calculate button click')
      console.log(this.mantisId)
      console.log(this.projectName)
      console.log(this.textPhrase)
      console.log(this.mantisUrl)

      let postData = {
        mantisId: this.mantisId,
        projectName: this.projectName,
        textPhrase: this.textPhrase,
        numberToShow: 130,
        mantisUrl: this.mantisUrl,
        method: this.method
      }
      const p = await this.axios.post('/calcsim', postData)
      //console.log(p.data)
    }
  },

  components: {
    NavigationHeaderBar,
    SideBar,
    TextInput,
    ClickButton,
    TextLabel,
  }
}
</script>
