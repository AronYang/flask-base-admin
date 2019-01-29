<template>
  <div class="card">
    <div class="card-body">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">
        <el-form-item label="环境名称" prop="name">
          <el-input v-model.trim="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="说明" >
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
import { EnviromentListApiUrl,EnviromentsPage } from '@/http/url'
export default {
  name: 'submitCreate',
  data() {
    return {
      ruleForm: {
        name: '',
        describe: '',
      },
      rules: {
        name: { required: true, message: '请输入名称', trigger: 'blur' },
        describe: { required: true, message: '请输入提交原因', trigger: 'blur' },
      },
    }
  },
  methods: {
    submitForm(formName) {
      // 提交按钮
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.create_enviroment()
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    create_enviroment() {
      var self = this
      this.$http.post(EnviromentListApiUrl, this.ruleForm).then(function(response) {
        self.$message(response.data.msg)
        if (response.data.status == 1) {
          self.$router.push(EnviromentsPage)
        }
      })
    },
  },
}

</script>
