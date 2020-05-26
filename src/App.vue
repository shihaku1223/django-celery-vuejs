<template>
  <div>
    <navigation-header-bar/>
    <div class='container'>
      <side-bar/>
      <div class='content'>
        <div class="dark-gray f4 normal mt0 mb4 pv4 bb b--silver" />
        <text-input
          placeHolder='mantis ticket id'/>

        <div class="dark-gray f4 normal mt0 mb4 pv4 bb b--silver" />
        <text-input
          placeHolder='text phrase'/>

        <click-button
          text='calculate'
          @click='onClick'/>

        <!--<router-view></router-view> -->
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

export default {

  data: () => ({
    taskData: 'Hello'
  }),

  methods: {
    onClick(e) {
      console.log('calculate button click')
      e.preventDefault()
    }
  },

  components: {
    NavigationHeaderBar,
    SideBar,
    TextInput,
    ClickButton,
  }

}
</script>
