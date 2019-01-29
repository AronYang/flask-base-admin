<template>
  <div class="card">
    <div class="card-body">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">


        <el-form-item label="选择任务类型">
          <el-select v-model="ruleForm.from_type" filterable clearable style="width:100%" @change="get_script_or_chain_list">
            <el-option value="script" label="脚本"></el-option>
            <el-option value="chain" label="任务链"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="选择任务">
          <el-select v-model="ruleForm.from_id" filterable clearable style="width:100%" @change="get_chain_info">
            <el-option :value="item.id" :label="item.name" :key="item.name" v-for="item in script_or_chain_list"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="选择ssh用户">
          <el-select v-model="ruleForm.ssh_user_id" filterable clearable style="width:100%">
            <el-option :value="item.id" :label="item.username" :key="item.id" v-for="item in ssh_user_list"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="目标主机">
          <el-input type="textarea" :autosize="{ minRows: 3, maxRows: 8}" placeholder="请输入IP, 以空格分隔" v-model="ruleForm.ips">
          </el-input>
          <el-button @click="ShowAddHostModal=true"  size="small">选择主机</el-button>

        </el-form-item>

        <el-form-item label="参数来源">
          <el-select v-model="idc_id" filterable clearable style="width:100%" @change="get_variables_list">
            <el-option value="">全局</el-option>
            <el-option :value="item.id" :label="item.name" :key="item.id" v-for="item in idc_list"></el-option>
          </el-select>
        </el-form-item>


        <el-form-item label="脚本参数">
          <!-- <el-row > -->
          <el-row :gutter="20">
            <el-col :span="4">脚本名称</el-col>
            <el-col :span="18">参数</el-col>
          </el-row>
          <el-row :gutter="20" v-for="item in selected_script_or_chain" :key="item.id">
            <hr class="form-group-divider">
            <el-col :span="4">{{item.name}}</el-col>
            <el-col :span="18">
              <div v-if="item.args == '' ">
                <el-form-item label="None"></el-form-item>
              </div>
              <div v-for="v,k in item.args">
                <el-form-item :label="k">
                  <el-input v-model="item.args[k].value" style="width:300px;"></el-input>
                </el-form-item>
              </div>
            </el-col>
          </el-row>

        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">保存</el-button>
          <!-- <el-button @click="resetForm('ruleForm')">清空</el-button> -->
        </el-form-item>


          <el-dialog
            title="选择主机"
            :visible.sync="ShowAddHostModal"
            size="small"
            >
               <host_filter v-on:newSelectHostList="HandlerNewSelectHostList"></host_filter>

            <span slot="footer" class="dialog-footer">
              <el-button @click="ShowAddHostModal = false">取 消</el-button>
              <el-button type="primary" @click="save_select_host_to_ips" >保存</el-button>
            </span>
          </el-dialog>

      </el-form>
    </div>
  </div>
</template>
<script>
  import { ToolChainsApi, ToolScriptsApi, ToolExecutesApi, SetSshUsersApi, SetVariablesApi, IdcApi } from '@/http/url'
  import host_filter from '@/views/cmdb/host_filter'


  export default {
    name: 'executeCreate',
    components: {
      host_filter
    },
    data() {
      return {
        ruleForm: {
          from_type: '',
          from_id: '',
          ssh_user_id: '',
          args: {},
          ips: '',
          // idc_id: '',
        },
        idc_id:'',
        script_or_chain_list: [], //脚本或链的列表，选择类型后加载
        ssh_user_list: [], //ssh用户列表，选择该任务对应的ssh用户
        variable_list: [], //变量列表
        scripts_in_chain: [],
        idc_list: [],
        ShowAddHostModal: false,
        newSelectHostList:[],
        rules: {
          name: { required: true, message: '请输入任务名称', trigger: 'blur' },
          script_ids: { required: true, type: 'array', message: '必须选择脚本', trigger: 'blur' },
        },
      }
    },
    computed: {
      selected_script_or_chain() {
        //根据选择的脚本或脚本链，返回内容是，脚本列表
        var return_list = []
        if (this.ruleForm.from_id != '') {

          if (this.ruleForm.from_type == 'script') {
            for (var n in this.script_or_chain_list) {
              if (this.script_or_chain_list[n].id == this.ruleForm.from_id) {
                return_list.push(this.script_or_chain_list[n])
              }
            }
          }
          if (this.ruleForm.from_type == 'chain') {
            return_list = this.scripts_in_chain
          }

        }
        console.log('return  list,', return_list)
        return return_list
      },
    },
    methods: {
      save_select_host_to_ips(){
        //把主机添加到ips中。
        var ip_list = this.ruleForm.ips.replace(/ /g,'').split(',')
        var ips = this.ruleForm.ips
        for (var n in this.newSelectHostList){
          var ip = this.newSelectHostList[n].ip
          if (ip_list.indexOf(ip) == -1){
              if (ips == ''){
                ips = ips + ip
              }else if(/,$/.test(ips.replace(/ /g,''))){
                ips  = ips + ip
              }else{

                ips = ips + ', '+ip
              }
          }
        }
        this.ruleForm.ips = ips
        this.ShowAddHostModal = false
      },
      HandlerNewSelectHostList(payload) {
        //关联主机时,子组件调用的函数,payload为返回的数据
        console.log(payload, 'payload')
        this.newSelectHostList = payload
      },
      get_script_or_chain_list() {
        var self = this
        self.script_or_chain_list = []
        self.ruleForm.from_id = ''
        if (this.ruleForm.from_type == 'script') {
          this.$http.get(ToolScriptsApi).then(function(response) {
            self.script_or_chain_list = response.data.result
            console.log(self.script_or_chain_list)
          })
        } else {
          this.$http.get(ToolChainsApi).then(function(response) {
            self.script_or_chain_list = response.data.result
          })
        }
      },
      get_chain_info() {
        //获取单个任务链下的所有脚本
        var self = this
        self.scripts_in_chain = []
        if (this.ruleForm.from_type == 'chain') {
          this.$http.get(ToolChainsApi + '/' + this.ruleForm.from_id).then((res) => {
            self.scripts_in_chain = res.data.result.scripts
          })
        }
      },
      get_ssh_user_list() {
        //获取ssh用户列表
        var self = this
        self.$http.get(SetSshUsersApi).then((res) => {
          self.ssh_user_list = res.data.result
        })
      },
      get_idc_list() {
        //获取idc列表
        var self = this
        self.$http.get(IdcApi).then((res) => {
          self.idc_list = res.data.result
        })
      },
      submitForm(formName) {
        // 提交按钮
        var self = this
        this.$refs[formName].validate((valid) => {
          if (valid) {
            self.create_execute()
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      create_execute() {
        var self = this

        var d ={}
        for (var n in this.selected_script_or_chain){
          var item = this.selected_script_or_chain[n]
            d[item.id] = item.args
        }

        this.ruleForm.args = d
        this.$http.post(ToolExecutesApi, this.ruleForm).then(function(response) {
          self.$message(response.data.msg)
          if (response.data.status == 1) {
            ///如果提交成功，则返回到上一次路径
            self.$router.go(-1)
          }
        })
      },
      get_variables_list(){
        var self = this
        this.$http.get(SetVariablesApi, {params:{idc_id:this.idc_id}}).then((res)=>{
          this.variable_list = res.data.result
          console.log( 'variable list:', this.variable_list)
          self.set_args_variable_value()
        })
      },
      set_args_variable_value(){
        //遍历选中的脚本或链列表，把里面的args遍历
        for (var n in this.selected_script_or_chain){
          var args = this.selected_script_or_chain[n].args

          //遍历变量列表，如果变量名称在参数里存在，则把变量的值覆盖。
          for (var m in this.variable_list){
            var variable_name = this.variable_list[m].name
            var variable_value = this.variable_list[m].value
            if (args.hasOwnProperty(variable_name)){
              console.log('variable name:',variable_name,' value:',variable_value)
              args[variable_name].value = variable_value
            }
          }
          this.selected_script_or_chain[n].args = args
          console.log('------',this.selected_script_or_chain)
        }
      }
    },
    mounted() {
      this.get_idc_list()
      this.get_ssh_user_list()
    }
  }

</script>
