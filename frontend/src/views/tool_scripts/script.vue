<template>
    <div>
        <div style="margin-bottom:15px">
            <el-select v-model="filter.tag" placeholder="--分类--">
                <el-option label="--分类--" value=""></el-option>
                <el-option v-for="tag in tag_list" :key="tag" :value="tag">{{tag}}
                </el-option>
            </el-select>

            <el-input style="width:400px" v-model="filter.search" placeholder="搜索脚本名称"></el-input>
            <el-button @click="get_script_list">搜索</el-button>
            <el-button type="primary" style="float:right" @click="$router.push($route.path+'/create')"><i class="el-icon-plus"></i>新增脚本</el-button>
        </div>

        <div class="card">

            <div class="card-body">

<div v-for="v_list,k in dataDict">
    <div>{{k}}
    <hr>
            <el-button v-for="v in v_list" :key="v" @click="$router.push($route.path+'/'+v.id+'/exec')">{{v.name}}</el-button>
    <br><br><br>
    </div>
</div>


<!--                 <data-tables :data="tableData"  :actions-def="actionsDef">
                    <el-table-column sortable prop="name" label="脚本名">
                    </el-table-column>
                    <el-table-column sortable prop="type" label="脚本类型">
                    </el-table-column>
                    <el-table-column sortable prop="tag" label="所属分类">
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
                            <el-button type="text" size="small" @click="del_script(scope.row.id)">删除</el-button>
                        </template>
                    </el-table-column>
                </data-tables>
 -->
            </div>
        </div>
    </div>
</template>


<script>

import { ToolScriptsApi, ToolScriptsTagsApi } from '../../http/url'

export default {
    name: 'script',
    data() {
        return {
            actionsDef: { //表格动作配置
                colProps: {
                    span: 19    //设置动作所在区域，把搜索条放在右边
                },
                def: [{
                        name: '新增脚本',
                        icon: 'plus',
                        buttonProps: { type: 'primary' },
                        handler: () => {
                            this.to_create_new_script()
                        }
                    },
                ]
            },
            tableData:[],
            filter:{
                search:'',
                tag:'',
            },
            tag_list:[], //分类名称
        }
    },
    computed:{
        dataDict(){
            var dataDict = {}
            for (var n in this.tableData){
                var tag = this.tableData[n].tag
                if(dataDict.hasOwnProperty(tag)==false){
                    dataDict[tag] = []
                }
                dataDict[tag].push(this.tableData[n])
            }
            return dataDict
        }
    },
    methods:{
        get_script_list(){
              var self  = this
              this.$router.push({path:this.$route.path,query:this.filter})  //在查询api的时候,把当前页面的url也进行跳转,把参数都加到当前url上.
              this.$http.get(ToolScriptsApi,{params:self.filter}).then(function(response) {
                    self.tableData = response.data.result
              })
        },
        get_filter_params(){
            //获取url过滤的参数,方便返回到该页面时,直接能够找到之前的过滤条件
            this.filter.tag = this.$route.query.tag
            this.filter.search = this.$route.query.search
        },
        get_tag_list(){
        //获取分类列表
            var self = this
            this.$http.get(ToolScriptsTagsApi).then((response)=>{
                self.tag_list = response.data.result
            })
        },
        to_create_new_script(){
            this.$router.push( this.$route.path + '/create')
        },
        del_script(script_id){
              var self = this
              this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {
                self.$http.delete(ToolScriptsApi + '/' + script_id).then((response) => {
                  self.$message(response.data.msg)
                  if (response.data.status == 1) {
                    self.get_script_list()
                  }
                })
              }).catch(() => {})
        }
    },
    mounted(){
        this.get_filter_params()
        this.get_script_list()
        this.get_tag_list()
    }

}

</script>
