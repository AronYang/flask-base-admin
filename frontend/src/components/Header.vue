<template>
  <header class="app-header navbar">
    <button class="navbar-toggler mobile-sidebar-toggler d-lg-none" type="button" @click="mobileSidebarToggle">&#9776;</button>

    <b-link class="navbar-brand text-center text-warning" to="/" >WeLAB</b-link>
    <!-- <b-link to="#"> <span style="width:155px;height:55px;    padding: 0.5rem 1rem;">NEO</span> </b-link> -->
    <button class="navbar-toggler sidebar-toggler d-md-down-none" type="button" @click="sidebarMinimize">&#9776;</button>


<!--     <b-nav is-nav-bar class="d-md-down-none">
      <b-nav-item class="px-3">Dashboard</b-nav-item>
      <b-nav-item class="px-3">Users</b-nav-item>
      <b-nav-item class="px-3">Settings</b-nav-item>
    </b-nav> -->
    <b-nav is-nav-bar class="ml-auto">
<!--       <b-nav-item class="d-md-down-none">
        <i class="icon-bell"></i><span class="badge badge-pill badge-danger">5</span>
      </b-nav-item>
 -->
<!--       <b-nav-item class="d-md-down-none">
        <i class="icon-list"></i>
      </b-nav-item>
 -->
 <!--       <b-nav-item class="d-md-down-none">
        <i class="icon-location-pin"></i>
      </b-nav-item> -->
      <b-nav-item-dropdown right>
        <template slot="button-content">
          <img src="static/img/avatars/6.jpg" class="img-avatar" alt="admin@bootstrapmaster.com">
          <span class="d-md-down-none">{{username}}</span>
        </template>
<!--         <b-dropdown-header class="text-center"><strong>Account</strong></b-dropdown-header>
        <b-dropdown-item><i class="fa fa-bell-o"></i> Updates<span class="badge badge-info">42</span></b-dropdown-item>
        <b-dropdown-item><i class="fa fa-envelope-o"></i> Messages<span class="badge badge-success">42</span></b-dropdown-item>
        <b-dropdown-item><i class="fa fa-tasks"></i> Tasks<span class="badge badge-danger">42</span></b-dropdown-item>
        <b-dropdown-item><i class="fa fa-comments"></i> Comments<span class="badge badge-warning">42</span></b-dropdown-item>
        <b-dropdown-header class="text-center"><strong>Settings</strong></b-dropdown-header>
        <b-dropdown-item><i class="fa fa-user"></i> Profile</b-dropdown-item>
        <b-dropdown-item><i class="fa fa-wrench"></i> Settings</b-dropdown-item>
        <b-dropdown-item><i class="fa fa-usd"></i> Payments<span class="badge badge-default">42</span></b-dropdown-item>
        <b-dropdown-item><i class="fa fa-file"></i> Projects<span class="badge badge-primary">42</span></b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item><i class="fa fa-shield"></i> Lock Account</b-dropdown-item>
 -->
        <b-dropdown-item  @click="to_my_info"><i class="fa fa-user"></i> 个人信息</b-dropdown-item>
        <b-dropdown-item  @click="to_modify_password"><i class="fa fa-wrench"></i> 修改密码</b-dropdown-item>
        <b-dropdown-item  @click="to_ssh_users"><i class="fa fa-wrench"></i> SSH帐户</b-dropdown-item>
        <b-dropdown-item  @click="logout"><i class="fa fa-lock"></i> 登出</b-dropdown-item>

      </b-nav-item-dropdown>
    </b-nav>&nbsp&nbsp
    <!-- <button class="navbar-toggler aside-menu-toggl  er d-md-down-none" type="button" @click="asideToggle">&#9776;</button> -->

  </header>
</template>


<script>

export default {
  name: 'header',
  data(){
    return {
      username:'',
    }
  },
  methods: {
    sidebarToggle (e) {
      e.preventDefault()
      document.body.classList.toggle('sidebar-hidden')
    },
    sidebarMinimize (e) {
      e.preventDefault()
      document.body.classList.toggle('sidebar-minimized')
    },
    mobileSidebarToggle (e) {
      e.preventDefault()
      document.body.classList.toggle('sidebar-mobile-show')
    },
    asideToggle (e) {
      e.preventDefault()
      document.body.classList.toggle('aside-menu-hidden')
    },
    logout(){
      this.$store.commit('logout')
      this.$router.push('/pages/login')
    },
    get_user(){
      this.username = localStorage.username
    },
    to_my_info(){
      //跳转到修改个人信息
      this.$router.push({name:'个人信息'})
    },
    to_modify_password(){
      this.$router.push({name:'修改密码'})
    },
    to_ssh_users(){
      this.$router.push({name:'SSH帐户'})
    }
  },
  mounted(){
    this.get_user()
  },

}
</script>
