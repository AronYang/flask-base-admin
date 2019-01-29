<template>
    <div>
        <div class="card">
            <div class="card-body">

                <data-tables :data="tableData"  :actions-def="actionsDef">
                    <el-table-column sortable prop="name" label="任务名称">
                    </el-table-column>
                    <el-table-column sortable prop="ssh_user" label="执行用户">
                    </el-table-column>
                    <el-table-column sortable prop="operator" label="操作人">
                    </el-table-column>
                    <el-table-column sortable prop="create_time" label="创建时间">
                    </el-table-column>
                    <el-table-column sortable prop="update_time" label="统计">
                        <template scope="scope">
                            total:{{scope.row.total_count}} success:{{scope.row.success_count}}  failed:{{scope.row.failed_count}}

                        </template>
                    </el-table-column>
                    <el-table-column sortable prop="update_time" label="状态">
                        <template scope="scope">
                            <el-tag type="success" v-if="scope.row.total_count == scope.row.success_count">成功</el-tag>
                            <el-tag type="danger" v-if="scope.row.total_count == scope.row.failed_count">失败</el-tag>
                            <el-tag type="warning" v-if="scope.row.total_count > scope.row.success_count && scope.row.success_count > 0">部分成功</el-tag>
                            <el-tag type="primary" v-if="scope.row.success_count == 0 && scope.row.failed_count == 0">等待执行</el-tag>

                        </template>

                    </el-table-column>

                    <el-table-column prop="id" label="操作">
                        <template scope="scope">
                            <el-button type="text" size="small" @click="show_scripts(scope.row.id)">解析</el-button>
                            &nbsp

                            <router-link :to="$route.path+'/'+scope.row.id">
                                <el-button type="text" size="small">
                                    执行
                                </el-button>
                            </router-link>
                            &nbsp

                            <el-button type="text" size="small" @click="del_execute(scope.row.id)"  v-if="scope.row.success_count == 0 && scope.row.failed_count == 0">删除</el-button>

                        </template>
                    </el-table-column>
                </data-tables>
            </div>
        </div>


    <el-dialog
      title="查看脚本内容"
      :visible.sync="ShowScriptContentModal"
      size="small"
      >
              <el-tabs v-model="tab_name" >

                <el-tab-pane :label="script.name" :name="script.name" :key="script.name" v-for="script in script_content_list">
                    <pre>{{script.script_content}}</pre>
                </el-tab-pane>

<!--                 <el-tab-pane label="配置管理" name="second">配置管理</el-tab-pane>
                <el-tab-pane label="角色管理" name="third">角色管理</el-tab-pane>
                <el-tab-pane label="定时任务补偿" name="fourth">定时任务补偿</el-tab-pane>
 -->
              </el-tabs>
      <span slot="footer" class="dialog-footer">
        <el-button @click="ShowScriptContentModal = false">关闭</el-button>
      </span>
    </el-dialog>

    </div>
</template>


<script>

import { ToolExecutesApi } from '../../http/url'

export default {
    name: 'script',
    data() {
        return {
            actionsDef: { //表格动作配置
                colProps: {
                    span: 19    //设置动作所在区域，把搜索条放在右边
                },
                def: [{
                        name: '新增任务',
                        icon: 'plus',
                        buttonProps: { type: 'primary' },
                        handler: () => {
                            this.to_create_new_execute()
                        }
                    },
                ]
            },
            tableData:[],
            tag_list:[], //分类名称
            script_content_list:[], //脚本列表
            tab_name:'',
            ShowScriptContentModal:false
        }
    },
    methods:{
        get_execute_list(){
              var self  = this
              this.$http.get(ToolExecutesApi).then(function(response) {
                    self.tableData = response.data.result
              })
        },
        // get_tag_list(){
        // //获取分类列表
        //     var self = this
        //     this.$http.get(ToolScriptsTagsApi).then((response)=>{
        //         self.tag_list = response.data.result
        //     })
        // },
        to_create_new_execute(){
            this.$router.push( this.$route.path + '/create')
        },
        del_execute(execute_id){
              var self = this
              this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {
                self.$http.delete(ToolExecutesApi + '/' + execute_id).then((response) => {
                  self.$message(response.data.msg)
                  if (response.data.status == 1) {
                    self.get_execute_list()
                  }
                })
              }).catch(() => {})
        },
        show_scripts(execute_id){
            var self = this
            this.ShowScriptContentModal = true
            this.script_content_list = []
            self.$http.get(ToolExecutesApi + '/' + execute_id+'/scripts').then((res)=>{
                self.script_content_list = res.data.result
                self.tab_name = self.script_content_list[0].name
            })

        }
    },
    mounted(){
        this.get_execute_list()
    }

}

</script>
