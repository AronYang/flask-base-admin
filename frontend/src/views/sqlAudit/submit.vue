<template>
  <div>
    <a href="#/sqlaudit/submits/create">
      <el-button style="margin:0 0 10px 0"> <i class="icon-plus"></i>&nbsp手动新建工单</el-button>
    </a>
    <el-tooltip class="item" effect="dark" content="点击后，自动去后台svn拉取最新的sql目录，并自动生成工单" placement="top-start">
          <el-button style="margin:0 0 10px 0" @click="auto_create_submit"  :loading="auto_create_submit_loading"> <i class="icon-refresh"></i>&nbsp自动生成工单</el-button>
    </el-tooltip>
    <div class="card">
      <div class="card-body">
        <data-tables :data="tableData">
          <el-table-column prop="name" label="工单名称" sortable>
            <template scope="scope">
              <el-button type="text"  @click="$router.push(SubmitUpdatePage+scope.row.id)">{{scope.row.name}}</el-button>
            </template>
          </el-table-column>
          <el-table-column sortable prop="dbname" label="数据库名称">
          </el-table-column>
          <el-table-column sortable prop="reason" label="申请原因">
          </el-table-column>
          <el-table-column sortable prop="online_time" label="计划上线时间">
          </el-table-column>
          <el-table-column sortable prop="create_time" label="申请时间">
          </el-table-column>

          <el-table-column sortable prop="status" label="工单状态">
            <template scope="scope">
              <el-tag type="warning" v-if="scope.row.status==0">草稿</el-tag>
              <el-button type="danger" :plain="true"  size="small" v-if="scope.row.status==0" @click="del_submit(scope.row.id)">删除</el-button>
              <el-tag type="info" v-if="scope.row.status==1">待处理</el-tag>
              <el-button type="default" :plain="true"  size="small" v-if="scope.row.status==1" @click="action(scope.row.id,'revoke')">撤回</el-button>
              <el-tag type="primary" v-if="scope.row.status==2">处理中</el-tag>
              <el-tag type="success" v-if="scope.row.status==3">已结束</el-tag>
              <el-tag type="danger" v-if="scope.row.status==4">被打回</el-tag>
              <el-tag type="danger" v-if="scope.row.status==5">被否决</el-tag>
            </template>
          </el-table-column>
        </data-tables>

      </div>
    </div>
  </div>
</template>
<script>
import { SubmitListApiUrl, SubmitUpdatePage,SubmitRevokeApiUrl, SubmitAutoCreateApiUrl } from '../../http/url'
export default {
  name: 'submit',
  data() {
    return {
      tableData: [],
      submitInfo: {},
      showSqlContent: false,
      editorOption: {
        tabSize: 4,
        styleActiveLine: true,
        lineNumbers: true,
        line: true,
        mode: 'text/x-mysql',
        theme: 'solarized light',
        lineWrapping: true,
        readOnly: true,
      },
      auto_create_submit_loading:false,  
      SubmitUpdatePage: SubmitUpdatePage,
    }
  },
  methods: {
    get_submits() {
      var self = this
      this.$http.get(SubmitListApiUrl).then(function(response) {
        self.tableData = response.data.result
      })
    },
    del_submit(id) {
      var self = this
      this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {
        this.$http.delete(SubmitListApiUrl + '/' + id).then(function(response) {
          self.$message(response.data.msg)
          if (response.data.status == 1) {
            self.get_submits()
          }
        })
      }).catch(() => {})
    },
    // get_submit(id) {
    //   var self = this
    //   self.submitInfo = {}
    //   this.dialogTableVisible = true
    //   this.$http.get(SubmitListApiUrl + '/' + id).then(function(response) {
    //     self.submitInfo = response.data.result
    //   })
    // },
    action(id,action) {
      //用put方式，撤消按钮
      if (action == 'revoke'){
        this.$confirm('此操作撤回还未处理的工单, 是否继续?', '警告').then(() => {
          this.$http.put(SubmitRevokeApiUrl+'/'+id).then((response)=>{
            self.$message(response.data.msg)
            if (response.data.status == 1){
              self.get_submits()
            }
          })
        })
      }
      var self = this
    },
    copySucess() {
      this.$message('SQL内容复制成功！')
    },
    auto_create_submit() {
      var self = this
      self.auto_create_submit_loading = true 
      self.$http.put(SubmitAutoCreateApiUrl).then((response)=>{
        self.$alert(response.data.msg, '提示', {
          dangerouslyUseHTMLString: true,
        })
        self.auto_create_submit_loading = false 
        this.get_submits()
      })
    },
  },
  mounted() {
    this.get_submits()
  }
}
  
</script>
