<template>
  <div class="card">
    <div class="card-body">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">

<!--         <el-form-item prop="name" required label="名称">
          <el-input v-model="ruleForm.name" placeholder=""></el-input>
        </el-form-item>
 -->
        <el-form-item prop="ip" required label="IP">
          <el-input v-model="ruleForm.ip" placeholder="192.168.0.1"></el-input>
        </el-form-item>
        <el-form-item prop="port" label="端口">
          <el-input v-model.number="ruleForm.port" type="number" placeholder="3306"></el-input>
        </el-form-item>
        <el-form-item label="用户名" prop="dbuser">
          <el-input v-model="ruleForm.dbuser" placeholder="username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="dbpwd">
          <el-input v-model="ruleForm.dbpwd" type="password" placeholder="password"></el-input>
        </el-form-item>

        <el-form-item label="环境" prop="cluster_id">
          <el-select v-model.number="ruleForm.cluster_id" placeholder="选择环境" style="width:100%" >
            <el-option :label="cluster.name" :value="cluster.id" :key="cluster.id" v-for="cluster in enviroments"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="ruleForm.type" placeholder="选择类型：'MySQL'，'Oracle'" style="width:100%">
            <el-option label="MySQL" value="MySQL"></el-option>
            <el-option label="Oracle" value="Oracle"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="ruleForm.remark"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">保存</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
<script>
import { InstanceListApiUrl, InstancesPage, EnviromentListApiUrl } from '@/http/url'
import { checkIP} from '@/http/pubfunc'

export default {
  name:'instance_update',
  data() {
    return {
      ruleForm: {
        cluster_id: '',
        ip: '',
        port: '',
        dbuser: '',
        dbpwd: '',
        type: '',
        remark: '',
      },
      enviroments:[],
      user_list: [],
      rules: {
        name: [
          { required: true, message: '请输入数据库名称', trigger: 'blur' },
          // { min: 3,  message: '长度在 3 到 5 个字符', trigger: 'blur' }
        ],
        cluster_id: [{ required: true, type:'number',message: '请选择环境', trigger: 'change' }],
        ip: [
          // { required: true, message: '请输入IP', trigger: 'blur' }
          { validator: checkIP, trigger: 'blur' }
        ],
        port: [
          { required: true, type: 'number', message: '请输入端口', trigger: 'blur' },
          { min: 0, max: 65536, type: 'number', message: '值范围0-65535', trigger: 'blur' },
        ],
        dbuser: [
          { required: true, message: "请输入用户名", trigger: 'blur' }
        ],
        dbpwd: [
          { required: true, message: "请输入密码", trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择数据库类型' }
        ],
      }
    };
  },
  methods: {
    get_enviroments(){
    //获取环境列表数据
        var self = this
        self.$http.get(EnviromentListApiUrl).then((response)=>{
            self.enviroments = response.data.result
        })
    },
    submitForm(formName) {
      // 提交按钮
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.update_instance()
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    update_instance() {
      // 提交配置
      var self = this
      var id = this.$route.params.id
      this.$http.put(InstanceListApiUrl +'/' +id, this.ruleForm).then(function(response) {
        self.$message(response.data.msg)
        if (response.data.status == 1){
          self.$router.push(InstancesPage)
        }
      })
    },
    get_instance(){
      var self = this
      var id = this.$route.params.id
        this.$http.get(InstanceListApiUrl+'/'+id).then(function(response){
          self.ruleForm = response.data.result
        })
    },
  },
  mounted() {
    this.get_instance()
    this.get_enviroments()
  }
}

</script>
