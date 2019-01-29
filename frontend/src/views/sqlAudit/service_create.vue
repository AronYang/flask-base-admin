<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">
    <div class="card">
      <div class="card-body">
        <el-form-item prop="name" required label="业务名">
          <el-input v-model="ruleForm.name" placeholder=""></el-input>
        </el-form-item>
        <el-form-item prop="description" label="描述">
          <el-input v-model="ruleForm.description"   type="textarea" autosize  :rows="2"  placeholder=""></el-input>
        </el-form-item>

        <template v-for="(db,index) in ruleForm.db_list">
          <el-form-item :label="'步骤'+index" :prop="'db_list.'+index+'.id[1]'" :rules="{
                    required: true, type:'number', message: '数据库选择不能为空', trigger: 'change'
                  }">
            <el-cascader expand-trigger="hover" :options="instanceTree" :props="props" v-model="db.id" @change="handleChange" filterable placeholder="可搜索数据库" style="width:80%">
            </el-cascader>
            <el-button :plain="true" type="danger" @click="db_list_del(index)" v-if="index>0">删除</el-button>
          </el-form-item>
        </template>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">保存</el-button>
          <el-button @click="db_list_add">新增数据库</el-button>
        </el-form-item>
      </div>
    </div>
  </el-form>
</template>
<script>
import { FlowDbTreeApiUrl,flowListApiUrl } from '@/http/url'

export default {
  data() {
    return {
      props: {
        value: 'id',
        children: 'db',
        label: 'name',
      },
      instanceTree: [],
      ruleForm: {
        name: '',
        description: '',
        db_list: [{ id: [] }],
      },
      user_list: [],
      rules: {
        name: [
          { required: true, message: '请输入数据库名称', trigger: 'blur' },
        ],
      }
    };
  },
  methods: {
    submitForm(formName) {
      // 提交按钮
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.create_flow()
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    create_flow() {
      // 提交配置
      var self = this
      this.$http.post(flowListApiUrl, self.ruleForm).then(function(response) {
        self.$message(response.data.msg)
      })
    },
    get_flow_dbtree() {
      // 获取数据库树列表
      var self = this
      this.$http.get(FlowDbTreeApiUrl).then(function(response) {
        console.log(response)
        self.instanceTree = response.data.result
      })
    },
    handleChange(value) {
      console.log(this.db_list)
    },
    db_list_add() {
      var d = { id: [] }
      this.ruleForm.db_list.push(d)
    },
    db_list_del(index) {
      this.ruleForm.db_list.splice(index, 1)
    }
  },
  mounted() {
    this.get_flow_dbtree()
  }
}

</script>
