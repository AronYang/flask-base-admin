<template>
  <div class="card">
    <div class="card-body">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">
        <el-form-item label="流程名称" prop="name">
          <el-input v-model.trim="ruleForm.name"></el-input>
        </el-form-item>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model.trim="ruleForm.description" type='textarea' placeholder="流程描述" autosize></el-input>
        </el-form-item>
        <el-form-item label="步骤" prop="node_ids">
          <el-select v-model="ruleForm.node_ids"  filterable  clearable  multiple placeholder="按先后选择定义流程" style="width:100%">
            <el-option v-for="node in nodes" :key="node.id" :label="node.name" :value="node.id">
            </el-option>
          </el-select>
          <div>
            <el-steps :space="80" direction="vertical" style='margin-top:15px'>
              <el-step :title="n.name" :key="n.id" :description="'审核人:'+ n.operatorNames + '  描述:'+n.description "  v-for="n in select_nodes"></el-step>
            </el-steps>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">保存</el-button>
          <!-- <el-button @click="resetForm('ruleForm')">清空</el-button> -->
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
<script>
import { FlowsPage, FlowListApiUrl, NodeListApiUrl } from '@/http/url'
export default {
  name: 'flowUpdate',
  data() {
    return {
      ruleForm: {
        name: '',
        description: '',
        node_ids: [],
      },
      nodes: [], //节点列表
      rules: {
        name: { required: true, message: '请输入名称', trigger: 'blur' },
        node_ids: {required:true, type:'array', message:'必须选择节点', trigger:'blur'}
      },
    }
  },
  computed: {
    select_nodes() {
      var newlist = []
      for (var i in this.ruleForm.node_ids){
        var select_id = this.ruleForm.node_ids[i]
        for (var n in this.nodes) {
          if (this.nodes[n].id == select_id) {
            newlist.push(this.nodes[n])
          }
        }
      }
      return newlist
    }
  },
  methods: {
    get_nodes() {
      var self = this
      self.$http.get(NodeListApiUrl).then((response) => {
        self.nodes = response.data.result
      })
    },
    submitForm(formName) {
      // 提交按钮
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.update_flow()
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    update_flow() {
      var self = this
      var id = self.$route.params.id
      this.$http.put(FlowListApiUrl+'/'+id, this.ruleForm).then(function(response) {
        self.$message(response.data.msg)
        if (response.data.status == 1) {
          self.$router.push(FlowsPage)
        }
      })
    },
    get_flow(){
     //获取流程信息
     var self = this 
     var id = self.$route.params.id  
     self.$http.get(FlowListApiUrl+'/'+id).then((response)=>{
        self.ruleForm = response.data.result
     })   
    }

  },
  mounted() {
    this.get_nodes()
    this.get_flow()  
  }
}

</script>
