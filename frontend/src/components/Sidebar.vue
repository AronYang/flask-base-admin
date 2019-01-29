<template>
  <div class="sidebar">
    <nav class="sidebar-nav">
      <div slot="header"></div>
      <ul class="nav">
        <li class="nav-item" v-for="(item, index) in navItems">

          <template v-if="item.title">
            <SidebarNavTitle :name="item.name"/>
          </template>
          <template v-else-if="item.divider">
            <li class="divider"></li>
          </template>

          <template v-else>
            <template v-if="item.children">
              <SidebarNavDropdown :padding="1" :name="item.name" :url="item.url" v-if="checkAcl(item.url)" :icon="item.icon">
                <template v-for="(child, index) in item.children">

                    <template v-if="child.children">
                      <SidebarNavDropdown :name="child.name" :url="child.url" :icon="child.icon">
                        <li class="nav-item" v-for="(child, index) in item.children">
                          <SidebarNavLink :padding="2" :name="child.name" :url="child.url" v-if="checkAcl(item.url)"  :icon="child.icon" :badge="child.badge"/>
                        </li>
                      </SidebarNavDropdown>
                    </template>

                    <template v-else>
                      <li class="nav-item">
                        <SidebarNavLink :padding="1" :name="child.name" :url="child.url" v-if="checkAcl(item.url)"  :icon="child.icon" :badge="child.badge"/>
                      </li>
                    </template>

                </template>
              </SidebarNavDropdown>
            </template>
            <template v-else>
              <SidebarNavLink :padding="0" :name="item.name" :url="item.url" v-if="checkAcl(item.url)"  :icon="item.icon" :badge="item.badge"/>
            </template>
          </template>
        </li>
      </ul>
      <slot></slot>
      <div slot="footer"></div>
    </nav>
  </div>
</template>
<script>
import SidebarNavDropdown from './SidebarNavDropdown'
import SidebarNavLink from './SidebarNavLink'
import SidebarNavTitle from './SidebarNavTitle'
import {UserGrantsApiUrl} from '@/http/url'


export default {
  name: 'sidebar',
  props: {
    navItems: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  data(){
    return{
      acls:{},
    }
  },
  components: {
    SidebarNavDropdown,
    SidebarNavLink,
    SidebarNavTitle
  },
  methods: {
    handleClick (e) {
      e.preventDefault()
      e.target.parentElement.classList.toggle('open')
    },
    checkAcl(url){
      return true
      if(localStorage.username == 'admin'){return true}
      if(this.acls.hasOwnProperty(url) == true){
        if(this.acls[url].get == true){
          return true
        }
      }
      return false
    },
    get_user_grants_info(){
      var self = this
      self.$http.get(UserGrantsApiUrl).then((response)=>{
        console.log(response.data.result)
        self.acls = response.data.result.acls
        // self.username = response.data.result.username
      })
    }
  },
  mounted(){
    this.get_user_grants_info()
  }
}
</script>

<style lang="css">
  .nav-link {
    cursor:pointer;
  }
</style>
