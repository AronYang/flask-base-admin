<template>
  <div class="card">
    <div class="card-body">
      <el-row style="">
        <el-col :span="5">

        <el-row>
          <el-col :span="8">
            <el-button type="primary" @click="treeNodeId='';ShowAddChildDepartmentModal=true;">添加部门</el-button>
          </el-col>
          <el-col :span='16'>
            <el-input style="float:right" placeholder="搜索部门" v-model="filterText"> </el-input>
          </el-col>
        </el-row>


          <el-tree style="margin-top:20px;min-height:700px" :data="department_tree" :props="defaultProps" @node-click="handleNodeClick" highlight-current :filter-node-method="filterNode" ref="tree2" :render-content="renderContent" node-key="id"></el-tree>
<!--           <el-row class="text-right" style="margin-top:5px">
            <el-button @click="treeNodeId='';ShowAddChildDepartmentModal=1;">添加一级部门</el-button>
          </el-row> -->
        </el-col>
        <el-col :span="19" >
          <div style="margin-left:20px">
            <data-tables :data="user_list" :search-def="searchDef" :actions-def="actionsDef">
              <el-table-column sortable prop="name" label="姓名" width="150">
              </el-table-column>
              <el-table-column sortable prop="username" label="用户名" width="150">
              </el-table-column>
              <el-table-column sortable prop="departName" label="部门">
              </el-table-column>
              <el-table-column sortable prop="mail" label="邮箱">
              </el-table-column>
              <el-table-column sortable prop="phone" label="电话">
              </el-table-column>
              <el-table-column prop="id" label="操作">
                <template scope="scope">
                    <el-button type="text" size="small" @click="get_user_info(scope.row.id)">
                      编辑&nbsp
                    </el-button>
                  <el-button type="text" size="small" @click="del_user(scope.row.id)">删除</el-button>
                </template>
              </el-table-column>
            </data-tables>
          </div>

        </el-col>
      </el-row>
    </div>


    <el-dialog
      title="添加部门"
      :visible.sync="ShowAddChildDepartmentModal"
      size="tiny"
      >

      <el-input v-model.trim="NewDepartmentName"  placeholder="输入部门名称"></el-input>

      <span slot="footer" class="dialog-footer">
        <el-button @click="ShowAddChildDepartmentModal = false">取 消</el-button>
        <el-button type="primary" @click="create_department">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="修改部门"
      :visible.sync="ShowModifyChildDepartmentModal"
      size="tiny"
      >
      <el-input placeholder="输入部门名称" v-model.trim="treeNodeName"></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="ShowModifyChildDepartmentModal = false">取 消</el-button>
        <el-button type="primary" @click="modify_department">确 定</el-button>
      </span>
    </el-dialog>


    <el-dialog
      title="添加用户"
      :visible.sync="ShowAddUserModal"
      size="small"
      >
      <el-form :model="ruleForm" :rules="rules" label-position="center" ref="ruleForm" label-width="120px" class="demo-ruleForm">
        <el-form-item label="部门" >
            <el-input v-model.trim="treeNodeName" disabled></el-input>
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model.trim="ruleForm.username"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model.trim="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="pwd">
          <el-input v-model.trim="ruleForm.pwd" type="password"></el-input>
        </el-form-item>
        <el-form-item label="手机" prop="phone">
          <el-input v-model.trim="ruleForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="mail">
          <el-input v-model.trim="ruleForm.mail"></el-input>
        </el-form-item>
        <el-form-item label="地区" >
          <el-input v-model.trim="ruleForm.city"></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="ShowAddUserModal = false">取 消</el-button>
        <el-button type="primary" @click="UserSubmitForm('ruleForm','add')">保存</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="编辑用户"
      :visible.sync="ShowEditUserModal"
      size="small"
      >
      <el-form :model="editUserForm" :rules="rules" label-position="center" ref="editUserForm" label-width="120px" class="demo-ruleForm">
        <el-form-item label="部门" >
            <el-input v-model.trim="editUserForm.groupName" disabled></el-input>
        </el-form-item>
        <el-form-item label="用户名" >
          <el-input v-model.trim="editUserForm.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model.trim="editUserForm.name"></el-input>
        </el-form-item>
        <el-form-item label="" v-if="resetPwd ==0">
                  <el-button type="text" @click="resetPwd=1" >重置密码</el-button>
        </el-form-item>

        <el-form-item label="密码" prop="pwd" v-if="resetPwd==1">
          <el-input v-model.trim="editUserForm.pwd" type="password"></el-input>
          <el-button type="text" @click="resetPwd=0" >取消重置密码</el-button>
        </el-form-item>

        <el-form-item label="手机" prop="phone">
          <el-input v-model.trim="editUserForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="mail">
          <el-input v-model.trim="editUserForm.mail"></el-input>
        </el-form-item>
        <el-form-item label="地区" >
          <el-input v-model.trim="editUserForm.city"></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="ShowEditUserModal = false">取 消</el-button>
        <el-button type="primary" @click="UserSubmitForm('editUserForm','edit')">保存</el-button>
      </span>
    </el-dialog>



  </div>
</template>


<script>
import { DepartmentsTreeApiUrl, DepartmentsListApiUrl, UserListApiUrl} from '@/http/url'

export default {
  name: 'department',
  data() {
    return {
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
      rules:{
        name: { required: true, message: '请输入名称', trigger: 'blur' },
        username:{required:true,message:'请输入用户名',trigger:'blur'},
        pwd:{required:true,min:8,message:'请输入密码，长度不小于8位',trigger:'blur'},
        phone:{required:true,min:11,max:11,message:'请输入手机号，长度为11位',trigger:'blur'},
        mail:{required:true,message:'请输入邮箱',trigger:'blur'},
      },
      searchDef: {   //表格搜索内容显示
        inputProps: {
          placeholder: '搜索用户'
        }
      },
      actionsDef: {  //表格内动作
        colProps: {
            span: 19 //设置动作所在区域，把搜索条放在右边
        },
        def: [{
          name: '新增用户',
          handler: () => {
            this.ShowAddUserModal = true
          }
        }, ]
      },
      treeNodeId: '',  //当前选中的节点
      treeNodeName:'', //当前选中的节点名称
      NewDepartmentName:'', // 新的部门名称
      filterText: '',   //部门过滤文本
      department_tree:[],   //部门树数据
      defaultProps: {   //部门的显示内容
        children: 'children',
        label: 'name'
      },
      ShowAddChildDepartmentModal:false,
      ShowModifyChildDepartmentModal:false,
      user_list:[],
      ShowAddUserModal:false,
      ShowEditUserModal:false,
      resetPwd:false,
    };
  },
  methods: {
    create_department(){
      //新增部门
      var self = this
      if(self.NewDepartmentName==''){
        self.$message.error('部门名称不能为空！')
        return
      }
      var d = {
        parent_id:self.treeNodeId,
        name:self.NewDepartmentName
      }
      self.$http.post(DepartmentsListApiUrl, d).then((response)=>{
        self.$message(response.data.msg)
        if(response.data.status == 1){
          self.get_department_tree()
          self.ShowAddChildDepartmentModal=0
        }
      })
    },
    modify_department(){
      //修改部门
      var self = this
      if(self.treeNodeName==''){
        self.$message.error('部门名称不能为空！')
        return
      }
      var d={
        name:self.treeNodeName
      }
      self.$http.put(DepartmentsListApiUrl+'/'+self.treeNodeId, d).then((response)=>{
        self.$message(response.data.msg)
        if(response.data.status == 1 ){
          self.ShowModifyChildDepartmentModal = false
          self.get_department_tree()
        }
      })
    },
    delete_department(){
      //删除部门
      var self = this
      self.$http.delete(DepartmentsListApiUrl+'/'+self.treeNodeId).then((response)=>{
        self.$message(response.data.msg)
        if (response.data.status == 1){
          self.get_department_tree()
        }
      })
    },
    get_department_users(){
      //获取单个部门下的所有用户
      var self = this
      self.$http.get(UserListApiUrl+'?group_id='+self.treeNodeId).then((response)=>{
        self.user_list = response.data.result
      })
    },
    handleNodeClick(data) {
      //部门点击事件，把部门ID和名称赋值
      this.treeNodeId = data.id
      this.treeNodeName = data.name
      this.get_department_users()
    },
    get_department_tree(){
      //获取部门树
      var self = this
      self.$http.get(DepartmentsTreeApiUrl).then((response)=>{
        self.department_tree = response.data.result
        this.$refs.tree2.setCheckedKeys([2])
        // console.log('department tree',self.department_tree)
      })
    },
    del_user(id){
        var self = this
        this.$confirm('确定要删除当前用户吗? ', '警告').then(() => {
           self.$http.delete(UserListApiUrl+'/'+id).then((response)=>{
              self.$message(response.data.msg)
              if(response.data.msg){
                self.get_department_users()
              }
           })
        }).catch(() => {})
    },
    get_user_info(id){
      //获取单个用户信息
      var self = this
      self.ShowEditUserModal = true
      self.$http.get(UserListApiUrl+'/'+id).then((response)=>{
        self.editUserForm = response.data.result
      })
    },
    create_user(){
      this.ruleForm.group_id = this.treeNodeId
      var self = this
      self.$http.post(UserListApiUrl,self.ruleForm).then((response)=>{
        self.$message(response.data.msg)
        if(response.data.status == 1){
          self.ShowAddUserModal = 0
        }
      })
    },
    update_user(){
      //更新用户信息
      var self = this
      var user_id = self.editUserForm.id
      self.$http.put(UserListApiUrl+'/'+user_id, self.editUserForm).then((response)=>{
        self.$message(response.data.msg)
        if(response.data.status == 1){
          self.get_department_users()
          self.ShowEditUserModal = false
          self.resetPwd = false
        }
      })
    },
    UserSubmitForm(formName,method) {
      // 提交按钮
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (method == 'add'){
            self.create_user()
          }else if (method == 'edit'){
            self.update_user()
          }
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    filterNode(value, data) {
      if (!value) return true;
      return data.name.indexOf(value) !== -1;
    },
    departmentAction(action, store, data) {
      //部门操作，修改名称，添加子部门等
      if (action == 'add'){
        this.NewDepartmentName = ''
        this.ShowAddChildDepartmentModal = true
      }else if (action == 'modify'){
        this.ShowModifyChildDepartmentModal = true
      }else if (action == 'delete'){
        this.$confirm('确定要删除当前部门吗? ', '警告').then(() => {
          this.delete_department()
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
    renderContent(h, { node, data, store }) {
      //这里用的是jsx语法。
      return (
        <span>
        <span> { node.label } <span style="color:gray">({data.count}) </span> </span>
          <el-dropdown   onCommand={(action) => this.hostgroupAction(action, store, data) }  v-show={ data.id == this.treeNodeId } style="margin-left:40px">
            <span class="el-dropdown-link" >
              <i class="icon-pencil " ></i>
            </span>
          <el-dropdown-menu slot="dropdown" >
            <el-dropdown-item command="add" > 添加子部门 < /el-dropdown-item>
            <el-dropdown-item command="modify" > 修改部门名称 < /el-dropdown-item>
            <el-dropdown-item command="delete" > 删除部门 < /el-dropdown-item>
          </el-dropdown-menu>
          </el-dropdown>
        </span>
      )
    },
  },
  watch: {
    filterText(val) {
      this.$refs.tree2.filter(val);
    }
  },
  mounted(){
    console.log('mounted...')
    this.get_department_tree()
    window.heihei=this
  }

}

</script>
