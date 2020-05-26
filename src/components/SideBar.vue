<template>
  <div class='sidebar bg-lightest-silver br b--silver'>
    <ul class='nav sidebar-content'>
      <navigation-item v-for="(item, index) in sideBarNavItemTitles"
        :text="item.text"
        :href="item.href"
        :key="index"
        :isActive="navItemActives[index]"
        @click="onNavItemClick(index)"
      />
    </ul>
  </div>

</template>

<style scoped>

.sidebar {
  position: relative;

  /* grow shrink basis */
  flex: 1 0 240px;
  flex-direction: column;
}

.sidebar .sidebar-content {
  position: -webkit-sticky;
  position: sticky;
  top: 70px;
  margin: 0px;

  height: calc(100vh - 70px);
  overflow: scroll;

  padding-left: 0;
  padding-right: 0;
  padding-top: 10px;
  padding-bottom: 10px;
  list-style-type: none;
}

@media (max-width: 720px) {
 .sidebar {
  -webkit-box-flex:1;
  -ms-flex:1 0 160px;
  flex:1 0 160px
 }
}

@media (max-width: 720px) {
 .sidebar .sidebar-content {
  top:100px;
  height:calc(100vh - 100px)
 }
}

</style>

<script>

import NavigationItem from '@/components/NavigationItem'

export default {
  name: 'side-bar',

  data: () => ({
    sideBarNavItemTitles: [
      { text: 'Home', href: '#home' },
      { text: 'About', href: '#about' }
    ],
    navItemActives: [],
    taskData: 'Hello'
  }),

  computed: {
    headerStype() {
    }
  },

  components: {
    NavigationItem,
  },

  created() {
    this.navItemActives = new Array(
      this.sideBarNavItemTitles.length).fill(false)
  },

  methods: {
    onNavItemClick(index) {
      this.navItemActives =
        [...this.navItemActives.values()].map((value, idx) => {
          return idx == index
      })
    }
  }

}

</script>
