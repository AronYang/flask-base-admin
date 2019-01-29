<template>
    <div class="card">
        <div class="card-body">
            <el-col style="margin-top:15px">
                <el-row>
                    <!-- <el-button v-for="cluster in clusters">{{cluster.name}}</el-button> -->
                    选择环境：
                    <el-radio-group v-model="select_env" @change="select_env_method">
                        <el-radio-button :label="cluster.id" v-for="cluster in clusters">{{cluster.name}}</el-radio-button>
                    </el-radio-group>
                </el-row>
                <hr>
                <el-row style="margin-bottom:10px">
                    <el-button  @click="checksql"  :loading="checksqlloadingstatus">检测</el-button>
                    <el-button type="danger" @click="execute('force')" :loading="execsqlloadingstatus">执行</el-button>
                    <el-button  @click="showHistoryExecModal = 1" style="float:right">历史记录<span class="el-dropdown-link"><i class="el-icon-arrow-down el-icon--right"></i></span></el-button>
                </el-row>
                <el-row>
                    <el-table :data="SvnFileListData" tablePropsborder=1 :pagination-def="paginationDef" @selection-change="handleSqlExecSelectionChange">
                        <el-table-column type="selection" width="55" :selectable='checkbox_valid'>
                        </el-table-column>
                        <el-table-column sortable show-overflow-tooltip prop="file" label="文件名">
                            <template scope="scope">
                                <el-button type="text" size="small" @click="showsqlFileContent(scope.row.file,scope.row.svndirname);svnSqlFilename = scope.row.file">{{scope.row.file}}</el-button>
                            </template>
                        </el-table-column>
                        <el-table-column sortable prop="instance" label="对应实例">
                            <template scope="scope">
                                <!-- <span v-text="scope.row.instance_ip + '' + scope.row.instance_port"> -->
                                <div>
                                    <span>
                                {{scope.row.instance_ip}} {{scope.row.instance_port}}
                              </span>
                                    <span v-if="scope.row.instance_ip == null && scope.row.instance_port == null ">
                                <el-button type="text">选择实例</el-button>
<!--
                                    <el-dropdown size="small" split-button type="primary">
                                        选择实例
                                      <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item v-for="instance in instance_list" @click="scope.row.instance_ip = instance.ip;scope.row.instance_port = instance.port;" >  {{instance.ip}} {{instance.port}}  </el-dropdown-item>
                                      </el-dropdown-menu>
                                    </el-dropdown> -->
                                </span>
                                    <span v-if="scope.row.database == ''">
                                    <el-dropdown @command="handleCommand" >
                                      <span class="el-dropdown-link">
                                        <i class="el-icon-arrow-down el-icon--right"></i>
                                      </span>
                                    <el-dropdown-menu slot="dropdown">
                                        <el-dropdown-item v-for="instance in instance_list" :command="[instance,scope.row]"> {{instance.ip}} {{instance.port}}</el-dropdown-item>
                                    </el-dropdown-menu>
                                    </el-dropdown>
                                    <!--                                   <el-select v-model="select_instance_value"   clearable placeholder="请选择">
                                    <el-option
                                      v-for="instance in instance_list"
                                      :key="instance.id"
                                      :label="instance.ip + instance.port"
                                      :value="instance.id">
                                    </el-option>
                                  </el-select> -->
                                    </span>
                                </div>
                            </template>

                        </el-table-column>

                        <el-table-column sortable prop="type" label="SQL类型">
                            <template scope="scope">
                                <el-tag :type="scope.row.type_length>=2?'danger':'primary' ">{{scope.row.type}}</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column sortable prop="database" label="所属数据库">
                        </el-table-column>
                        <el-table-column sortable prop="date" label="最后提交时间">
                        </el-table-column>
                        <el-table-column sortable prop="author" label="提交人">
                        </el-table-column>
                        <!-- <el-table-column sortable prop="msg" label="提交信息"> -->
                        <!-- </el-table-column> -->
                        <el-table-column prop="id" label="操作">
                            <template scope="scope">
                                <!--                     <el-button type="text" size="small" @click="showsqlFileContent(scope.row.file);svnSqlFilename = scope.row.file">查看</el-button> -->
                                <!-- <el-button type="text" size="small">历史</el-button> -->
                                <el-button type="text" size="small" @click="showHistoryVersion=true;getHistoryVersion(scope.row)">历史版本</el-button>

                                <!-- <el-button type="text" size="small" @click="showModalexec=true">执行</el-button> -->
                            </template>
                        </el-table-column>
                    </el-table>
                    <!-- 查看sql文件内容的详情。  -->
                    <el-dialog :title="'文件内容：' + svnSqlFilename" :visible.sync="showModalSvnSqlContent" width="70%">
                        <span>
                <div v-if="svnSqlContent !=  ''">
                  <codemirror v-model="svnSqlContent" :options="editorOption"></codemirror>
                </div>
                <div v-if="showSqlContent ==  1">
                  <codemirror v-model="ruleForm.sqlContent" :options="editorOption"></codemirror>
                </div>
              </span>
                        <span slot="footer" class="dialog-footer">
                    <el-button @click="showModalSvnSqlContent = false ">关闭</el-button>
                </span>
                    </el-dialog>



                    <!-- 执行单个SQL页面的modal。  -->
                    <!--                     <el-dialog :title="'文件内容：'" :visible.sync="showModalexec" width="70%">
                        <span>

                    <div class="text-muted">要检查和执行的环境：</div>
                    <el-select v-model="cluster_id" filterable placeholder="请选择环境" style="width:100%;margin-bottom:15px" @change="get_env_instances">
                      <el-option v-for="cluster in clusters" :key="cluster.id" :label="cluster.name" :value="cluster.id">
                      </el-option>
                    </el-select>


                    <div class="text-muted">要检查和执行的实例：</div>
                    <el-select v-model="instance_id" filterable placeholder="请选择实例" style="width:100%;margin-bottom:15px" @change="singe_exec_instance_set" >
                      <el-option v-for="instance in instance_list" :key="instance.id" :label="instance.ip + ':' + instance.port" :value="instance.id">
                      </el-option>
                    </el-select>

                    <el-row style="margin-top:20px">
                      <div class="text-muted">操作命令：</div>
                      <el-tooltip class="item" effect="dark" content="不会真正执行，基于inception检测" placement="top">
                        <el-button type="default" @click="checksql" :loading="check_loading_status" :disabled="cluster_id == ''">检测</el-button>
                      </el-tooltip>


                      <el-tooltip class="item" effect="dark" content="执行遇到错误时，接着执行后续的sql" placement="top">
                        <el-button type="danger" @click="execute('force')" :loading="force_loading_status" :disabled="cluster_id == ''">强制执行</el-button>
                      </el-tooltip>
                    </el-row>

                    </span>
                        <span slot="footer" class="dialog-footer">
                       <el-button @click="showModalexec = false ">关闭</el-button>
                    </span>
                    </el-dialog> -->




                    <!-- 批量执行页面的modal。  -->
                    <!--                   <el-dialog :title="'文件内容：'" :visible.sync="showModalBatchExecStatus" width="70%">
                        <span>
                    <div class="text-muted">要检查和执行的环境：</div>
                    <el-select v-model="cluster_id" filterable placeholder="请选择环境" style="width:100%;margin-bottom:15px" @change="get_env_instances">
                      <el-option v-for="cluster in clusters" :key="cluster.id" :label="cluster.name" :value="cluster.id">
                      </el-option>
                    </el-select>
                    <el-row>
                      <div class="text-muted">执行关系：</div>
                      <table class="table  table-bordered  table-condensed">
                        <tbody>
                          <tr style="background-color:rgb(238,241,246)">
                            <td>实例</td>
                            <td>SQL</td>
                          </tr>
                        </tbody>
                        <tr v-for="instance in instance_list">
                            <td>
                                <el-tooltip class="item" effect="dark" :content="'该实例包含库：'+instance.dbNames" placement="top">
                                            <span>{{instance.ip}}:{{instance.port}}</span>
                        </el-tooltip>
                        </td>
                        <td>
                            <span v-for="sql in instance.sqlFileList">
                                            {{sql.filename}} &nbsp &nbsp
                                        </span>
                        </td>
                        </tr>
                        </table>
                </el-row>
                <el-row>
                    <div class="text-muted">执行次序：</div>
                    <span v-for="(sql,index) in SqlExecSelectionVals">

                          <span style="color:red">{{index + 1}}</span> .&nbsp
                    <el-tooltip class="item" effect="dark" content="该文件未找到对应实例！" placement="top">
                        <span style="color:red" v-if="found_db_sqlfiles.indexOf(sql.file)==-1">{{sql.file}}</span>
                    </el-tooltip>
                    <span v-if="found_db_sqlfiles.indexOf(sql.file)!=-1">{{sql.file}}</span> &nbsp&nbsp
                    </span>
                </el-row>
                <el-row style="margin-top:20px">
                    <div class="text-muted">操作命令：</div>
                    <el-tooltip class="item" effect="dark" content="不会真正执行，基于inception检测" placement="top">
                        <el-button type="default" @click="checksql" :loading="check_loading_status" :disabled="cluster_id == ''">检测</el-button>
                    </el-tooltip>
                    <el-tooltip class="item" effect="dark" content="执行遇到错误时，接着执行后续的sql" placement="top">
                        <el-button type="danger" @click="execute('force')" :loading="force_loading_status" :disabled="cluster_id == ''">强制执行</el-button>
                    </el-tooltip>
                </el-row>
                </span>
                <span slot="footer" class="dialog-footer">
                       <el-button @click="showModalBatchExecStatus = false ">关闭</el-button>
                </span>
                </el-dialog> -->

                    <!-- 显示历史版本信息的modal。  -->
                    <el-dialog :title="'历史版本：'" :visible.sync="showHistoryVersion" width="70%">
                        <div v-for="history in FileHistoryVersionList">
                            {{history.revision}}--{{history.author}}---{{history.date}}---{{history.msg}}
                        </div>

                        <span slot="footer" class="dialog-footer">
                                <el-button @click="showHistoryVersion = false ">关闭</el-button>
                        </span>

                    </el-dialog>



                </el-row>

            </el-col>

            <el-col>
                <template>
                    <el-tabs v-model="execute_tab" type="card" style="margin-top:15px">
                        <el-tab-pane label="检查结果" name="check">
                            <el-col style="margin-top:15px">
                                <div class="text-muted">SQL检查结果：
                                    <el-button type="text" @click="checkTables = []">清空</el-button>
                                </div>
                                <div style="margin-left:15px">
                                    <template v-for="check in checkTables">
                                        <h6 style="margin-top:15px">{{check.instance}}:{{check.filename}}</h6>
                                        <div v-if="check.status == 0 " class="text-danger">{{check.data}}</div>
                                        <el-table :data="check.data" v-if="check.data != '' && check.status == 1">
                                            <el-table-column prop="SQL" label="SQL" sortable show-overflow-tooltip>
                                            </el-table-column>
                                            <el-table-column sortable prop="execute_time" label="执行时间" width="120">
                                            </el-table-column>
                                            <el-table-column sortable prop="Affected_rows" label="影响行数" width="120">
                                            </el-table-column>
                                            <el-table-column sortable prop="errlevel" label="错误" width="100">
                                                <template scope="scope">
                                                    <el-tag type="warning" v-if="scope.row.errlevel==1">警告</el-tag>
                                                    <el-tag type="danger" v-if="scope.row.errlevel==2">严重</el-tag>
                                                    <el-tag type="success" v-if="scope.row.errlevel==0">正常</el-tag>
                                                </template>
                                            </el-table-column>
                                            <el-table-column sortable prop="errormessage" label="信息" show-overflow-tooltip>
                                            </el-table-column>
                                        </el-table>
                                    </template>
                                </div>
                            </el-col>
                        </el-tab-pane>
                        <el-tab-pane label="执行结果" name="execute">
                            <el-col style="margin-top:15px">
                                <!-- <div class="text-muted">SQL执行结果：</div> -->
                                <div style="margin-left:15px">
                                    <template v-for="(table_v,table_k) in execTableDicts">
                                        <br>
                                        <div><strong>{{table_k}}:</strong></div>
                                        <el-table :data="table_v">
                                            <el-table-column prop="SQL" label="SQL" sortable>
                                                <template scope="scope">
                                                    <el-tooltip class="item" effect="dark" :content="scope.row.SQL" placement="top-start">
                                                        <div style="max-height:50px;overflow:hidden" v-text="scope.row.SQL">
                                                        </div>
                                                    </el-tooltip>
                                                </template>
                                            </el-table-column>
                                            <el-table-column sortable prop="execute_time" label="执行时间" width="150">
                                            </el-table-column>
                                            <el-table-column sortable prop="Affected_rows" label="影响行数" width="150">
                                            </el-table-column>
                                            <el-table-column sortable prop="errlevel" label="状态" width="100">
                                                <template scope="scope">
                                                    <el-tag type="warning" v-if="scope.row.errlevel==1">警告</el-tag>
                                                    <el-tag type="danger" v-if="scope.row.errlevel==2">失败</el-tag>
                                                    <el-tag type="success" v-if="scope.row.errlevel==0">成功</el-tag>
                                                </template>
                                            </el-table-column>
                                            <el-table-column sortable prop="errormessage" label="信息">
                                                <template scope="scope">
                                                    <el-tooltip class="item" effect="dark" :content="scope.row.errormessage" placement="top-start">
                                                        <div style="max-height:50px;overflow:hidden" v-text="scope.row.errormessage">
                                                        </div>
                                                    </el-tooltip>
                                                </template>
                                            </el-table-column>
                                        </el-table>
                                    </template>
                                </div>
                            </el-col>
                        </el-tab-pane>
                    </el-tabs>
                </template>
            </el-col>
        </div>
            <el-dialog :title="'历史记录：'" :visible.sync="showHistoryExecModal" width="100%">
                <el-col style="margin-top:15px;">
                    <data-tables :data="execHistory">
                        <el-table-column width="180" prop="clusterName" label="集群名称" sortable>
                        </el-table-column>
                        <el-table-column prop="exec_filename" label="执行的文件" sortable>
                        </el-table-column>
                        <el-table-column width="180" prop="create_time" label="执行时间" sortable>
                        </el-table-column>
                        <el-table-column width="120" prop="userName" label="执行人" sortable>
                        </el-table-column>
                        <el-table-column width="120" prop="userName" label="查看" sortable>
                            <template scope="scope">
                                <a href="javascript:;" @click="record_id=scope.row.record_id;execute_tab='execute';get_exec_info(scope.row.record_id)">查看</a> </template>
                        </el-table-column>
                    </data-tables>
                </el-col>
                  <span slot="footer" class="dialog-footer">
                    <el-button @click="showHistoryExecModal = false">关闭</el-button>
                  </span>
            </el-dialog>

    </div>


    </div>




    <!-- </div> -->
</template>
<script>
    import { FlowListApiUrl, ConfirmActionApiUrl, ConfirmListApiUrl, ConfirmExecApiUrl, ConfirmListPage, ConfirmGetSvnSqlContent, InstanceListApiUrl, ConfirmCheckApiUrl } from '@/http/url'
    import { ConfirmSvnSqlListApiUrl, ConfirmGetClusterApiUrl, ConfirmGetExecHistoryApiUrl, ConfirmGetSqlFileHistoryVersionApiUrl } from '@/http/url'
    export default {
        name: 'confirmUpdate',
        data() {
            return {
                SvnFileListData: [],
                clusters: [],
                execute_tab: 'execute',
                props: {
                    value: 'id',
                    children: 'dbs',
                    label: 'name',
                },
                form: {},
                cluster_id: '', //选中的集群
                instance_id: '', //选中的实例
                dbs: [],
                ruleForm: {
                    name: '',
                },
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
                showSqlContent: 0, //控制sql内容是否显示
                // execTable: [], //存放拉出来的命令执行结果的数据
                checkTables: [], // 存放sql语法检测的结果
                execute_loading_status: false,
                check_loading_status: false,
                force_loading_status: false,
                record_id: '',
                sqlFileList: [], //选中的要执行的sql文件,文件里是字典
                svnSqlContent: '', //查看从svn里拉出来的文件内容
                svnSqlFilename: '', //当前选中的文件名称
                instance_list: [], //环境下的实例列表.
                exced_file_in_cluster: [], //已执行过的文件放入这个里面
                found_db_sqlfiles: [], //已找到的数据库文件放在这个列表里,用来判断有些文件没有找到对应数据库
                // actionsDef: { //表格按钮配置
                //     colProps: {
                //         span: 19
                //     },
                //     def: [
                //         {
                //             name: '检测',
                //             buttonProps: { type: 'primary' },
                //             handler: () => {

                //                 this.checksql()
                //                 // this.showModalBatchExecStatus = true
                //                 // this.auto_relation_cluster_and_sqlfile()
                //             }
                //         },
                //         {
                //             name: '执行',
                //             buttonProps: { type: 'danger' },
                //             handler: () => {

                //                 this.execute('force')
                //                 // this.showModalBatchExecStatus = true
                //                 // this.auto_relation_cluster_and_sqlfile()
                //             }
                //         },


                //     ]
                // },
                showModalSvnSqlContent: false, //查看文件详情的modal
                // showModalexec: false, //单个执行modal显示控制
                // showModalBatchExecStatus: false, //批量执行modal显示控制
                paginationDef: {
                    show: false
                }, // 表格分页设置,关闭分页功能
                SqlExecSelectionVals: [], //sql文件选择
                execTableDicts: {}, //当前拉取的执行结果
                execHistory: [], //历史执行记录条目，
                showHistoryVersion: false, //查看历史版本modal的关开
                FileHistoryVersionList: [], //历史版本信息存放在这个列表里
                select_env: '', //当前环境选择的ID
                showHistoryExecModal: false, //查看历史执行记录
                checksqlloadingstatus:false,
                execsqlloadingstatus:false,
            }
        },
        methods: {
            get_exec_info(value) {
                // 获取执行结果, 每隔几秒种循环获取.
                var self = this
                var record_id = this.record_id
                if (value != record_id) {
                    return
                }
                // this.execTable = []
                this.$http.get(ConfirmExecApiUrl + '?record_id=' + record_id).then((response) => {
                    if (response.data.status == 1) {
                        self.execTableDicts = response.data.result
                        console.log(self.execTableDicts, 'exec table dicts')
                    }
                    var circle_tag = 1
                    //如果不是在审核页面了，不再循不
                    if (self.$route.path.indexOf('/sqlaudit/confirms/') == -1) {
                        cicle_tag = 0
                    }
                    //如果循环标记为1，则循环拉取执行记录
                    if (circle_tag == 1) {
                        console.log('circle...', self.execTableDicts)
                        setTimeout(function() {
                            self.get_exec_info(value)
                        }, 2000)
                    }
                })
            },
            checksql() {
                //检测sql语法
                if (this.SqlExecSelectionVals.length == 0) {
                    this.$message.error("未选择要检测的sql!")
                    return
                }
                this.checksqlloadingstatus= true

                var submit_id = this.$route.params.id
                var self = this
                this.execute_tab = 'check'
                this.checkTables = []
                this.check_loading_status = true
                //如果是svntag=1,把svn里的文件提上去
                var d = {
                    cluster_id: this.cluster_id,
                    submit_id: submit_id,
                    // instance_list: this.instance_list,
                    SqlExecSelectionVals: this.SqlExecSelectionVals,
                }
                this.$http.put(ConfirmCheckApiUrl, d).then((response) => {
                    self.$message(response.data.msg)
                    self.check_loading_status = false
                    self.checkTables = response.data.result
                    console.log(self.checkTables)
                    this.checksqlloadingstatus = false
                })
            },
            execute(action) {
                //执行命令, action包含check, execute
                var submit_id = this.$route.params.id
                if (this.SqlExecSelectionVals.length == 0) {
                    this.$message.error("未选择要执行的sql!")
                    return
                }

                this.execsqlloadingstatus = true
                var self = this
                // 判断该环境是否执行过
                if (action == 'execute' || action == 'force') {
                    var data = {
                        cluster_id: this.cluster_id,
                        submit_id: submit_id,
                        action: action,
                        instance_list: this.instance_list,
                        SqlExecSelectionVals: this.SqlExecSelectionVals,
                    }
                    var already_exec_files = []
                    for (var i in this.instance_list) {
                        for (var n in this.instance_list[i].sqlFileList) {
                            var will_exec_file = this.instance_list[i].sqlFileList[n]
                            for (var n2 in this.ruleForm.passrecords) {
                                var already_exec_filenames = this.ruleForm.passrecords[n2].exec_filenames
                                if (already_exec_filenames.indexOf(will_exec_file) != -1) {
                                    if (already_exec_files.indexOf(will_exec_file) == -1) {
                                        already_exec_files.push(will_exec_file)
                                    }
                                }
                            }
                        }
                    }
                    if (already_exec_files != '') {
                        this.$confirm(already_exec_files.join(', ') + '文件在该环境已经执行过, 是否继续?', '提示', {
                            confirmButtonText: '确定',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }).then(() => {
                            self.execSqlCmd(action, data)
                        }).catch(() => {
                            // self.force_loading_status = false
                            self.execsqlloadingstatus = false
                            return
                        });
                    } else {
                        self.execSqlCmd(action, data)
                    }
                }
            },
            execSqlCmd(action, data) {
                var self = this
                this.execute_tab = 'execute'
                this.execTableDicts = {}
                if (action == 'execute') { self.execute_loading_status = true } //button置为加载中
                if (action == 'force') { self.force_loading_status = true } //button置为加载中
                self.$http.put(ConfirmExecApiUrl, data).then((response) => {
                    self.$message(response.data.msg)
                    // self.execute_loading_status = false
                    if (action == 'execute') { self.execute_loading_status = false } //button置为加载中
                    if (action == 'force') { self.force_loading_status = false } //button置为加载中
                    if (response.data.status == 1) {
                        if (action == 'execute' || action == 'force') {
                            // self.execute_loading_status = false //button置为正常状态
                            self.record_id = response.data.result.record_id
                            console.log(response.data.result, 'record id...')
                            // self.get_confirm_info() //重新获取工单数据
                            self.get_the_cluster_exists_file()
                            self.get_exec_info(self.record_id) //循环获取数据
                            self.execsqlloadingstatus = false
                        }
                    }
                })
            },
            showsqlFileContent(filename, svndirname) {
                //查看单个sql文件状态
                var submit_id = this.$route.params.id
                this.showModalSvnSqlContent = true
                var self = this
                var d = {
                    svndirname: svndirname,
                    filename: filename,
                }
                self.svnSqlContent = ''
                self.$http.get(ConfirmGetSvnSqlContent, { params: d }).then((response) => {
                    console.log(response.data.result)
                    self.svnSqlContent = response.data.result
                })
            },
            get_env_instances() {
                //环境值变后，获取该环境下的实例列表。
                var self = this
                this.get_the_cluster_exists_file()
                self.$http.get(InstanceListApiUrl, { params: { cluster_id: this.cluster_id } }).then((response) => {
                    for (var n in response.data.result) {
                        response.data.result[n].sqlFileList = []
                    }
                    self.instance_list = response.data.result
                    self.auto_relation_cluster_and_sqlfile()
                })
            },
            get_the_cluster_exists_file() {
                // 获取集群中已经执行过的文件列表
                var exced_file_in_cluster = []
                var cluster_id = this.cluster_id
                for (var n in this.ruleForm.passrecords) {
                    var exec = this.ruleForm.passrecords[n]
                    if (exec.cluster_id == cluster_id) {
                        for (var m in exec.exec_filenames) {
                            var exec_file = exec.exec_filenames[m]
                            if (exced_file_in_cluster.indexOf(exec_file) == -1) {
                                exced_file_in_cluster.push(exec_file)
                            }
                        }
                    }
                }
                this.exced_file_in_cluster = exced_file_in_cluster
            },
            auto_relation_cluster_and_sqlfile() {
                // 自动把环境下的实例上sql文件关联起来
                if (this.ruleForm.svntag != 1) {
                    this.ruleForm.svnfilelist = [this.ruleForm.dbname, ]
                    this.sqlFileList = [this.ruleForm.dbname, ]
                    console.log('svntag != 1')
                }
                this.found_db_sqlfiles = [] //已找到数据库的文件放到这里面。
                for (var n in this.instance_list) {
                    this.instance_list[n].sqlFileList = []
                    var instance = this.instance_list[n]
                    for (var m in instance.dbs) {
                        var dbname = instance.dbs[m]
                        for (var i in this.SqlExecSelectionVals) {
                            var select_sql_file = this.SqlExecSelectionVals[i].file
                            var select_database = this.SqlExecSelectionVals[i].database
                            if (select_database == dbname) {
                                var d = {
                                    database: select_database,
                                    filename: select_sql_file,
                                }
                                // this.instance_list[n].sqlFileList.push(select_sql_file)
                                this.found_db_sqlfiles.push(select_sql_file)
                                this.instance_list[n].sqlFileList.push(d)
                                // this.found_db_sqlfiles.push(d)
                            }
                        }
                    }
                }
            },
            select_env_then_relation_instance() {
                // 自动把环境下的实例上sql文件关联起来
                if (this.ruleForm.svntag != 1) {
                    this.ruleForm.svnfilelist = [this.ruleForm.dbname, ]
                    this.sqlFileList = [this.ruleForm.dbname, ]
                    console.log('svntag != 1')
                }
                this.found_db_sqlfiles = [] //已找到数据库的文件放到这里面。
                for (var n in this.instance_list) {
                    // this.instance_list[n].sqlFileList = []
                    var instance = this.instance_list[n]
                    for (var m in instance.dbs) {
                        var dbname = instance.dbs[m]
                        for (var i in this.SvnFileListData) {
                            var select_sql_file = this.SvnFileListData[i].file
                            if (this.SvnFileListData[i].database == dbname) {
                                this.SvnFileListData[i].instance_ip = instance.ip
                                this.SvnFileListData[i].instance_port = instance.port
                                this.SvnFileListData[i].instance_id = instance.id

                                console.log(dbname, instance.ip, instance.port)
                            }
                        }
                    }
                }
                // this.SvnFileListData = Object.assign({}, this.SvnFileListData)
                this.$set(this.SvnFileListData)
            },
            checkbox_valid(row, index) {
                //返回sql列表,是否可以选择, 如果type_length>=2,则不可以选择.
                if (row.instance_ip == undefined) {
                    return false
                } else {
                    return true
                }
            },
            getExecHistory() {
                var id = this.$route.params.id
                var self = this
                var url = ConfirmGetExecHistoryApiUrl + id
                this.$http.get(url).then((response) => {
                    self.execHistory = response.data.result
                    console.log('history...', self.execHistory)
                })
            },
            handleSqlExecSelectionChange(val) {
                //选择sql文件列表
                this.SqlExecSelectionVals = val
            },

            get_sql_file_list() {
                //获取svn下的sql文件列表
                var id = this.$route.params.id
                var self = this
                console.log(this.$route.params, '2222222222')
                this.$http.get(ConfirmSvnSqlListApiUrl + id).then((response) => {
                    console.log(response)
                    self.SvnFileListData = response.data.result

                })
            },
            get_clusters() {
                //获取当前用户在当前工单下能够拥有的集群节点权限
                var id = this.$route.params.id
                var self = this
                this.$http.get(ConfirmGetClusterApiUrl + id).then((response) => {
                    self.clusters = response.data.result
                })
            },
            getHistoryVersion(row) {
                var data = {
                    file: row.file,
                    svndirname: row.svndirname,
                }
                this.FileHistoryVersionList = []
                var self = this
                this.$http.get(ConfirmGetSqlFileHistoryVersionApiUrl, { params: data }).then((response) => {
                    if (response.data.status == 0) {
                        self.FileHistoryVersionList = response.data.result
                    } else {
                        self.$message.error(response.data.msg)
                    }

                    console.log(response.data.result, 'history version...')
                })
            },
            select_env_method(value) {
                //选中环境后，执行的函数。
                console.log('value....', value)
                this.cluster_id = value
                var self = this
                this.get_the_cluster_exists_file()
                self.$http.get(InstanceListApiUrl, { params: { cluster_id: this.cluster_id } }).then((response) => {
                    for (var n in response.data.result) {
                        response.data.result[n].sqlFileList = []
                    }
                    self.instance_list = response.data.result
                    self.select_env_then_relation_instance()
                })
            },
            handleCommand(value) {
                console.log(value)
                console.log(this.SvnFileListData)
                var instance = value[0]
                var row = value[1]
                for (var n in this.SvnFileListData) {
                    if (this.SvnFileListData[n] == undefined) { continue }
                    var svn_file = this.SvnFileListData[n].file
                    if (svn_file == row.file) {
                        console.log('11111111111111')
                        // this.SvnFileListData[n].instance_ip = instance.ip
                        // this.SvnFileListData[n].instance_port = instance.port
                        // this.SvnFileListData[n].handle_relation = 1

                        row.instance_ip = instance.ip
                        row.instance_port = instance.port
                        row.instance_id = instance.id
                        row.handle_relation = 1
                        console.log(this.SvnFileListData)
                        this.$set(row)
                    }
                }
                this.$set(this.SvnFileListData)
            }
        },
        mounted() {
            this.get_sql_file_list()
            this.get_clusters()
            this.getExecHistory()
        }
    }

</script>
