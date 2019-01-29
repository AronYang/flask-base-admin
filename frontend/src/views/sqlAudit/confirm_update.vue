<template>
  <div>
    <div class="card">
      <div class="card-body">
        <span class="text-muted">工单操作：</span>
        <el-button type="primary" @click="auditAction('pass')" :disabled="ruleForm.current_action_status==0">通过</el-button>
        <el-button type="warning" @click="auditAction('back')" :disabled="ruleForm.current_action_status==0">打回</el-button>
        <!--         <el-button type="danger" @click="auditAction('reject')" :disabled="ruleForm.current_action_status==0">否决</el-button> -->
        <el-button @click="auditAction('revoke')">撤回</el-button>
      </div>
    </div>


    <div class="card">
      <div class="card-body">
          <el-col :span='24'>
            <table class="table   table-bordered">
              <tbody>
                <tr>
                  <td class="text-muted">工单名称</td>
                  <td>{{ruleForm.name}}</td>
                  <td class="text-muted">申请人</td>
                  <td>{{ruleForm.submitterName}}</td>
                </tr>
                <tr>
                  <td class="text-muted">申请数据库</td>
                  <td>{{ruleForm.dbname}}</td>
                  <td class="text-muted">申请原因</td>
                  <td>{{ruleForm.reason}}</td>
                </tr>
                <tr>
                  <td class='text-muted'>工单状态</td>
                  <td>
                    <el-tag type="default" v-if="ruleForm.status==0">待提交</el-tag>
                    <el-tag type="info" v-if="ruleForm.status==1">待处理</el-tag>
                    <el-tag type="primary" v-if="ruleForm.status==2">处理中</el-tag>
                    <el-tag type="success" v-if="ruleForm.status==3">已结束</el-tag>
                    <el-tag type="danger" v-if="ruleForm.status==4">被打回</el-tag>
                    <el-tag type="danger" v-if="ruleForm.status==5">被否决</el-tag>
                  </td>
                  <td class="text-muted">申请时间</td>
                  <td>{{ruleForm.create_time}}</td>
                </tr>
                <tr v-if="ruleForm.svntag==1">
                  <td class="text-muted">svn目录</td>
                  <td>{{ruleForm.svndirname}}</td>
                  <td class="text-muted">svn版本</td>
                  <td>{{ruleForm.svn_version}}</td>
                </tr>
                <tr>
                  <td class="text-muted">所属流程</td>
                  <td>{{ruleForm.flow.name}}</td>
                  <td class="text-muted">计划上线时间</td>
                  <td>{{ruleForm.online_time}}</td>
                </tr>
                <tr>
                  <td class="text-muted">步骤列表</td>
                  <td colspan=3>
                    <template>
                      <el-steps :space="80" direction="vertical" :active="current_step" style='margin-top:15px'>
                        <el-step :title="n.name" :key="n.id" :description="'描述:'+n.description + ' 审核人:'+ n.operatorNames" v-for="n in ruleForm.nodes"></el-step>
                      </el-steps>
                    </template>
                  </td>
                </tr>
                <tr>
                  <td class="text-muted">操作记录</td>
                  <td colspan=3>
                    <div v-for="record in ruleForm.records">
                      <span class="text-muted">&nbsp&nbsp节点：</span> {{record.nodeName}}
                      <span class="text-muted">&nbsp&nbsp审批人：</span>{{record.operatorName}}
                      <span class="text-muted">&nbsp&nbsp操作：
                            <span v-if="record.node_action == 1" class="text-success">通过</span>
                      <span v-if="record.node_action == 2" class="text-danger">退回</span>
                      <span v-if="record.node_action == 3" class="text-danger">否决</span>
                      <span v-if="record.node_action == 4" class="text-warning">撤回</span>
                      <span v-if="record.node_action == 5" class="text-info">执行</span>
                      </span>
                      <span class="text-muted">&nbsp&nbsp时间：</span>
                      <span style="color:gray">{{record.update_time}}</span>
                      <span class="text-muted">&nbsp&nbsp说明：</span>
                      <span>{{record.node_note}}</span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class='text-muted'>SQL来源</td>
                  <td colspan=3>
                    <span v-if="ruleForm.svntag == 1">SVN获取</span>
                    <span v-else>手动输入</span>
                  </td>
                </tr>
                <tr v-if="ruleForm.svntag != 1">
                  <td class='text-muted'>SQL内容</td>
                  <td colspan=3>
                    <div class="text-left">
                      <button class="btn btn-link" v-clipboard:copy="ruleForm.sqlContent" v-clipboard:success="copySucess">复制SQL文本</button>
                      <button class='btn btn-link' @click="showSqlContent = 0" v-if="showSqlContent==1">隐藏SQL内容</button>
                      <button class='btn btn-link' @click="showSqlContent = 1" v-if="showSqlContent==0">显示SQL内容</button>
                    </div>
                    <div v-if="showSqlContent ==  1">
                      <codemirror v-model="ruleForm.sqlContent" :options="editorOption"></codemirror>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </el-col>
    </div>
    </div>

  </div>
  <!-- </div> -->
</template>
<script>
import { FlowListApiUrl, ConfirmActionApiUrl, ConfirmListApiUrl, ConfirmExecApiUrl, ConfirmListPage, ConfirmGetSvnSqlContent, InstanceListApiUrl, ConfirmCheckApiUrl } from '@/http/url'
export default {
  name: 'confirmUpdate',
  data() {
    return {
      form: {},
      ruleForm: {
        name: '',
      },
      flow_list: [],
      editorOption: {
        tabSize: 4,
        height: 1000,
        styleActiveLine: true,
        lineNumbers: true,
        line: true,
        mode: 'text/x-mysql',
        theme: 'solarized light',
        lineWrapping: true,
        readOnly: true,
      },
    }
  },
  computed: {
    current_step() {
      var num = 0
      for (var n in this.ruleForm.nodes) {
        var node = this.ruleForm.nodes[n]
        if (node.id == this.ruleForm.node_id) {
          console.log('n.', n)
          var n = Number(n)
          num = n + 1
          break
        }
      }
      console.log(num, typeof(num))
      return num
    }
  },

  methods: {
    get_actionname(action) {
      //返回动作对应的名称
      if (action == 'pass') {
        return '通过'
      } else if (action == 'revoke') {
        return '撤回'
      } else if (action == 'back') {
        return '打回'
      } else if (action == 'reject') {
        return '否决'
      }
    },
    copySucess() {
      this.$message('SQL内容复制成功！')
    },
    auditAction(action) {
      //执行审核动作
      var id = this.$route.params.id
      var action_name = this.get_actionname(action)

      var data = {
        id: id,
        action: action,
        reason: '',
      }
      var self = this
      this.$prompt('' + action_name + '理由： ', '[审核' + action_name + ']操作', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({ value }) => {
        data.reason = value
        self.$http.put(ConfirmActionApiUrl, data).then((response) => {
          self.$message(response.data.msg)
          if (response.data.status == 1) {
            self.$router.push(ConfirmListPage)
          }
        })
      }).catch(() => {});
    },
    get_confirm_info() {
      //获取单个工单的详细信息
      var id = this.$route.params.id
      var self = this
      this.$http.get(ConfirmListApiUrl + '/' + id).then((response) => {
        self.ruleForm = response.data.result
      })
    },


  },
  mounted() {
    this.get_confirm_info()
  }
}

</script>
