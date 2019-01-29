<template>
    <div>
        <div style="margin-bottom:15px">
            <el-select v-model="filter.idc_id" placeholder="--所有变量--">
                <el-option label="--所有变量--" :value="-1"></el-option>
                <el-option label="默认" value=""></el-option>
                <el-option v-for="idc in idc_list" :key="idc.id" :label="idc.name" :value="idc.id"> </el-option>
            </el-select>

            <el-input style="width:400px" v-model="filter.search" placeholder="搜索变量"></el-input>
            <el-button @click="get_variable_list">搜索</el-button>
        </div>

        <div class="card">
            <div class="card-body">

                <data-tables :data="tableData"  :actions-def="actionsDef">
                    <el-table-column sortable prop="name" label="变量名称">
                    </el-table-column>
                    <el-table-column sortable prop="value" label="值">
                    </el-table-column>

                    <el-table-column sortable prop="remark" label="描述">
                    </el-table-column>
                    <el-table-column sortable prop="idc_name" label="所属机房">
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

import { SyssetVariableApi,   IdcApi } from '../../http/url'

export default {
    name: 'variable',
    data() {
        return {
            actionsDef: { //表格动作配置
                colProps: {
                    span: 19    //设置动作所在区域，把搜索条放在右边
                },
                def: [{
                        name: '新增变量',
                        icon: 'plus',
                        buttonProps: { type: 'primary' },
                        handler: () => {
                            this.to_create_new_variable()
                        }
                    },
                ]
            },
            filter:{
                search:'',
                idc_id:-1,
            },
            tableData:[],
            idc_list: [], //IDC列表
        }
    },
    methods:{
        get_idc_list() {
            //获取idc的列表，并改为text,value格式，方便页面做过滤。
            var self = this
            this.$http.get(IdcApi).then(function(response) {
                self.idc_list = response.data.result
            })
        },
        get_variable_list(){
              var self  = this
              this.$router.push({path:this.$route.path,query:this.filter})  //在查询api的时候,把当前页面的url也进行跳转,把参数都加到当前url上.
              this.$http.get(SyssetVariableApi,{params:self.filter}).then(function(response) {
                    self.tableData = response.data.result
              })
        },
        to_create_new_variable(){
            this.$router.push( this.$route.path + '/create')
        },
        del_ssh_user(ssh_user_id){
              var self = this
              this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {
                self.$http.delete(SyssetVariableApi + '/' + ssh_user_id).then((response) => {
                  self.$message(response.data.msg)
                  if (response.data.status == 1) {
                    self.get_variable_list()
                  }
                })
              }).catch(() => {})
        },
        get_filter_params(){
            //获取url过滤的参数,方便返回到该页面时,直接能够找到之前的过滤条件
            var idc_id = this.$route.query.idc_id
            this.filter.search = this.$route.query.search

            console.log('idc_id',idc_id)
            if (idc_id == undefined){
                return
            }

            if(idc_id != ''){
                idc_id = Number(idc_id)
            }
            this.filter.idc_id = idc_id
        },
    },
    mounted(){
        this.get_filter_params()
        this.get_variable_list()
        this.get_idc_list()
    }

}

</script>
