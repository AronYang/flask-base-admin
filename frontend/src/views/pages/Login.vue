<template>
  <div class="app flex-row " style="background-color:rgb(30,40,45)">
    <div class="container" style="max-width:700px;margin-top:8%;">
      <div class="row justify-content-center">
        <div class="col-md-8">
        <div class="text-center">
                            <h1 style="color:rgb(232,130,58);">WeLAB</h1>
                            <br>
        </div>
          <div class="card-group mb-0">
            <div class="card p-3">

              <div class="card-body"  @keyup.enter="loginin">
                <!-- <p class="text-muted">Sign In to your account</p> -->
                <div class="input-group mb-3">
                  <span class="input-group-addon"><i class="icon-user"></i></span>
                  <input type="text" class="form-control" placeholder="用户名" v-model="username">
                </div>
                <div class="input-group mb-4">
                  <span class="input-group-addon"><i class="icon-lock"></i></span>
                  <input type="password" class="form-control" placeholder="密码" v-model="password">
                </div>
                <div class="row">
                  <div class="col-6">
                    <!-- <button type="button text-right" class="btn btn-primary px-4">Login</button> -->
                  </div>
                  <div class="col-6 text-right">
                    <button type="button text-right" class="btn btn-primary px-4" @click="loginin">登陆</button>

                    <!-- <button type="button" class="btn btn-link px-0">Forgot password?</button> -->
                  </div>
                </div>
              </div>
            </div>
<!--             <div class="card text-white bg-primary py-5 d-md-down-none" style="width:44%">
              <div class="card-body text-center">
                <div>
                  <h2>Sign up</h2>
                  <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                  <button type="button" class="btn btn-primary active mt-3">Register Now!</button>
                </div>
              </div>
            </div> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    loginin () {
      console.log(this.username + this.password)
      let self = this

      this.$http.post('/api/token',{username:self.username,password:self.password}).then(function (response) {
        // 存储token
        console.log(response)
        self.$store.commit('login', {'username':self.username,'token':response.data.token} )
        // localStorage.token = response.data.token
        // localStorage.username = self.username

        if (self.$route.query.redirect != undefined){
          self.$router.push(self.$route.query.redirect)
        }else{
          self.$router.push('/')
        }
      }).catch(function (error) {
        console.log(error)

        self.$message.error('用户名或密码错误！')
      })
    }
  }
}
</script>
