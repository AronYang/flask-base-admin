<template>
  <div class="card">
    <div class="card-body">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">
        <el-form-item label="工单名称" prop="name">
          <el-input v-model.trim="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="原因说明" prop="reason">
          <el-input v-model.trim="ruleForm.reason" type='textarea' autosize></el-input>
        </el-form-item>
        <el-form-item label="计划上线时间" prop="online_time" style="width:100%">
            <el-date-picker
              v-model="ruleForm.online_time"
              type="datetime"
              format="yyyy-MM-dd HH-mm"
              placeholder="选择日期时间" >
            </el-date-picker>
        </el-form-item>


        <el-form-item label="选择流程" prop="flow_id">
          <el-select v-model.number="ruleForm.flow_id" filterable  clearable placeholder="" style="width:100%">
            <el-option :label="flow.name" :value="flow.id" :key="flow.id" v-for="flow in flow_list"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="SQL来源">
          <template>
            <el-radio class="radio" v-model="ruleForm.svntag" label="0">默认</el-radio>
            <el-radio class="radio" v-model="ruleForm.svntag" label="1">SVN获取</el-radio>
          </template>
        </el-form-item>

        <el-form-item label="选择SQL目录" prop="svndirname" v-if="ruleForm.svntag == 1">
          <el-select v-model="ruleForm.svndirname" filterable  clearable placeholder="搜索" style="width:100%">
            <el-option :label="dirname" :value="dirname" :key="dirname" v-for="dirname in sqlsvndirlist"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="数据库名称" prop="dbname"  v-if="ruleForm.svntag == 0">
          <el-input v-model.trim="ruleForm.dbname" placeholder="test"></el-input>
        </el-form-item>
        <el-form-item label="SQL内容" prop="sqlContent"  v-if="ruleForm.svntag == 0">
          <el-col>
            <div class="codemirror">
              <!-- codemirror -->
              <codemirror v-model="ruleForm.sqlContent" :options="editorOption"></codemirror>
            </div>
          </el-col>
          <el-col>
          </el-col>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm',1)">提交</el-button>
          <el-button @click="submitForm('ruleForm',0)" v-if="!ruleForm.status >= 0 ">保存草稿</el-button>
        </el-form-item>
      </el-form>
      </el-form>
    </div>
  </div>
</template>
<script>
import { SubmitListApiUrl, FlowListApiUrl, SubmitSqlSvnDirList } from '@/http/url'
export default {
  name: 'submitCreate',
  data() {
    return {
      ruleForm: {
        name: '',
        reason: '',
        sqlContent: '',
        flow_id: '',
        dbname:'',
        online_time:'',
        svndirname:'',
        svntag:'0',
      },
      sqlsvndirlist:[],
      flow_list: [],
      rules: {
        name: { required: true, message: '请输入名称', trigger: 'blur' },
        reason: { required: true, message: '请输入提交原因', trigger: 'blur' },
        sqlContent: { required: true, message: '请输入SQL内容', trigger: 'blur' },
        dbname: { required: true, message: '请输入数据库名称', trigger: 'blur' },
        online_time: { required: true, type:"date", message: '请选择时间', trigger: 'blur' },
        flow_id: { required: true, type: 'number', message: '请选择对应流程', trigger: 'change' },
        svndirname: { required: true,  message: '请选择SVN目录', trigger: 'change' },
      },
      editorOption: {
        tabSize: 4,
        styleActiveLine: true,
        lineNumbers: true,
        line: true,
        mode: 'text/x-mysql',
        theme: 'solarized light'
      },
    }
  },
  methods: {
    submitForm(formName,status) {
      // 提交按钮
      var self = this
      this.ruleForm.status = status
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.create_submit()
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    create_submit() {
      var self = this
      this.$http.post(SubmitListApiUrl, this.ruleForm).then(function(response) {
        self.$message(response.data.msg)
        if (response.data.status == 1) {
          self.$router.push('/sqlaudit/submits')
        }
      })
    },
    get_flows() {
      var self = this
      this.$http.get(FlowListApiUrl).then((response) => {
        self.flow_list = response.data.result
      })
    },
    get_sqldirlist(){
      var self = this 
      self.$http.get(SubmitSqlSvnDirList).then((response)=>{
        self.sqlsvndirlist = response.data.result
        console.log(self.sqlsvndirlist)
      })
    }
  },
  mounted() {
    this.get_flows()
    this.get_sqldirlist()
  }
}

</script>
