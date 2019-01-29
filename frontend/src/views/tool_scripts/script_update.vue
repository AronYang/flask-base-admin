<template>
  <div class="card">
    <div class="card-body">
  <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
    <el-tab-pane label="执行脚本" name="执行脚本"></el-tab-pane>
    <el-tab-pane label="更新脚本" name="更新脚本"></el-tab-pane>
  </el-tabs>

      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">


        <el-form-item label="脚本名称" prop="name">
          <el-input v-model.trim="ruleForm.name"></el-input>
        </el-form-item>
<!--         <el-form-item label="脚本类型" prop="type">
          <el-select v-model="ruleForm.type" filterable placeholder="Shell或Python" style="width:100%" >
              <el-option label="Shell" value="Shell"></el-option>
              <el-option label="Python" value="Python"></el-option>
          </el-select>
        </el-form-item> -->

        <el-form-item label="分类" prop="tag">
          <el-select     v-model="ruleForm.tag" filterable allow-create placeholder="请选择或输入新的分类,如：常用命令, 系统管理, 网络管理, 部署  " style="width:100%">
            <el-option value="常用命令"></el-option>
            <el-option value="系统管理"></el-option>
            <el-option value="网络管理"></el-option>
            <el-option value="故障排查"></el-option>
            <el-option value="构建工具"></el-option>

            <el-option  v-for="tag in tag_list" :key="tag"  :label="tag"  :value="tag"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="输入参数" prop='args' >
          <!-- <el-input v-model.trim="ruleForm.route" placeholder="参数"></el-input> -->
          <!-- <br> -->
          <el-row >
            <el-col :span="4">参数名称</el-col>
            <el-col :span="2">是否必填</el-col>
            <el-col :span="4">默认值</el-col>
            <el-col :span="6">说明</el-col>
            <el-col :span="6">操作</el-col>
          </el-row>
          <el-row :gutter="20" v-for="v,k in ruleForm.args" :key="k">
            <el-col :span="4">{{k}}</el-col>
            <el-col :span="2">
                <el-tag type="danger" v-if="v.is_must == 1">是</el-tag>
                <el-tag type="info" v-else>否</el-tag>
            </el-col>

            <el-col :span="4">{{v.value}}<div v-if="v.value==''">空</div></el-col>
            <el-col :span="6">{{v.describe}}<div v-if="v.describe==''">空</div></el-col>

            <el-col :span="6"><el-button type="danger" size="small" @click="del_arg(k)">删除</el-button></el-col>
          </el-row>

          <br>
          <el-row :gutter="20">
            <el-col :span="4">
              <el-input v-model.trim="add_arg.name" placeholder="参数名称"></el-input>
            </el-col>
            <el-col :span="2">
              <el-checkbox v-model="add_arg.is_must">是否必须</el-checkbox>
            </el-col>
            <el-col :span="4">
              <el-input v-model.trim="add_arg.value" placeholder="默认值"></el-input>
            </el-col>
            <el-col :span="6">
              <el-input v-model.trim="add_arg.describe" placeholder="说明"></el-input>
            </el-col>

            <el-col :span="6">
              <el-button size="small" @click="add_args()"> 新增参数</el-button>
            </el-col>
          </el-row>
        </el-form-item>

        <el-form-item label="脚本内容" prop="content">
          <el-col>
            <div class="codemirror" v-show="ruleForm.type =='Python'">
              <codemirror v-model="ruleForm.content" :options="editorOptionPython" ></codemirror>
            </div>
            <div class="codemirror" v-show="ruleForm.type != 'Python'">
              <codemirror v-model="ruleForm.content" :options="editorOptionShell" ></codemirror>
            </div>
          </el-col>
          <el-col>
          </el-col>
        </el-form-item>
        <el-form-item label="说明">
          <el-input v-model.trim="ruleForm.remark" type='textarea' autosize></el-input>
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
import { ToolScriptsApi } from '@/http/url'
export default {
  name: 'scriptCreate',
  data() {
    return {
      ruleForm: {
        name: '',
        type: '',
        tag: '',
        args: {},  //格式：{'nginx':{'value':123,'describe':'nginx安装'}},
        content:'',
        remark: '',
      },
      rules: {
        name: { required: true, message: '请输入脚本名称', trigger: 'blur' },
        type: { required: true, message: '请选择脚本类型', trigger: 'blur' },
        tag: { required: true, message: '请输入或选择分类', trigger: 'blur' },
        content: { required: true, message: '请输入脚本内容', trigger: 'blur' },
      },
      add_arg:{
        name:'',
        value:'',
        describe:'',
      },
      tag_list:[],
      editorOptionShell: {
        tabSize: 4,
        styleActiveLine: true,
        lineNumbers: true,
        line: true,
        mode: 'text/x-sh',
        lineWrapping: true,
        showCursorWhenSelecting: true,
        theme: 'solarized light'
      },
      editorOptionPython: {
        tabSize: 4,
        styleActiveLine: true,
        lineNumbers: true,
        line: true,
        lineWrapping: true,
        showCursorWhenSelecting: true,
        mode: 'text/x-python',
        theme: 'solarized light'
      },
      activeName:'更新脚本',
    }
  },
  computed:{
  },
  methods: {
    del_arg(k){
      //删除参数
      this.$delete(this.ruleForm.args,k)
    },
    add_args(){
      //添加参数
      var k = this.add_arg.name
      var v = this.add_arg.value
      var describe = this.add_arg.describe
      var d ={}
      d[k]= {'value':v,'describe':describe}
      this.ruleForm.args = Object.assign({},this.ruleForm.args,d)
      this.add_arg.name = ''
      this.add_arg.value = ''
      this.add_arg.describe = ''
    },
    get_script_ruleForm() {
      var self = this
      var script_id = self.$route.params.id
      self.$http.get(ToolScriptsApi+'/'+script_id).then((response) => {
        self.ruleForm = response.data.result
      })
    },
    submitForm(formName) {
      // 提交按钮
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.update_script()
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    update_script() {
      var self = this
      var script_id = self.$route.params.id
      this.$http.put(ToolScriptsApi+'/'+script_id, this.ruleForm).then(function(response) {
        self.$message(response.data.msg)
        if (response.data.status == 1) {
          ///如果提交成功，则返回到上一次路径
          self.$router.go(-1)
        }
      })
    },
    handleClick(tab,event){

      var update_url = this.$route.path.replace('/exec','')
      if (this.activeName =='执行脚本'){
          this.$router.push(update_url+'/exec')
      }else{
        this.$router.push(update_url)
      }
    }
  },
  mounted() {
    this.get_script_ruleForm()
  }
}

</script>
