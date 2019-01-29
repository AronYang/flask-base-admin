<template>
    <div>
        <div class="card">
            <div class="card-body">

                <data-tables :data="tableData"  :actions-def="actionsDef">
                    <el-table-column sortable prop="name" label="任务名称">
                    </el-table-column>

                    <el-table-column sortable prop="depend" label="脚本关系">
                        <template scope="scope">
                            <div v-if="scope.row.depend == 1">与</div>
                            <div  v-if="scope.row.depend == 0">或</div>
                        </template>
                    </el-table-column>

<!--                     <el-table-column sortable prop="is_valid" label="是否有效">
                        <template scope="scope">
                            <el-tag  type="primary" v-if="scope.row.is_valid == 1">有效</el-tag>
                            <el-tag  v-if="scope.row.is_valid == 0">无效</el-tag>
                        </template>
                    </el-table-column> -->

                    <el-table-column sortable prop="remark" label="说明">
                    </el-table-column>
                    <el-table-column sortable prop="update_time" label="更新时间">
                    </el-table-column>

                    <el-table-column prop="id" label="操作">
                        <template scope="scope">
                            <router-link :to="$route.path+'/'+scope.row.id">
                                <el-button type="text" size="small">
                                    编辑
                                </el-button>
                            </router-link>
                            <el-button type="text" size="small" @click="del_chain(scope.row.id)">删除</el-button>
                        </template>
                    </el-table-column>
                </data-tables>
            </div>
        </div>
    </div>
</template>


<script>

import { ToolChainsApi, ToolScriptsTagsApi } from '../../http/url'

export default {
    name: 'script',
    data() {
        return {
            actionsDef: { //表格动作配置
                colProps: {
                    span: 19    //设置动作所在区域，把搜索条放在右边
                },
                def: [{
                        name: '新增任务链',
                        icon: 'plus',
                        buttonProps: { type: 'primary' },
                        handler: () => {
                            this.to_create_new_chain()
                        }
                    },
                ]
            },
            tableData:[],
            tag_list:[], //分类名称
        }
    },
    methods:{
        get_chain_list(){
              var self  = this
              this.$http.get(ToolChainsApi).then(function(response) {
                    self.tableData = response.data.result
              })
        },
        get_tag_list(){
        //获取分类列表
            var self = this
            this.$http.get(ToolScriptsTagsApi).then((response)=>{
                self.tag_list = response.data.result
            })
        },
        to_create_new_chain(){
            this.$router.push( this.$route.path + '/create')
        },
        del_chain(chain_id){
              var self = this
              this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {
                self.$http.delete(ToolChainsApi + '/' + chain_id).then((response) => {
                  self.$message(response.data.msg)
                  if (response.data.status == 1) {
                    self.get_chain_list()
                  }
                })
              }).catch(() => {})
        }
    },
    mounted(){
        this.get_chain_list()
    }

}

</script>
