<template>
  <div class="card">
    <div class="card-body">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">
        <el-form-item label="旧密码" prop="oldpwd">
          <el-input v-model.trim="ruleForm.oldpwd" type='password'></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop='newpwd1'>
          <el-input v-model.trim="ruleForm.newpwd1" type='password'></el-input>
        </el-form-item>
        <el-form-item label="重复新密码" prop='newpwd2'>
          <el-input v-model.trim="ruleForm.newpwd2" type='password'></el-input>
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
import { UserPasswordApiUrl } from '@/http/url'
export default {
  name: 'mypassword',
  data() {
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.ruleForm.newpwd1) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        oldpwd:'',
        newpwd1:'',
        newpwd2:'',
      },
      rules: {
        oldpwd: { required: true, message: '请输入旧密码', trigger: 'blur' },
        newpwd1: { required: true, min:8, message: '密码长度最小为8位', trigger: 'blur' },
        newpwd2: { validator: validatePass2, required:true, trigger: 'blur' },
      },
    }
  },
  methods: {
    submitForm(formName) {
      // 提交按钮
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.modify_password()
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    modify_password() {
      var self = this
      this.$http.put(UserPasswordApiUrl, this.ruleForm).then(function(response) {
        if (response.data.status == 1){
          self.$alert(response.data.msg)
          self.ruleForm.oldpwd=''
          self.ruleForm.newpwd1=''
          self.ruleForm.newpwd2=''
        }else{
          self.$alert(response.data.msg)
        }
      })
    },
  },
}

</script>
