<template>

  <li class='nav-item'
    :class="{ active: isActive }"
    @click="onClick">
    <a class='nav-link dark-gray hover-bg-light-silver'
       :href='href'>
      {{ text }}
    </a> 
  </li>

</template>

<style scoped>


.nav-item {

}

.nav-link {
  display: block;
  text-decoration: none;
  line-height: 1.5;

  padding-left: 10px;
  padding-right: 10px;
  padding-top: 5px;
  padding-bottom: 5px;
}

a:active {
 outline:none;
 border-color:#79589f;
 -webkit-box-shadow:0 0 0 2px rgba(157,112,208,0.4);
 box-shadow:0 0 0 2px rgba(157,112,208,0.4)
}

a {
  background-color: transparent;
  font-size: 13px;
}

.sidebar .sidebar-content .active a {
 font-weight:bold;
 background:rgba(255,255,255,0.8)
}

</style>

<script>

export default {
  name: 'navigation-item',

  data: () => ({
  }),

  props: {
    isActive: {
      type: Boolean,
      default: false,
    },
    text: String,
    href: {
      type: String,
      default: "#hello"
    }
  },

  computed: {
  },

  methods: {
    onClick(e) {
      this.$emit('click')
      e.preventDefault()
    }
  }
}

</script>
