<template>
  <div>
    <div class="card">
      <div class="card-body">
        <template>
          <el-radio-group v-model="handletag" @change="get_confirms">
            <el-radio label="0">待审核工单</el-radio>
            <el-radio label="1">已审核工单</el-radio>
          </el-radio-group>
        </template>
    <el-tooltip class="item" effect="dark" content="点击后，自动去后台svn拉取最新的sql目录，并自动生成工单" placement="top-start" style="float:right;">
          <el-button style="margin:0 0 10px 0" @click="auto_create_submit"  :loading="auto_create_submit_loading"> <i class="icon-refresh"></i>&nbsp自动生成工单</el-button>
    </el-tooltip>


        <data-tables :data="tableData"  >
          <el-table-column prop="name" label="工单名称" sortable>
            <template scope="scope">
              <!-- <el-button type="text" @click="$router.push(ConfirmUpdatePage+scope.row.id)">{{scope.row.name}}</el-button> -->
              {{scope.row.name}}
            </template>
          </el-table-column>
          <el-table-column sortable prop="reason" label="申请原因">
          </el-table-column>
          <el-table-column sortable prop="flowName" label="流程名称">
          </el-table-column>
          <el-table-column sortable prop="submitterName" label="申请人" width="100">
          </el-table-column>
          <el-table-column sortable prop="svntag" label="SQL来源">
            <template scope="scope">
              <span v-if="scope.row.svntag==1">SVN
                <span class="text-muted">({{scope.row.svndirname}}) </span>
              </span>
              <span v-if="scope.row.svntag!=1">默认</span>
            </template>
          </el-table-column>
          <el-table-column sortable prop="nodeName" label="当前步骤">
          </el-table-column>
<!--           <el-table-column sortable prop="nodeUser" label="当前审核人">
          </el-table-column>
 --><!--           <el-table-column sortable prop="online_time" label="计划上线时间">
          </el-table-column> -->


          <el-table-column sortable prop="create_time" label="申请时间">
          </el-table-column>
          <el-table-column sortable prop="status" label="工单状态" width="120">
            <template scope="scope">
              <el-tag type="warning" v-if="scope.row.status==0">草稿</el-tag>
              <el-tag type="info" v-if="scope.row.status==1">待处理</el-tag>
              <el-tag type="primary" v-if="scope.row.status==2">处理中</el-tag>
              <el-tag type="success" v-if="scope.row.status==3">已结束</el-tag>
              <el-tag type="danger" v-if="scope.row.status==4">被打回</el-tag>
              <el-tag type="danger" v-if="scope.row.status==5">被否决</el-tag>
            </template>
          </el-table-column >
          <el-table-column label='操作'>
            <template scope="scope">
              <el-button type="text" @click="$router.push(ConfirmUpdatePage+scope.row.id)">审核</el-button>
              <el-button type="text" @click="$router.push(ConfirmExecPage+scope.row.id)">执行</el-button>
            </template>

          </el-table-column>
          <!--           <el-table-column prop="id" label="操作">
            <template scope="scope">
              <el-button type="text" size="small" @click="get_submit(scope.row.id)">查看</el-button>
              <el-button type="text" size="small" v-if="scope.row.status == 0 ||scope.row.status==2" @click="autoAuditDialogVisible = true; selectId=scope.row.id">执行语句</el-button>
              <el-button type="text" size="small" v-if="scope.row.status == 0||scope.row.status==2" @click="auditPass(scope.row.id)">审核通过</el-button>
              <el-button type="text" size="small" v-if="scope.row.status == 3" @click="showAuditResult = true; get_result(scope.row.id);">查看执行过程</el-button>
            </template>
          </el-table-column> -->
        </data-tables>
      </div>
    </div>
    <!-- 查看弹出层 -->
    <el-dialog title="工单信息" :visible.sync="dialogTableVisible">
      <table class="table   table-bordered">
        <tbody>
          <tr>
            <td>工单名称</td>
            <td>{{submitInfo.name}}</td>
          </tr>
          <tr>
            <td>申请原因</td>
            <td>{{submitInfo.reason}}</td>
          </tr>
          <tr>
            <td>相关审核人员</td>
            <td>{{submitInfo.configOperatorName}}</td>
          </tr>
          <tr>
            <td>申请人</td>
            <td>{{submitInfo.submiterName}}</td>
          </tr>
          <tr>
            <td>申请时间</td>
            <td>{{submitInfo.create_time}}</td>
          </tr>
          <tr>
            <td>数据库信息</td>
            <td>{{submitInfo.configName}}</td>
          </tr>
          <tr>
            <td>SQL内容</td>
            <td>
              {{submitInfo.sql_filename}}
              <button class="btn btn-link" @click="showSqlContent = 1" v-if="showSqlContent==0">显示</button>
              <button class="btn btn-link" @click="showSqlContent = 0" v-if="showSqlContent==1">隐藏</button>
            </td>
          </tr>
          <tr v-if="showSqlContent">
            <td colspan="2">
              <el-col>
                <div class="text-right">
                  <button class="btn btn-link" v-clipboard:copy="submitInfo.sqlContent" v-clipboard:success="copySucess">复制</button>
                  <!--                   <button class="btn btn-link"> <a :href="submitInfo.downloadurl" :download="submitInfo.sql_filename">下载文件</a> </button> -->
                </div>
                <codemirror v-model="submitInfo.sqlContent" :options="editorOption"></codemirror>
              </el-col>
            </td>
          </tr>
          <tr>
            <td>工单状态</td>
            <td>
              <span v-if='submitInfo.status == 0'>草稿</span>
              <span v-if='submitInfo.status == 1'>待处理</span>
              <span v-if='submitInfo.status == 2' class="text-danger">处理中</span>
              <span v-if='submitInfo.status == 3' class="text-success">已结束</span>
            </td>
          </tr>
          <tr>
            <td>审核人</td>
            <td>{{submitInfo.operatorName}}</td>
          </tr>
        </tbody>
      </table>
      <span slot="footer" class="dialog-footer">
            <!-- <el-button @click="dialogTableVisible = false">取 消</el-button> -->
            <el-button type="primary" @click="dialogTableVisible = false">关闭</el-button>
          </span>
    </el-dialog>
    <!--     <el-dialog
    title="提示"
    :visible.sync="auditDialogVisible"
    size="tiny"
    >
    <span>确定要把状态置为已处理吗？</span>
    <p class="text-muted"><small>请在处理前，手动下载sql内容在数据库执行</small></p>
    <span slot="footer" class="dialog-footer">
      <el-button @click="auditDialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="audit('audit')">确 定</el-button>
    </span>
  </el-dialog> -->
    <el-dialog title="提示" :visible.sync="autoAuditDialogVisible" size="tiny">
      <span>你确定要自动执行SQL内容吗？</span>
      <p class="text-muted"><small></small></p>
      <span slot="footer" class="dialog-footer">
      <el-button @click="autoAuditDialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="audit('autoaudit')">确 定</el-button>
    </span>
    </el-dialog>
    <el-dialog title="执行过程" :visible.sync="showAuditResult">
      <table class="table   table-bordered">
        <tr>
          <td>类型</td>
          <td>SQL</td>
          <td>影响行数</td>
          <td>状态</td>
          <td>结果</td>
        </tr>
        <tr v-for="result in result_list">
          <td>{{result.type}}</td>
          <td>{{result.sql}}</td>
          <td>{{result.rowcount}}</td>
          <td>
            <span class="badge badge-success" v-if="result.status == 1">成功</span>
            <span class="badge badge-danger" v-if="result.status == 0">失败</span>
          </td>
          <td>{{result.result}}</td>
        </tr>
      </table>
      <span slot="footer" class="dialog-footer">
      <el-button @click="showAuditResult = false">关闭</el-button>
      <!-- <el-button type="primary" @click="audit('autoaudit')">确 定</el-button> -->
    </span>
    </el-dialog>
  </div>
</template>
<script>
import { ConfirmListApiUrl, ConfirmUpdatePage, SubmitAutoCreateApiUrl, ConfirmExecPage} from '@/http/url'
export default {
  name: 'submit',
  data() {
    return {
      tableData: [],
      copyData: 'copy data.',
      dialogTableVisible: false, //查看modal显示
      auditDialogVisible: false, //手动审核modal显示
      autoAuditDialogVisible: false, //自动审核modal显示
      submitInfo: {},
      showSqlContent: false,
      showAuditResult: false,
      selectId: '',
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
      result_list: [],
      handletag: '0', //待审核与已审核标记
      ConfirmUpdatePage:ConfirmUpdatePage,
      ConfirmExecPage:ConfirmExecPage,
      auto_create_submit_loading:false,  
    }
  },
  methods: {
    get_confirms() {
      console.log('get confirms')
      var self = this

      this.$http.get(ConfirmListApiUrl + '?handletag=' + self.handletag).then(function(response) {
        self.tableData = response.data.result
      })
    },
    del_confirm(id) {
      var self = this
      this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {
        this.$http.delete(ConfirmListApiUrl + '/' + id).then(function(response) {
          self.$message(response.data.msg)
          if (response.data.status == 1) {
            self.get_confirms()
          }
        })
      }).catch(() => {})
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
    this.get_confirms()
  }
}

</script>
