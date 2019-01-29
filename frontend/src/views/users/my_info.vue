<template>
  <div class="card">
    <div class="card-body">
      <h4 class="card-title">个人信息：</h4>
      <table class="table   ">
        <tr>
          <td width='120'>姓名</td>
          <td>
            <span v-if="edit_status == 0">{{ruleForm.name}} </span>
            <el-input v-if="edit_status == 1" v-model="ruleForm.name" placeholder=""></el-input>
          </td>
        </tr>
        <tr>
          <td width='120'>部门</td>
          <td>{{ruleForm.groupName}}
          </td>
        </tr>
        <tr>
          <td width='120'>用户名</td>
          <td>{{ruleForm.username}}</td>
        </tr>
        <tr>
          <td width='120'>姓别</td>
          <td>
            <span v-if="edit_status == 0">{{ruleForm.sex}} </span>
          <el-select v-model.number="ruleForm.sex" placeholder="选择性别" style="width:100%"  v-if="edit_status == 1">
            <el-option label="男" value="男" ></el-option>
            <el-option label="女" value="女" ></el-option>
          </el-select>

          </td>
        </tr>
        <tr>
          <td width='120'>电话</td>
          <td>
            <span v-if="edit_status == 0">{{ruleForm.phone}} </span>
            <el-input v-if="edit_status == 1" v-model="ruleForm.phone" placeholder=""></el-input>
          </td>
        </tr>
        <tr>
          <td width='120'>邮箱</td>
          <td>
            <span v-if="edit_status == 0">{{ruleForm.mail}} </span>
            <el-input v-if="edit_status == 1" v-model="ruleForm.mail" placeholder=""></el-input>
          </td>
        </tr>
        <tr>
          <td width='120'>地区</td>
          <td>
            <span v-if="edit_status == 0">{{ruleForm.city}} </span>
            <el-input v-if="edit_status == 1" v-model="ruleForm.city" placeholder=""></el-input>
          </td>
        </tr>
        <tr>
          <td width="120">
            <el-button type='text' @click="edit_status = !edit_status" v-if="edit_status == 0">编辑</el-button>
          </td>
          <td>
            <el-button type='primary' @click="modify_info" v-if="edit_status == 1">保存</el-button>
            <el-button type='default' @click="edit_status = 0" v-if="edit_status == 1">取消</el-button>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>
<script>
import { UserInfoApiUrl } from '@/http/url'
export default {
  name: 'myinfo',
  data() {
    return {
      ruleForm: {},
      edit_status: 0,
    }
  },
  methods: {
    modify_info() {
      var self = this
      this.$http.put(UserInfoApiUrl, this.ruleForm).then(function(response) {
        self.$message(response.data.msg)
        if (response.data.status == 1) {
          self.edit_status = 0 
        }
      })
    },
    get_info() {
      var self = this
      self.$http.get(UserInfoApiUrl).then((response) => {
        self.ruleForm = response.data.result
      })
    }
  },
  mounted() {
    this.get_info()
  }
}

</script>
