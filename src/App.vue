<template>
  <div>
    <navigation-header-bar/>
    <div class='container'>
      <side-bar/>
      <div class='content'>
        I am content
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

export default {

  data: () => ({
    taskData: 'Hello'
  }),

  components: {
    NavigationHeaderBar,
    SideBar,
  }

}
</script>
