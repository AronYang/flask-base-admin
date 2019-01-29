<template>
  <div class="card">
    <div class="card-body">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">


        <el-form-item label="任务名称" prop="name">
          <el-input v-model.trim="ruleForm.name"></el-input>
        </el-form-item>

        <el-form-item label="脚本关系"  >
          <el-select v-model.string="ruleForm.depend" style="width:100%">
            <el-option value="0" label="或">或(不依赖前一个脚本的执行成功或失败)</el-option>
            <el-option value="1" label="与">与(前一个脚本执行成功才会执行后一个脚本)</el-option>
          </el-select>
        </el-form-item>

<!--         <el-form-item label="状态" >
            <el-checkbox v-model="ruleForm.is_valid">是否有效</el-checkbox>
        </el-form-item> -->

        <el-form-item label="脚本" prop="script_ids">
          <el-select v-model="ruleForm.script_ids"  filterable  clearable  multiple placeholder="按先后选择脚本" style="width:100%">
            <el-option v-for="script in script_list" :key="script.id" :label="script.name" :value="script.id">
            </el-option>
          </el-select>
          <div>
            <el-steps :space="80" direction="vertical" style='margin-top:15px'>
              <el-step :title="n.name" :key="n.id"  :description="'脚本说明:'+n.remark " v-for="n in select_scripts"></el-step>
            </el-steps>
          </div>
        </el-form-item>

        <el-form-item label="说明">
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
import { ToolChainsApi, ToolScriptsApi } from '@/http/url'
export default {
  name: 'chainCreate',
  data() {
    return {
      ruleForm: {
        name: '',
        depend:'0',
        is_valid:true,
        script_ids:[],
        remark: '',
      },
      script_list:[],
      rules: {
        name: { required: true, message: '请输入任务名称', trigger: 'blur' },
        script_ids: { required: true,type:'array', message: '必须选择脚本', trigger: 'blur' },
      },
    }
  },
  computed:{
    select_scripts() {
      //选中的脚本，匹配出来后，在step中显示
      var newlist = []
      for (var i in this.ruleForm.script_ids){
        var select_id = this.ruleForm.script_ids[i]
        for (var n in this.script_list) {
          if (this.script_list[n].id == select_id) {
            newlist.push(this.script_list[n])
          }
        }
      }
      return newlist
    }
  },
  methods: {
    get_script_list(){
          var self  = this
          this.$http.get(ToolScriptsApi).then(function(response) {
                self.script_list = response.data.result
          })
    },
    submitForm(formName) {
      // 提交按钮
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.update_chain()
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    get_chain_ruleForm() {
      var self = this
      var chain_id = self.$route.params.id
      self.$http.get(ToolChainsApi+'/'+chain_id).then((response) => {
        self.ruleForm = response.data.result
        // self.ruleForm.depend =  response.data.result.depend.toString()
      })
    },
    update_chain() {
      var self = this
      var chain_id = self.$route.params.id
      this.$http.put(ToolChainsApi+'/'+chain_id, this.ruleForm).then(function(response) {
        self.$message(response.data.msg)
        if (response.data.status == 1) {
          ///如果提交成功，则返回到上一次路径
          self.$router.go(-1)
        }
      })
    },
  },
  mounted() {
      this.get_script_list()
      this.get_chain_ruleForm()
  }
}

</script>
