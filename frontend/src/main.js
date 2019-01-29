// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App'
import router from './router'
import store from './store'
// import VueRouter from 'vue-router'
import axios from './http'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import DataTables from 'vue-data-tables'
// import go from 'gojs'
// import Sticky from 'vue-sticky-position'
// var VueClipboard = require('vue-clipboard')


Vue.use(ElementUI)
Vue.use(BootstrapVue)
Vue.use(DataTables)
// Vue.use(go)
// Vue.use(Sticky)


// Vue.use(store)
Vue.prototype.$http = axios
Vue.prototype.$store = store
// Vue.prototype.$go = go
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {
    App
  }
})
