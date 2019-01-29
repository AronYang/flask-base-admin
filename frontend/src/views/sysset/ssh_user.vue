<template>
    <div>

        <div class="card">
            <div class="card-body">

                <data-tables :data="tableData"  :actions-def="actionsDef">
                    <el-table-column sortable prop="username" label="ssh用户名">
                    </el-table-column>
                    <el-table-column sortable prop="describe" label="描述">
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
                            <el-button type="text" size="small" @click="del_ssh_user(scope.row.id)">删除</el-button>
                        </template>
                    </el-table-column>
                </data-tables>
            </div>
        </div>
    </div>
</template>


<script>

import { SyssetSshUserApi } from '../../http/url'

export default {
    name: 'ssh_user',
    data() {
        return {
            actionsDef: { //表格动作配置
                colProps: {
                    span: 19    //设置动作所在区域，把搜索条放在右边
                },
                def: [{
                        name: '新增SSH用户',
                        icon: 'plus',
                        buttonProps: { type: 'primary' },
                        handler: () => {
                            this.to_create_new_ssh_user()
                        }
                    },
                ]
            },
            tableData:[],
        }
    },
    methods:{
        get_ssh_user_list(){
              var self  = this
              this.$http.get(SyssetSshUserApi).then(function(response) {
                    self.tableData = response.data.result
              })
        },
        to_create_new_ssh_user(){
            this.$router.push( this.$route.path + '/create')
        },
        del_ssh_user(ssh_user_id){
              var self = this
              this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {
                self.$http.delete(SyssetSshUserApi + '/' + ssh_user_id).then((response) => {
                  self.$message(response.data.msg)
                  if (response.data.status == 1) {
                    self.get_ssh_user_list()
                  }
                })
              }).catch(() => {})
        }
    },
    mounted(){
        this.get_ssh_user_list()
    }

}

</script>
