<template>
  <div class="card">
    <div class="card-body">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">
        <el-form-item label="节点名称" prop="name">
          <el-input v-model.trim="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="审核人" prop='operators'>
          <!-- <el-input v-model.trim="ruleForm.operators" type='textarea' autosize></el-input> -->
          <el-select v-model="ruleForm.operators" multiple placeholder="请选择" style="width:100%">
            <el-option
              v-for="user in user_list"
              :key="user.id"
              :label="user.name"
              :value="user.id">
            </el-option>
          </el-select>

        </el-form-item>

        <el-form-item label="审核类型" prop='step_type'>
          <template>
            <el-radio-group v-model="ruleForm.step_type">
              <el-radio label="0">任一成员通过</el-radio>
              <el-radio label="1">所有成员通过</el-radio>
            </el-radio-group>
          </template>
        </el-form-item>


        <el-form-item label="描述">
          <el-input v-model.trim="ruleForm.description" type='textarea' autosize></el-input>
        </el-form-item>

        <el-form-item label="">
          <template>
            <!-- `checked` 为 true 或 false -->
            <el-tooltip class="item" effect="dark" content="选中后，当流程走到该节点时，可以把SQL在对应实例中执行" placement="right">
              <el-checkbox v-model="ruleForm.exec_tag">是否执行SQL</el-checkbox>
            </el-tooltip>
          </template>
        </el-form-item>
        <el-form-item label="选择执行环境" prop="cluster_ids" v-if="ruleForm.exec_tag == 1">
          <el-select v-model="ruleForm.cluster_ids" multiple placeholder="" style="width:100%">
            <el-option :label="cluster.name" :value="cluster.id" :key="cluster.id" v-for="cluster in enviroments"></el-option>
          </el-select>
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
import { EnviromentListApiUrl, NodesPage, NodeListApiUrl, UserListApiUrl } from '@/http/url'
export default {
  name: 'nodeUpdate',
  data() {
    return {
      ruleForm: {
        name: '',
        description: '',
        cluster_ids: [],
        exec_tag: '',
        operators:[],
      },
      user_list: [],  //用户列表
      enviroments: [],  //环境列表
      rules: {
        name: { required: true, message: '请输入名称', trigger: 'blur' },
        describe: { required: true, message: '请输入提交原因', trigger: 'blur' },
        operators:{required: true,type:'array', message:'请选择审核人',trigger:'blur'},
        cluster_ids:{required:true,type:'array',message:'请选择环境',trigger:'blur'},
        step_type:{required:true,message:'请选择审核类型',trigger:'blur'},
      },
      step_type:'0',

    }
  },
  methods: {
    get_users() {
      var self = this
      self.$http.get(UserListApiUrl).then((response) => {
        self.user_list = response.data.result
      })
    },
    get_enviroments() {
      //获取环境列表数据
      var self = this
      self.$http.get(EnviromentListApiUrl).then((response) => {
        self.enviroments = response.data.result
      })
    },
    submitForm(formName) {
      // 提交按钮
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.update_node()
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    update_node() {
      var self = this
      var id = self.$route.params.id
      this.$http.put(NodeListApiUrl +'/'+id, this.ruleForm).then(function(response) {
        self.$message(response.data.msg)
        if (response.data.status == 1) {
          self.$router.push(NodesPage)
        }
      })
    },
    get_node(){
      var self = this
      var id = self.$route.params.id 
      self.$http.get(NodeListApiUrl+'/'+id).then((response)=>{
        self.ruleForm = response.data.result  
        self.ruleForm.step_type = response.data.result.step_type.toString()
      })
    }
  },
  mounted() {
    this.get_enviroments()
    this.get_users()
    this.get_node()
  }
}

</script>
