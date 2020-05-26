<template>
  <div class='navigation items-stretch bg-purple shadow-outer-1'>I am header
  </div>

</template>

<style scoped>

.items-stretch {
  -ms-flex-align: stretch;
  -webkit-box-align: stretch;
  align-items: stretch;
}

.shadow-outer-1 {
  -webkit-box-shadow: 0 0 0 1px rgba(89,105,129,0.1),0 1px 3px 0 rgba(89,105,129,0.1),0 1px 2px 0 rgba(0,0,0,0.05);
  box-shadow: 0 0 0 1px rgba(89,105,129,0.1),0 1px 3px 0 rgba(89,105,129,0.1),0 1px 2px 0 rgba(0,0,0,0.05);
}

.navigation {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  color: white;
  z-index: 1;

  display: flex;
  height: 70px;
  font-size: 14px;
  font-family: "salesforce-sans", -apple-system, BlinkMacSystemFont, 'avenir next', avenir, helvetica, 'helvetica neue', ubuntu, roboto, noto, 'segoe ui', arial, sans-serif;
}

</style>

<script>

export default {
  name: 'navigation-header-bar',

  data: () => ({
    taskData: 'Hello'
  }),

  computed: {
    headerStype() {
    }
  },

}

</script>
