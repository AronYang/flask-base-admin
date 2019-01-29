<template>
  <div class="card">
    <div class="card-body">
      <el-row style="margin-bottom:15px">
        <el-select v-model="query.dubbo_id" @change.passive="get_router_list">
          <el-option v-for="config in config_list" :label="config.name" :key="config.id" :value="config.id">{{config.name}}</el-option>
        </el-select>
        <el-input v-model="query.name" @keyup.enter.native="get_router_list" placeholder="搜索路由名称或服务名称" style="width:200px"></el-input>
        <el-button @click="get_router_list" icon="el-icon-search" type="primary">搜索</el-button>
        <el-button type="primary" @click="show_create_modal=true;$refs['routerForm'].resetFields();clear_form_value()">_新增</el-button>
        <el-tooltip class="item" effect="dark" content="查看路由操作日志" placement="top-start">
          <el-button type="warning" style="float: right" @click="show_router_log" icon="el-icon-tickets" circle></el-button>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="同步当前集群的所有路由规则，大概需要几十秒时间" placement="top-start">
          <el-button type="primary" style="float: right" @click="sync_routers_by_zk" :loading="sync_loading_status" icon="el-icon-refresh" circle></el-button>
        </el-tooltip>
      </el-row>
      <data-tables :data="router_list" :table-props="tableProps">
        <el-table-column sortable prop="name" align="center" label="路由名称" show-overflow-tooltip>
          <template slot-scope='scope'>
            {{scope.row.name}}
          </template>
        </el-table-column>
        <el-table-column sortable align="center" prop="path" label="服务名" show-overflow-tooltip />
        <!-- <el-table-column sortable align="center"  prop="priority" label="优先级" width="100" /> -->
        <el-table-column sortable align="center" prop="enabled" label="状态" width="100">
          <template slot-scope='scope'>
            <el-tooltip class="item" effect="dark" content="点击可快速启用或禁用" placement="top-start">
              <el-button size="mini" type="success" v-if="scope.row.enabled=='true'" @click="toggle_router_enable(scope.row)">已启用</el-button>
              <el-button size="mini" type="danger" v-if="scope.row.enabled=='false'" @click="toggle_router_enable(scope.row)">已禁用</el-button>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column sortable align="center" prop="update_time" label="更新时间" width="150" show-overflow-tooltip>
        </el-table-column>
        <el-table-column sortable align="center" prop="action" label="动作" width="100">
          <template slot-scope='scope'>
            <div v-if="scope.row.action == 'filter'">过滤</div>
            <div v-if="scope.row.action == 'deny'">拒绝</div>
          </template>
        </el-table-column>
        <el-table-column prop="id" align="center" label="操作" width="120">
          <template slot-scope="scope">
            <el-button icon="el-icon-edit" circle size="small" @click="show_edit_modal=true;get_router_info(scope.row.id);">
            </el-button>
            </router-link>
            <el-button type="danger" icon="el-icon-delete" circle size="small" @click="del_router(scope.row.id)"></el-button>
          </template>
        </el-table-column>
      </data-tables>
      <el-dialog title="路由编辑" class="dialog-center" :visible.sync="show_edit_modal" width="65%" top="0%" fullscreen close-on-press-escape close-on-click-modal>
        <el-row>
          <el-col :span="9">
            <div id="chart_edit" style="width:100%;height:500px">
            </div>
          </el-col>
          <el-col :span="15">
            <el-form ref="editform" label-width="150px" :model="routerForm" :rules="rules">
              <el-form-item label="名称：" prop="name">
                <el-input v-model="routerForm.name"></el-input>
              </el-form-item>
              <el-form-item label="状态：" prop="enabled">
                <el-radio v-model="routerForm.enabled" label="true">启用</el-radio>
                <el-radio v-model="routerForm.enabled" label="false">禁用</el-radio>
              </el-form-item>
              <el-form-item label="服务名：" prop="path">
                {{routerForm.path}}
              </el-form-item>
              <hr />
              <el-form-item label="匹配消费者：" prop="rules">
                <el-row :gutter="15" v-if="routerForm.rules==''" style="color:gray">没有匹配规则</el-row>
                <template v-for="rule,index in routerForm.rules">
                  <el-row style="margin-bottom:5px;">
                    <el-col :span="5" style="padding-left:7.5px">
                      <span v-if="rule.name == 'consumer.host'">消费者IP</span>
                      <span v-if="rule.name == 'consumer.application'">消费者应用</span>
                      <span v-if="rule.name == 'consumer.cluster'">消费者集群</span>
                    </el-col>
                    <el-col :span="3" >
                      {{rule.ex}}
                    </el-col>
                    <el-col :span="12" >
                      {{rule.value}}
                    </el-col>
                    <el-col :span="3"  style="padding-left:18px">
                      <el-button icon="el-icon-minus" @click="routerForm.rules.splice(index,1)"></el-button>
                    </el-col>
                  </el-row>
                </template>
              </el-form-item>
              <el-form-item label="  ">
                <el-row :gutter="15">
                  <el-col :span="5">
                    <el-select v-model="routerRuleData.name" placeholder="来源IP或应用">
                      <el-option value="consumer.host" label="消费者IP">消费者IP</el-option>
                      <el-option value="consumer.application" label="消费者应用">消费者应用</el-option>
                      <el-option value="consumer.cluster" label="消费者集群">消费者集群</el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="3">
                    <el-select v-model="routerRuleData.ex" placeholder="匹配">
                      <el-option value="=">=</el-option>
                      <el-option value="!=">!=</el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="12">
                    <el-tooltip placement="top">
                      <div slot="content">
                        <div>访问该服务的消费者IP有：<span v-for="c in nearinfo.consumer">{{c}},&nbsp</span></div>
                        <div>访问该服务的应用有：<span v-for="c in nearinfo.application">{{c}},&nbsp</span></div>
                        <div>访问该服务的集群有：<span v-for="c in nearinfo.cluster">{{c}},&nbsp</span></div>
                      </div>
                      <el-input v-model="routerRuleData.value" placeholder="输入匹配的内容，以逗号分隔"></el-input>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="3" >
                    <el-button icon="el-icon-plus" @click="addRules"></el-button>
                  </el-col>
                </el-row>
              </el-form-item>
              <hr />
              <el-form-item label="动作：" prop="action">
                <el-row :gutter="15">
                  <el-col :span="5">
                    <el-select v-model="routerForm.action">
                      <el-option value="deny" label="拒绝">拒绝(没在规则中的来源将都会被允许)</el-option>
                      <el-option value="filter" label="过滤">过滤提供者(满足条件的提供者将能被消费者访问)</el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="3">
                    <el-tooltip placement="top" effect="light">
                      <div slot="content">
                        <p>
                          1. 默认允许所有消费者访问<br />
                          2. 当某个消费者同时匹配黑名单和白名单时，优先白名单 <br />
                          3. 一个服务只能有一条白名单规则，否则两条规则交叉，就都被筛选掉了 <br />
                          4. 支持乏匹配，如:172.20.10.*
                        </p>
                      </div>
                      <i class="el-icon-question"></i>
                    </el-tooltip>
                  </el-col>
                </el-row>
                <el-row>
                </el-row>
              </el-form-item>
              <el-form-item label="过滤提供者：" prop="filters" v-if="routerForm.action=='filter'">
                <el-row v-if="routerForm.filters==''" style="color:gray">没有过滤规则</el-row>
                <template v-for="filter,index in routerForm.filters">
                  <el-row  style="margin-bottom:5px;">
                    <el-col :span="5" style="padding-left:7.5px;">
                      <span v-if="filter.name == 'provider.host'">提供者IP</span>
                      <span v-if="filter.name == 'provider.cluster'">提供者集群</span>
                      <span v-if="filter.name == 'provider.protocol'">提供者协议</span>
                      <span v-if="filter.name == 'provider.port'">提供者端口</span>
                    </el-col>
                    <el-col :span="3">
                      {{filter.ex}}
                    </el-col>
                    <el-col :span="12">
                      {{filter.value}}
                    </el-col>
                    <el-col :span="3" style="padding-left:18px">
                      <el-button icon="el-icon-minus" @click="routerForm.filters.splice(index,1)"></el-button>
                    </el-col>
                  </el-row>
                </template>
              </el-form-item>
              <el-form-item label=" " v-if="routerForm.action=='filter'">
                <el-row :gutter="15">
                  <el-col :span="5">
                    <el-select v-model="routerFilterData.name" placeholder="提供者过滤配置">
                      <el-option value="provider.host" label="提供者IP">提供者IP</el-option>
                      <el-option value="provider.cluster" label="提供者集群">提供者集群</el-option>
                      <el-option value="provider.protocol" label="提供者协议">提供者协议</el-option>
                      <el-option value="provider.port" label="提供者端口">提供者端口</el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="3">
                    <el-select v-model="routerFilterData.ex" placeholder="匹配">
                      <el-option value="=">=</el-option>
                      <el-option value="!=">!=</el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="12">
                    <el-tooltip placement="top">
                      <div slot="content">
                        <div>该服务的提供者有：<span v-for="c in nearinfo.provider">{{c}},&nbsp</span></div>

                      </div>
                      <el-input v-model="routerFilterData.value" placeholder="输入匹配的内容，以逗号分隔"></el-input>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="3">
                    <el-button icon="el-icon-plus" @click="addFilters"></el-button>
                  </el-col>
                </el-row>
              </el-form-item>
              <el-form-item>
                <el-button style="float:right;margin-left:10px;" type="primary" @click="save_edit_form('editform')">提交</el-button>
                <el-button style="float:right" @click="show_edit_modal = false">关闭</el-button>
              </el-form-item>
            </el-form>
            <!--         <span slot="footer" class="dialog-footer">
            <el-button @click="show_edit_modal = false">关闭</el-button>
            <el-button type="primary" @click="save_edit_form('editform')">提交</el-button>
        </span>
 -->
          </el-col>
        </el-row>
      </el-dialog>
      <el-dialog title="路由新增" class="dialog-center" :visible.sync="show_create_modal" width="65%" top="0%" fullscreen close-on-press-escape close-on-click-modal>
        <el-row>
          <el-col :span="9">
            <div id="chart_create" style="width:100%;height:500px;text-align:center;vertical-align: middle;">
              <br>
              <br>
              <br>
              <el-tag type="warning">
                <h4>请先选择服务名以渲染图表!<br>

                  </h4>
              </el-tag>
            </div>
          </el-col>
          <el-col :span="15">
            <el-form ref="routerForm" label-width="100px" :model="routerForm" :rules="rules">
              <el-form-item label="名称：" prop="name">
                <el-input v-model="routerForm.name"></el-input>
              </el-form-item>
              <el-form-item label="是否生效：" prop="enabled">
                <el-radio v-model="routerForm.enabled" label="true">启用</el-radio>
                <el-radio v-model="routerForm.enabled" label="false">禁用</el-radio>
              </el-form-item>
              <el-form-item label="服务名：" prop="path">
                <el-autocomplete v-model="routerForm.path" value-key="name" :fetch-suggestions="querySearch" placeholder="请输入服务名" style="width:100%" @select="get_node_info"></el-autocomplete>
              </el-form-item>
              <hr />
              <el-form-item label="匹配消费者：" prop="rules">
                <el-row v-if="routerForm.rules==''" style="color:gray">没有匹配规则</el-row>
                <template v-for="rule,index in routerForm.rules">
                  <el-row :gutter="15" style="margin-bottom:5px;">
                    <el-col :span="5" style="padding-left:7.5px;">
                      <span v-if="rule.name == 'consumer.host'">消费者IP</span>
                      <span v-if="rule.name == 'consumer.application'">消费者应用</span>
                      <span v-if="rule.name == 'consumer.cluster'">消费者集群</span>
                    </el-col>
                    <el-col :span="3">
                      {{rule.ex}}
                    </el-col>
                    <el-col :span="12">
                      {{rule.value}}
                    </el-col>
                    <el-col :span="3"  style="padding-left:18px">
                      <el-button icon="el-icon-minus" @click="routerForm.rules.splice(index,1)"></el-button>
                    </el-col>
                  </el-row>
                </template>
              </el-form-item>
              <el-form-item label="  ">
                <el-row :gutter="15">
                  <el-col :span="5">
                    <el-select v-model="routerRuleData.name" placeholder="来源IP或应用">
                      <el-option value="consumer.host" label="消费者IP">消费者IP</el-option>
                      <el-option value="consumer.application" label="消费者应用">消费者应用</el-option>
                      <el-option value="consumer.cluster" label="消费者集群">消费者集群</el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="3">
                    <el-select v-model="routerRuleData.ex" placeholder="匹配">
                      <el-option value="=">=</el-option>
                      <el-option value="!=">!=</el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="12">
                    <el-tooltip placement="top">
                      <div slot="content">
                        <div>访问该服务的消费者IP有：<span v-for="c in nearinfo.consumer">{{c}},&nbsp</span></div>
                        <div>访问该服务的应用有：<span v-for="c in nearinfo.application">{{c}},&nbsp</span></div>
                        <div>访问该服务的集群有：<span v-for="c in nearinfo.cluster">{{c}},&nbsp</span></div>
                      </div>
                      <el-input v-model="routerRuleData.value" placeholder="输入匹配的内容，以逗号分隔"></el-input>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="3">
                    <el-button icon="el-icon-plus" @click="addRules"></el-button>
                  </el-col>
                </el-row>
              </el-form-item>
              <hr />
              <el-form-item label="动作：" prop="action">
                <el-row :gutter="15">
                  <el-col :span="5">
                    <el-select v-model="routerForm.action">
                      <el-option value="deny" label="拒绝">拒绝(规则中的来源将都会被拒绝，但没在其中的默认允许)</el-option>
                      <el-option value="filter" label="过滤">过滤(满足条件的提供者将能被消费者访问)</el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="3">
                    <el-tooltip placement="top" effect="light">
                      <div slot="content">
                        <p>
                          1. 默认允许所有消费者访问<br />
                          2. 当某个消费者同时匹配黑名单和白名单时，优先白名单 <br />
                          3. 一个服务只能有一条白名单规则，否则两条规则交叉，就都被筛选掉了 <br />
                          4. 支持乏匹配，如:172.20.10.*
                        </p>
                      </div>
                      <i class="el-icon-question"></i>
                    </el-tooltip>
                  </el-col>
                </el-row>
              </el-form-item>
              <el-form-item label="过滤提供者：" prop="filters" v-if="routerForm.action=='filter'">
                <el-row v-if="routerForm.filters==''" style="color:gray">没有匹配规则</el-row>
                <template v-for="filter,index in routerForm.filters">
                  <el-row :gutter="15" style="margin-bottom:5px;">
                    <el-col :span="5" style="padding-left:7.5px;">
                      <span v-if="filter.name == 'provider.host'">提供者IP</span>
                      <span v-if="filter.name == 'provider.cluster'">提供者集群</span>
                      <span v-if="filter.name == 'provider.protocol'">提供者协议</span>
                      <span v-if="filter.name == 'provider.port'">提供者端口</span>
                    </el-col>
                    <el-col :span="3">
                      {{filter.ex}}
                    </el-col>
                    <el-col :span="12">
                      {{filter.value}}
                    </el-col>
                    <el-col :span="3"  style="padding-left:18px">
                      <el-button icon="el-icon-minus" @click="routerForm.filters.splice(index,1)"></el-button>
                    </el-col>
                  </el-row>
                </template>
              </el-form-item>
              <el-form-item label=" " v-if="routerForm.action=='filter'">
                <el-row :gutter="15">
                  <el-col :span="5">
                    <el-select v-model="routerFilterData.name" placeholder="来源IP或应用">
                      <el-option value="provider.host" label="提供者IP">提供者IP</el-option>
                      <el-option value="provider.cluster" label="提供者集群">提供者集群</el-option>
                      <el-option value="provider.protocol" label="提供者协议">提供者协议</el-option>
                      <el-option value="provider.port" label="提供者端口">提供者端口</el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="3">
                    <el-select v-model="routerFilterData.ex" placeholder="匹配">
                      <el-option value="=">=</el-option>
                      <el-option value="!=">!=</el-option>
                    </el-select>
                  </el-col>
                  <el-col :span="12">
                    <el-tooltip placement="top">
                      <div slot="content">
                        <div>该服务的提供者有：<span v-for="c in nearinfo.provider">{{c}},&nbsp</span></div>
                      </div>
                      <el-input v-model="routerFilterData.value" placeholder="输入匹配的内容，以逗号分隔"></el-input>
                    </el-tooltip>
                  </el-col>
                  <el-col :span="3">
                    <el-button icon="el-icon-plus" @click="addFilters"></el-button>
                  </el-col>
                </el-row>
              </el-form-item>
              <el-form-item>
                <el-button style="float:right;margin-left:10px;" type="primary" @click="save_create_form('routerForm')">提交</el-button>
                <el-button style="float:right" @click="show_create_modal = false">关闭</el-button>
              </el-form-item>
            </el-form>
            <!--         <span slot="footer" class="dialog-footer">
            <el-button @click="show_create_modal = false">关闭</el-button>
            <el-button type="primary" @click="save_create_form('routerForm')">提交</el-button>

          </span>
 -->
          </el-col>
        </el-row>
      </el-dialog>
      <el-dialog title="路由操作日志" class="dialog-center" :visible.sync="show_log_modal" width="65%" top="0%" close-on-press-escape close-on-click-modal>
        <data-tables :data="router_log_list">
          <el-table-column align="center" prop="name" label="名称" />
          <el-table-column align="center" prop="username" label="操作人" />
          <el-table-column align="center" prop="msg" label="描述">
          </el-table-column>
          <el-table-column align="center" prop="status" label="状态">
            <template slot-scope='scope'>
              <el-button size="mini" type="success" v-if="scope.row.status==1" circle icon="el-icon-success"></el-button>
              <el-button size="mini" type="danger" v-if="scope.row.status==0" circle icon="el-icon-error"></el-button>
            </template>
          </el-table-column>
          <el-table-column align="center" prop="create_time" label="创建时间" show-overflow-tooltip />
        </data-tables>
        <span slot="footer" class="dialog-footer">
            <el-button @click="show_log_modal = false">关闭</el-button>
          </span>
      </el-dialog>
    </div>
  </div>
</template>
<style>
</style>
<script>
import echarts from 'echarts'

import { DubboRoutersApi, DubboConfigsApi, DubboTopologyApi, DubboTopologyNearInfoApi } from '@/http/url'
export default {
  name: 'router',
  data() {
    var checkRuleData = (rule, value, callback) => {
      console.log('value,', value, rule)

      if (value.length == 0) {
        return callback(new Error('请输入规则！'))
      }
      if (value.name == '' || value.ex == '' || value.value == '') {
        return callback(new Error('请输入完整的规则！'))
      }

      callback();
    };
    return {

      router_list: [], //路由列表
      config_list: [], //dubbo zk集群列表
      service_list: [], //服务节点列表
      router_log_list: [], //路由操作日志列表
      nearinfo: {},
      show_edit_modal: false,
      show_create_modal: false,
      show_log_modal: false,
      sync_loading_status: false,
      nodes: [],
      links: [],
      activeName2: 'blackwhite',
      routerForm: { //路由新增表单
        name: '',
        // priority: 0,
        path: '',
        action: '',
        someAllowValue: '',
        someDenyValue: '',
        rules: [], // [{name:'',ex:'',value:''}]
        filters: [], // [{name:'',ex:'',value:''}]
        enabled: 'true',
      },
      routerRuleData: {
        'name': '',
        'ex': '',
        'value': '',
      },
      routerFilterData: {
        'name': '',
        'ex': '',
        'value': '',
      },

      tableProps: {
        highlightCurrentRow: true,
        border: true,
      },
      query: {
        dubbo_id: '',
        name: '',
      },
      categories: [
        { name: 'application', itemStyle: { color: '#B8860B' } },
        { name: 'service', itemStyle: { color: '#55AA00' } },
        { name: 'provider', itemStyle: { color: '#6495ED' } },
        { name: 'consumer', itemStyle: { color: '#0088A8' } },
      ], // 图中展示的分类
      rules: {
        name: { required: true, message: '请输入名称！', trigger: 'blur' },
        path: { required: true, message: '请输入服务！', trigger: 'change' },
        enabled: { required: true, message: '请选择是否使能！', trigger: 'blur' },
        rules: { validator: checkRuleData, trigger: 'change' },
        filters: { validator: checkRuleData, trigger: 'change' },
        action: { required: true, message: '请选择动作！', trigger: 'change' }
      },

    }
  },
  methods: {
    clear_form_value() {
      // this.$refs['routerForm'].resetFields(); //清空表单校验  

      for (var k in this.routerForm) {
        this.routerForm[k] = ''
      };
      this.routerForm.rules = []
      this.routerForm.filters = []
      for (var k in this.routerRuleData) {
        this.routerRuleData[k] = ''
      }
    },
    toggle_router_enable(row){
      var self = this
      this.$http.put(DubboRoutersApi+'/'+row.id+'/toggle').then((response)=>{
        self.$message(response.data.msg)
        if (response.data.status == 1){
          console.log(row.enabled,response.data.result.enabled)

          row.enabled = response.data.result.enabled
        }
      })
    },
    save_edit_form(formName) {
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.$http.put(DubboRoutersApi + '/' + self.routerForm.id, self.routerForm).then((response) => {
            self.$message(response.data.msg)
            if (response.data.status == 1) {
              self.get_router_list()
              self.show_edit_modal = false
            }
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      })
    },
    save_create_form(formName) {
      var self = this
      self.routerForm.dubbo_id = self.query.dubbo_id
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.$http.post(DubboRoutersApi, self.routerForm).then((response) => {
            self.$message(response.data.msg)
            if (response.data.status == 1) {
              self.get_router_list()
              self.show_create_modal = false
            }
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });

    },
    sync_routers_by_zk() {
      var self = this
      self.sync_loading_status = true
      this.$http.post(DubboRoutersApi + '/' + self.query.dubbo_id + '/sync').then((response) => {
        self.$message(response.data.msg)
        self.sync_loading_status = false
        if (response.data.status == 1) {
          self.get_router_list()
        }
      })
    },
    get_router_list() {
      var self = this
      self.router_list = []
      self.router_log_list = []
      self.service_list = []
      this.$http.get(DubboRoutersApi, { params: self.query }).then((response) => {
        self.router_list = response.data.result
        self.router_info = Object.assign({}, self.router_list[0])
        self.get_service_list()
      })
    },
    get_router_info(id) {
      var self = this
      self.clear_form_value()
      this.$http.get(DubboRoutersApi + '/' + id).then((response) => {
        self.routerForm = response.data.result
        console.log('router_info', self.router_info)
        self.get_node_info('edit')
        // self.relate_echart()

      })
    },
    get_dubbo_config_list() {
      var self = this
      this.$http.get(DubboConfigsApi).then((response) => {
        self.config_list = response.data.result
        self.query.dubbo_id = self.config_list[0].id
        self.get_router_list()

      })
    },
    del_router(id) {
      var self = this
      this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {
        self.$http.delete(DubboRoutersApi + '/' + id).then((response) => {
          self.$message(response.data.msg)
          if (response.data.status == 1) {
            self.get_router_list()
          }
        })
      })
    },
    get_service_list() {
      var self = this
      var service_nodes_url = DubboTopologyApi + '/' + self.query.dubbo_id + '/service'
      this.$http.get(service_nodes_url).then((response) => {
        self.service_list = response.data.result
        console.log('service list ', self.service_list)
      })
    },
    querySearch(queryString, cb) {
      var restaurants = this.service_list;
      var results = []
      for (var n in restaurants) {
        if (restaurants[n].name.toLowerCase().indexOf(queryString.toLowerCase()) != -1) {
          results.push(restaurants[n])
        }
      }
      // var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
      // 调用 callback 返回建议列表的数据
      cb(results);
    },
    show_router_log() {
      this.show_log_modal = true
      var self = this
      self.$http.get(DubboRoutersApi + '/' + self.query.dubbo_id + '/logs').then((response) => {
        self.router_log_list = response.data.result

      })

    },
    get_node_info(item) {
      var self = this
      var d = {
        dubbo_id: this.query.dubbo_id,
      }
      if (item == 'create') {
        d.path = this.routerForm.path
      } else if (item == 'edit') {
        d.path = this.router_info.path
      } else if (typeof item.name == 'string') {
        d.path = item.name
      }
      console.log('dict', d)
      this.nearinfo = {}
      this.$http.get(DubboTopologyNearInfoApi, { params: d }).then((response) => {
        self.nearinfo = Object.assign({}, response.data.result)
        self.relate_echart(item)
        console.log('near info...', self.nearinfo)
      })
    },
    addRules() {
      console.log('add rules', this.routerForm.rules)
      var d = {
        'name': this.routerRuleData.name,
        'ex': this.routerRuleData.ex,
        'value': this.routerRuleData.value,
      }

      if (d.name == '' || d.ex == '' || d.value == '') {
        this.$message('添加规则，内容未输完整！')
        return
      }
      console.log('rules', this.routerForm.rules)
      if (this.routerForm.rules == undefined) {

        this.routerForm.rules = [d]
      } else {
        this.routerForm.rules.push(d)
      }
      this.routerRuleData.name = ''
      this.routerRuleData.ex = ''
      this.routerRuleData.value = ''

    },
    addFilters() {
      var d = {
        'name': this.routerFilterData.name,
        'ex': this.routerFilterData.ex,
        'value': this.routerFilterData.value,
      }
      if (d.name == '' || d.ex == '' || d.value == '') {
        this.$message('添加规则，内容未输完整！')
        return
      }
      console.log('rules', this.routerForm.filters)

      if (typeof this.routerForm.filters != 'object') {
        this.routerForm.filters = [d]
      } else {
        this.routerForm.filters.push(d)
      }
      this.routerFilterData.name = ''
      this.routerFilterData.ex = ''
      this.routerFilterData.value = ''
    },
    relate_echart(tag) {
      if (tag == 'edit') {
        var id = 'chart_edit'
      } else {
        var id = 'chart_create'
      }
      console.log(tag, 'chart id:', id)

      this.myChart = echarts.init(document.getElementById(id))
      // this.myChart = myChart
      var self = this

      this.myChart.showLoading()
      self.nodes = []
      self.links = []
      var query = {
        dubbo_id: this.query.dubbo_id,
        deep: 1,
        name: this.routerForm.path,

      }
      this.$http.get(DubboTopologyApi, { params: query }).then((response) => {
        self.nodes = response.data.result.nodes
        self.links = response.data.result.links

        self.myChart.hideLoading()
        for (var n in self.nodes) {
          self.nodes[n].label = {
            normal: {
              show: true
            }
          }

          if (self.nodes[n].category == self.query.category) {
            self.nodes[n].symbolSize = 30
          } else {
            if (self.nodes[n].category == 'application') {
              if (self.query.category == "") {
                self.nodes[n].symbolSize = 30
                self.nodes[n].label = {
                  normal: {
                    show: true
                  }
                }
              } else {
                self.nodes[n].symbolSize = 30
              }
            } else if (self.nodes[n].category == 'service') {
              self.nodes[n].symbolSize = 20
              // self.nodes[n].itemStyle = {color:'#99FF99'}
            } else if (self.nodes[n].category == 'provider') {
              self.nodes[n].symbolSize = 15
              // self.nodes[n].itemStyle = {color:'#CCCCFF'}
            } else {
              self.nodes[n].symbolSize = 15
              // self.nodes[n].itemStyle = {color:'#CCCCFF'}

            }

          }
        }
        var option = {
          title: {
            text: '',
            subtext: 'Default layout',
            top: 'bottom',
            left: 'right'
          },
          tooltip: {
            show: false
          },
          legend: [{
            // selectedMode: 'single',
            // align:'right',
            left: 'right',
            data: self.categories.map(function(a) {
              return a.name
            })
          }],
          animationDuration: 500,
          animationEasingUpdate: 'quinticInOut',

          series: [{
            name: 'dubbo',
            type: 'graph',
            layout: 'force',
            data: self.nodes,
            links: self.links,
            categories: self.categories,
            roam: true,
            // legendHoverLink:true,
            focusNodeAdjacency: true, // 选中高亮周周的线

            label: {
              normal: {
                position: 'right',
                // show:true
              },
            },
            force: { // 力引导图基本配置
              // initLayout: ,//力引导的初始化布局，默认使用xy轴的标点
              repulsion: 400, // 节点之间的斥力因子。支持数组表达斥力范围，值越大斥力越大。
              // gravity : 0.03,//节点受到的向中心的引力因子。该值越大节点越往中心点靠拢。
              edgeLength: 120, // 边的两个节点之间的距离，这个距离也会受 repulsion。[10, 50] 。值越小则长度越长
              layoutAnimation: true
              // 因为力引导布局会在多次迭代后才会稳定，这个参数决定是否显示布局的迭代动画，在浏览器端节点数据较多（>100）的时候不建议关闭，布局过程会造成浏览器假死。                        
            },
            draggable: true, // 指示节点是否可以拖动
            edgeSymbol: ['none', 'arrow'], // 加上方向箭头  
            edgeLabel: { // 显示方向线的值
              normal: {
                show: true,
                position: 'middle',
                formatter: function(param) { return param.data.category },
                textStyle: {
                  fontSize: 8
                },
                verticalAlign: 'bottom'
              }
            },
          }]
        }
        self.myChart.setOption(option)

      })
    }

  },
  mounted() {
    this.get_dubbo_config_list()
  },
}

</script>
