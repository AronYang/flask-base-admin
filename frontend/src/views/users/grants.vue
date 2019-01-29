<style>
.table th, .table td {
  padding:0.35rem;
}

</style>
<template>
  <div class="card">
    <div class="card-body">
      <el-row style="">
        <el-col :span="5">
          <el-row class="text-left" style="margin-top:5px;margin-bottom:10px">
            <el-button @click="ShowAddChildRoleModal=1" type="primary">添加角色</el-button>
          </el-row>
          <el-tree style="height:900px" :data="role_list" :props="defaultProps" @node-click="handleNodeClick" highlight-current :render-content="renderContent"   ref="tree"  node-key="id" show-checkbox></el-tree>
        </el-col>

        <el-col :span="18" style="margin-left:20px">
        <el-row class="text-right">
          <el-button type="primary" @click="submitGrants">保存权限</el-button>
        </el-row>
        <hr>
        <div>
          <p class="text-muted">允许用户:</p>
          <!-- <p v-for="user in roleInfo.users">{{user.name}}</p> -->
          <el-select v-model="roleInfo.user_ids" multiple placeholder="" style="width:100%">
            <el-option :label="user.name+'('+user.username+')'" :value="user.id" :key="user.id" v-for="user in user_list"></el-option>
          </el-select>

        </div>
        <hr>
        <div >
          <p class="text-muted">允许部门:</p>
          <el-select v-model="roleInfo.group_ids" multiple placeholder="" style="width:100%">
            <el-option :label="department.name" :value="department.id" :key="department.id" v-for="department in department_list">
              <span :style="{'padding-left':(department.level-2)*20+'px'}">{{ department.name }}</span>
            </el-option>
          </el-select>

        </div>
        <hr>

        <p class="text-muted">权限设置:</p>
        <table class="table  table-bordered table-condensed">
        <tbody>
          <tr>
            <td><strong>名称</strong></td>
            <td><strong>URL</strong></td>
            <td><strong @click="aclGetAllselect"><el-checkbox  v-model="aclGetAllSelectStatus"></el-checkbox>&nbsp查看</strong></td>
            <td><strong @click="aclPostAllselect"><el-checkbox  v-model="aclPostAllSelectStatus"></el-checkbox>&nbsp新增</strong></td>
            <td><strong @click="aclPutAllselect"><el-checkbox  v-model="aclPutAllSelectStatus"></el-checkbox>&nbsp更新</strong></td>
            <td><strong @click="aclDelAllselect"><el-checkbox  v-model="aclDelAllSelectStatus"></el-checkbox>&nbsp删除</strong></td>
          </tr>

        <template v-for="u in url_list">
              <tr>
              <td><span :style="{'margin-left':u.offset*20+'px'}">{{u.name}}</span></td>
              <td>{{u.url}}</td>
              <td><el-checkbox v-model="u.get"></el-checkbox></td>
              <td><el-checkbox v-model="u.post"></el-checkbox></td>
              <td><el-checkbox v-model="u.put"></el-checkbox></td>
              <td><el-checkbox v-model="u.delete"></el-checkbox></td>
              </tr>
        </template>
        </tbody>
        </table>
<hr>

        </el-col>
      </el-row>
    </div>


    <el-dialog
      title="添加角色"
      :visible.sync="ShowAddChildRoleModal"
      size="tiny"
      >

      <el-input v-model.trim="NewRoleName"  placeholder="输入角色名称"></el-input>

      <span slot="footer" class="dialog-footer">
        <el-button @click="ShowAddChildRoleModal = false">取 消</el-button>
        <el-button type="primary" @click="create_role">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="修改角色"
      :visible.sync="ShowModifyChildRoleModal"
      size="tiny"
      >
      <el-input placeholder="输入角色名称" v-model.trim="treeNodeName"></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="ShowModifyChildRoleModal = false">取 消</el-button>
        <el-button type="primary" @click="modify_role">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>


<script>
// import { RolesTreeApiUrl, UserListApiUrl} from '@/http/url'

import {RolesListApiUrl, GrantsRoleApiUrl, DepartmentsListApiUrl, UserListApiUrl} from '@/http/url'

import nav from '../../_nav'
export default {
  name: 'role',
  data() {
    return {
      url_list:[],
      acl_list:[],
      roleInfo:{},
      role_list:[],
      user_list:[],
      department_list:[],
      ruleForm:{
        name:'',
        username:'',
        pwd:'',
        phone:'',
        mail:'',
        city:'',
        group_id:'',
      },
      editUserForm:{},
      treeNodeId: '',  //当前选中的节点
      treeNodeName:'', //当前选中的节点名称
      NewRoleName:'', // 新的角色名称
      filterText: '',   //角色过滤文本
      role_tree:[],   //角色树数据
      defaultProps: {   //角色的显示内容
        children: 'children',
        label: 'name'
      },
      ShowAddChildRoleModal:false,
      ShowModifyChildRoleModal:false,
      ShowAddUserModal:false,
      ShowEditUserModal:false,
      resetPwd:false,
      aclGetAllSelectStatus:false,
      aclPostAllSelectStatus:false,
      aclPutAllSelectStatus:false,
      aclDelAllSelectStatus:false
    };
  },
  methods: {
    get_user_list(){
        var self = this
        self.$http.get(UserListApiUrl).then((response)=>{
          self.user_list = response.data.result
        })
    },
    get_department_list(){
        var self = this
        self.$http.get(DepartmentsListApiUrl).then((response)=>{
          self.department_list = response.data.result
          console.log(self.department_list)
        })
    },
    create_role(){
      //新增角色
      var self = this
      if(self.NewRoleName==''){
        self.$message.error('角色名称不能为空！')
        return
      }
      var d = {
        name:self.NewRoleName
      }
      self.$http.post(RolesListApiUrl, d).then((response)=>{
        self.$message(response.data.msg)
        if(response.data.status == 1){
          self.get_roles()
          self.ShowAddChildRoleModal=0
        }
      })
    },
    modify_role(){
      //修改角色
      var self = this
      if(self.treeNodeName==''){
        self.$message.error('角色名称不能为空！')
        return
      }
      var d={
        name:self.treeNodeName,
      }
      self.$http.put(RolesListApiUrl+'/'+self.treeNodeId, d).then((response)=>{
        self.$message(response.data.msg)
        if(response.data.status == 1 ){
          self.ShowModifyChildRoleModal = false
          self.get_roles()
        }
      })
    },
    delete_role(){
      //删除角色
      var self = this
      self.$http.delete(RolesListApiUrl+'/'+self.treeNodeId).then((response)=>{
        self.$message(response.data.msg)
        if (response.data.status == 1){
          self.get_roles()
        }
      })
    },
    handleNodeClick(data) {
      //角色点击事件，把角色ID和名称赋值
      this.treeNodeId = data.id
      this.treeNodeName = data.name
      this.$refs.tree.setCheckedNodes([data,])
      this.get_role_info()
    },
    get_role_info(){
      //获取色角的授权信息
      var self = this
      self.url_list = self.handler_url_list()
      self.$http.get(GrantsRoleApiUrl+'/'+this.treeNodeId).then((response)=>{
        self.roleInfo = response.data.result
        for (var n in self.roleInfo.acls){
          var acl = self.roleInfo.acls[n]
          for(var m in self.url_list){
            var s_acl = self.url_list[m]
            if (acl.url == s_acl.url){
              self.url_list[m].get = acl.get
              self.url_list[m].post = acl.post
              self.url_list[m].put = acl.put
              self.url_list[m].delete = acl.delete
            }
          }
        }
      })
    },
    roleAction(action, store, data) {
      //角色操作，修改名称，添加子角色等
      if (action == 'modify'){
        this.ShowModifyChildRoleModal = true
      }else if (action == 'delete'){
        this.$confirm('确定要删除当前角色吗? ', '警告').then(() => {
          this.delete_role()
        }).catch(() => {})
      }
    },
    showNodeEdit(nodeId) {
      if (nodeId == this.treeNodeId) {
        return true
      } else {
        return false
      }
    },
    handler_url_list(){
      // 把_nav里的配置导出来，生成同一级别的对象，方便保存进数据库
      var url_list = []
      for (var n in nav.items){
        var r = nav.items[n]
        var d = {
          name:r.name,
          url:r.url,
          offset:0,
          get:0,
          post:0,
          put:0,
          delete:0,
        }
        url_list.push(d)
        if(r.children){
          for (var m in r.children){
            var r2 = r.children[m]
            var d = {
              name:r2.name,
              url:r2.url,
              offset:1,
              get:0,
              post:0,
              put:0,
              delete:0,
            }
            url_list.push(d)
          }
        }
      }
      return url_list
    },
    submitGrants(){
      //保存权限信息
      console.log(this.url_list)
      var self = this
      var d={
        acls:this.url_list,
        user_ids: self.roleInfo.user_ids,
        group_ids:self.roleInfo.group_ids,
      }
      self.$http.put(GrantsRoleApiUrl+'/'+ this.treeNodeId, d).then((response)=>{
         self.$message(response.data.msg)
      })
    },
    get_roles(){
      // 获取角色列表
      var self = this
      self.$http.get(RolesListApiUrl).then((response)=>{
        self.role_list = response.data.result
        if(self.role_list.length > 0){
            self.treeNodeId = self.role_list[0].id
            self.treeNodeName = self.role_list[0].name
            self.$refs.tree.setCheckedKeys([1]);
            self.get_role_info()
        }
      })
    },
    aclGetAllselect: function() {
      // console.log('get...')
        // if (this.aclGetAllSelectStatus == false) {
        //     var value = true
        // } else {
        //     var value = false
        // }
        for (var n in this.url_list) {
            this.url_list[n].get = !this.aclGetAllSelectStatus
        }
    },
    aclPostAllselect: function() {
        // console.log(this.aclPostAllselectStatus,'status...')

        for (var n in this.url_list) {
            this.url_list[n].post = !this.aclPostAllSelectStatus
        }
    },
    aclDelAllselect: function() {
        // if (this.aclDelAllSelectStatus == false) {
        //     var value = true
        // } else {
        //     var value = false
        // }
        for (var n in this.url_list) {
            this.url_list[n].delete = !this.aclDelAllSelectStatus
        }
    },
    aclPutAllselect: function() {
        // if (this.aclPutAllSelectStatus == false) {
        //     var value = true
        // } else {
        //     var value = false
        // }
        for (var n in this.url_list) {
            this.url_list[n].put = !this.aclPutAllSelectStatus
        }
    },
    renderContent(h, { node, data, store }) {
      //这里用的是jsx语法。
      return (
        <span>
          <span > { node.label }</span>
          <span style="float: right;" v-show={ data.id == this.treeNodeId } >
            <el-dropdown style="width:20px"  onCommand={(action) => this.roleAction(action, store, data) }>
              <span class="el-dropdown-link" >
                <i class="icon-pencil" > < /i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="modify" > 修改角色名称 </el-dropdown-item>
                <el-dropdown-item command="delete" > 删除角色 </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </span>
        </span>
      )
    },
  },
  mounted(){
    console.log('mounted...')
    window.heihei=this
    this.url_list = this.handler_url_list()
    this.get_roles()
    this.get_user_list()
    this.get_department_list()


    // this.routes = this.$router.options.routes
  }

}

</script>
