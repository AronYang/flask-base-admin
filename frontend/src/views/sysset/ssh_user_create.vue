<template>
  <div class="card">
    <div class="card-body">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">


        <el-form-item label="用户名称" prop="username">
          <el-input v-model.trim="ruleForm.username"></el-input>
        </el-form-item>

        <el-form-item label="登陆">
        <template>
          <el-radio v-model="ruleForm.login_type" label="1">使用密码</el-radio>
          <el-radio v-model="ruleForm.login_type" label="2">使用key</el-radio>
        </template>
        </el-form-item>

        <el-form-item label="密码"  prop="password" v-if="ruleForm.login_type == '1'">
          <el-input type="password" v-model.trim="ruleForm.password"></el-input>
        </el-form-item>

        <el-form-item label="私钥内容" prop="key" v-if="ruleForm.login_type == '2'">
          <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 10}" v-model.trim="ruleForm.key"></el-input>
        </el-form-item>

        <el-form-item label="用户说明">
          <el-input v-model.trim="ruleForm.describe" type='textarea' autosize></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">保存</el-button>
          <!-- <el-button @click="resetForm('ruleForm')">清空</el-button> -->
        </el-form-item>
      </el-form>
      </el-form>
    </div>
  </div>
</template>
<script>
import { SyssetSshUserApi } from '@/http/url'
export default {
  name: 'scriptCreate',
  data() {
    return {
      ruleForm: {
        login_type:'1',
        username: '',
        password: '',
        key: '',
        describe: '',
      },
      rules: {
        username: { required: true, message: '请输入ssh用户', trigger: 'blur' },
        password: { required: true, message: '请输入密码', trigger: 'blur' },
        key: { required: true, message: '请输入密钥', trigger: 'blur' },
      },
    }
  },
  computed:{
  },
  methods: {

    submitForm(formName) {
      // 提交按钮
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.create_ssh_user()
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    create_ssh_user() {
      var self = this
      this.$http.post(SyssetSshUserApi, this.ruleForm).then(function(response) {
        self.$message(response.data.msg)
        if (response.data.status == 1) {
          ///如果提交成功，则返回到上一次路径
          self.$router.go(-1)
        }
      })
    },
  },
  mounted() {

  }
}

</script>
