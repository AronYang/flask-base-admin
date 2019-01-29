<template>
  <div class="card">
    <div class="card-body">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">


        <el-form-item label="变量名称" prop="name">
          <el-input v-model.trim="ruleForm.name" placeholder="建议全部大写"></el-input>
        </el-form-item>

        <el-form-item label="值"  prop="value">
          <el-input  v-model.trim="ruleForm.value"></el-input>
        </el-form-item>

        <el-form-item label="选择机房" prop='idc_id'>
          <el-select v-model="ruleForm.idc_id" filterable clearable style="width:100%">
                <el-option label="默认" value=""></el-option>
                <el-option v-for="idc in idc_list" :key="idc.id" :label="idc.name" :value="idc.id"> </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="变量说明">
          <el-input v-model.trim="ruleForm.remark" type='textarea' autosize></el-input>
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
import { SyssetVariableApi, IdcApi } from '@/http/url'
export default {
  name: 'variableCreate',
  data() {
    return {
      ruleForm: {
        name: '',
        value: '',
        idc_id: '',
        remark: '',
      },
      idc_list:[],
      rules: {
        name: { required: true, message: '请输入', trigger: 'blur' },
        value: { required: true, message: '请输入值', trigger: 'blur' },
        // idc_id: { required: true, type:'number',message: '请选择机房', trigger: 'change' },
      },
    }
  },
  computed:{
  },
  methods: {
        get_idc_list() {
            //获取idc的列表，并改为text,value格式，方便页面做过滤。
            var self = this
            this.$http.get(IdcApi).then(function(response) {
                self.idc_list = response.data.result
            })
        },
        submitForm(formName) {
          // 提交按钮
          var self = this
          this.$refs[formName].validate((valid) => {
            if (valid) {
              self.create_variable()
            } else {
              console.log('error submit!!');
              return false;
            }
          });
        },
        create_variable() {
          var self = this
          this.$http.post(SyssetVariableApi, this.ruleForm).then(function(response) {
            self.$message(response.data.msg)
            if (response.data.status == 1) {
              ///如果提交成功，则返回到上一次路径
              self.$router.go(-1)
            }
          })
        },
  },
  mounted() {
    this.get_idc_list()
  }
}

</script>
