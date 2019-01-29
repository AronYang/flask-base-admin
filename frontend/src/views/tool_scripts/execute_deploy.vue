<template>
  <div>
    <!--     <div class="card">
      <div class="card-body">
      </div>
    </div>
 -->
    <div class="card">
      <div class="card-body">
        <h6>
            <span v-if="executeInfo.from_type=='script'">脚本：</span>
            <span v-if="executeInfo.from_type=='chain'">脚本链：</span>

               <span style="color:green"> {{executeInfo.execute_name}}</span> &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
            <el-tag >总数：{{executeInfo.tasks.length}}</el-tag>
            <el-tag type="success" >成功数：{{success_count}}</el-tag>
            <el-tag type="danger">失败数：{{failed_count}}</el-tag>

            <el-button type="danger" style="float:right" @click='execute_task'> <i class="icon-shuffle "></i> &nbsp执行</el-button>

            <el-button type="primary" style="float:right;margin-right:10px" @click="$router.go(-1)" ><i class="icon-action-undo "></i>&nbsp返回</el-button>

        </h6>
        <br>
        <el-table :data="executeInfo.tasks"  >
<!--           <el-table-column type="selection" width="55" >
          </el-table-column> -->
          <el-table-column  prop="id" label="全选" :render-header="render_header" width="65">
            <template scope="scope">
              <el-checkbox :label="scope.row.id"  v-model="select_tasks[scope.row.id]">&nbsp</el-checkbox>
            </template>
          </el-table-column>

          <el-table-column sortable prop="ip" label="IP">
          </el-table-column>

          <el-table-column sortable prop="ip" label="脚本结果统计">
            <template scope="scope">
                <div>{{scope.row.script_success_count}}/{{scope.row.script_total_count}}</div>
            </template>
          </el-table-column>


          <el-table-column sortable prop="status" label="执行状态">
            <template scope="scope">

              <el-tag type="primary" v-if="scope.row.status == 0">成功</el-tag>
              <el-tag type="danger" v-if="scope.row.status == 1">失败</el-tag>
              <img src="/static/img/loading.gif" v-if="scope.row.status==null && scope.row.deploy_tag == 1"></img>

            </template>
          </el-table-column>

          <el-table-column sortable prop="status" label="花费时间">
             <template scope="scope">
                    <div v-if="scope.row.end_time != null ">
                            {{scope.row.end_time - scope.row.start_time}} &nbsp秒
                    </div>
             </template>
          </el-table-column>

          <el-table-column prop="id" label="详情">
            <template scope="scope">
              <el-button type="text" size="small" @click="show_task_log(scope.row)">详情</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>


    <el-dialog
      title="执行结果"
      :visible.sync="ShowTaskLogModal"
      size="small"
      >
      <div>{{task_result.ip}}</div>
      <pre style="background-color:rgb(228,229,230)">{{task_result.result}}</pre>

      <span slot="footer" class="dialog-footer">
        <el-button @click="ShowTaskLogModal = false">关闭</el-button>
      </span>
    </el-dialog>


  </div>
</template>
<script>
  import { ToolExecutesApi } from '@/http/url'
  export default {
    name: 'executeDeploy',
    data() {
      return {
        select_tasks:{},
        select_all_tag:true,
        task_result:'',
        ShowTaskLogModal:false,
        executeInfo: {
          tasks:[],
        },
      }
    },
    computed:{
      failed_count(){
        var failed_count = 0
        for (var n in this.executeInfo.tasks){
            if (this.executeInfo.tasks[n].status == 1){
              failed_count = failed_count + 1
            }
        }
        return failed_count
      },
      success_count(){
        var success_count = 0
        for (var n in this.executeInfo.tasks){
            if (this.executeInfo.tasks[n].status == 1){
              success_count = success_count + 1
            }
        }
        return success_count
      }
    },
    methods: {
      get_execute_info() {
        //获取任务信息
        var execute_id = this.$route.params.id
        var self = this
        var selection = []
        for (var n in this.multipleSelection){
          selection.push(this.multipleSelection[n])
        }

        this.$http.get(ToolExecutesApi + '/' + execute_id).then((res) => {
          for (var n in res.data.result.tasks){
            var data = res.data.result.tasks[n]
            if (self.select_tasks.hasOwnProperty(data.id) == false){
                self.select_tasks[data.id.toString()]=true
            }
          }
          self.executeInfo = res.data.result

          self.selectionTest()

          setTimeout(function() {
              self.get_execute_info()
          }, 2000)

        })
      },
      execute_task() {
        //执行任务
        var execute_id = this.$route.params.id
        var self = this
        var task_ids = []
        for (var k in this.select_tasks) {
          task_ids.push(k)
        }
        var data = {
          task_ids: task_ids
        }

        if (task_ids == ''){
          this.$message.error('请选择主机！')
          return
        }

        this.$http.put(ToolExecutesApi + '/' + execute_id, data).then((res) => {
          self.$message(res.data.msg)
        })
      },
      show_task_log(row) {
        //查看单个任务的执行详情
        this.task_result = row
        // this.task_result = row.result
        this.ShowTaskLogModal = true
      },

      selectionTest(){
        //刷新字典
        this.select_tasks = Object.assign({},this.select_tasks)
      },
      render_header(creatElement, { column, $index }){
        //返回表格自定义头部
        return creatElement('el-checkbox',{
              on: { change: this.ToggleSelectAll },
            }, '全选')
      },
      ToggleSelectAll(){
        //全选控制按钮
        var status = true
        if (this.select_all_tag == false){
          this.select_all_tag = true
          status = false
        }else{
          this.select_all_tag = false
        }

        for (var n in this.executeInfo.tasks){
            var data = this.executeInfo.tasks[n]
            this.select_tasks[data.id]= status
          }
        this.select_tasks = Object.assign({},this.select_tasks)
      }

    },
    mounted() {
      this.get_execute_info()
    }
  }

</script>
