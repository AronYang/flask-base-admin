<template>
  <div class="card">
    <div class="card-body">
      <el-row style="margin-bottom:15px">
        <el-select v-model="query.dubbo_id" @change.passive="get_router_list">
          <el-option v-for="config in config_list" :label="config.name" :key="config.id" :value="config.id">{{config.name}}</el-option>
        </el-select>
        <el-input v-model="query.name" @keyup.enter.native="get_router_list" placeholder="搜索路由名称" style="width:200px"></el-input>
        <el-button @click="get_router_list" icon="el-icon-search" type="primary">搜索</el-button>
        <el-button type="primary" @click="show_create_modal=true">_新增</el-button>

        <el-tooltip class="item" effect="dark" content="查看路由操作日志" placement="top-start">
          <el-button type="warning" style="float: right" @click="show_router_log" icon="el-icon-tickets" circle></el-button>
        </el-tooltip>

        <el-tooltip class="item" effect="dark" content="同步当前集群的所有路由规则，大概需要几十秒时间" placement="top-start">
          <el-button type="primary" style="float: right" @click="sync_routers_by_zk" :loading="sync_loading_status" icon="el-icon-refresh" circle></el-button>
        </el-tooltip>

      </el-row>
      <data-tables :data="router_list" :table-props="tableProps">
        <el-table-column sortable prop="name"  align="center" label="路由名称" show-overflow-tooltip>
          <template slot-scope='scope'>
            <el-button type='text' @click="router_info=Object.assign({},scope.row); show_modal=true">{{scope.row.name}}</el-button>
          </template>
        </el-table-column>
        <el-table-column sortable align="center"  prop="path" label="服务名" show-overflow-tooltip />
        <el-table-column sortable align="center"  prop="priority" label="优先级" width="100" />
        <el-table-column sortable align="center"  prop="enabled" label="状态" width="100">
          <template slot-scope='scope'>
            <el-button size="mini" type="success" v-if="scope.row.enabled=='true'" @click=
            "router_info=Object.assign({},scope.row);scope.row.enabled='false';save_edit_form()">已启用</el-button>
            <el-button size="mini" type="danger" v-if="scope.row.enabled=='false'" @click=
            "router_info=Object.assign({},scope.row);scope.row.enabled='true';save_edit_form()">已禁用</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="id"  align="center" label="操作" width="120">
          <template slot-scope="scope">
            <el-button  icon="el-icon-edit" circle size="small" @click="show_edit_modal=true;router_info=Object.assign({},scope.row);get_node_info('edit')">
              
            </el-button>
            </router-link>
            <el-button type="danger" icon="el-icon-delete" circle size="small" @click="del_router(scope.row.id)"></el-button>
          </template>
        </el-table-column>
      </data-tables>
      <el-dialog title="路由详情" :visible.sync="show_modal" width="50%" top="0%" close-on-press-escape close-on-click-modal>
        <el-form ref="form" v-model="router_info" label-width="150px" style="margin-bottom:0">
          <el-form-item label="路由名称" prop="name">
            {{router_info.name}}
          </el-form-item>
          <el-form-item label="状态:">
            <el-tag type='success' v-if="router_info.enabled=='true'">已启用</el-tag>
            <el-tag type='danger' v-if="router_info.enabled=='false'">已禁用</el-tag>
          </el-form-item>
          <el-form-item label="优先级">{{router_info.priority}}
          </el-form-item>
          <el-form-item label="服务名" prop="path">
            {{router_info.path}}
          </el-form-item>
          <el-form-item label="匹配规则">
            <el-row>
              <el-col :span="8">条件</el-col>
              <el-col :span="8">匹配</el-col>
              <el-col :span="8">不匹配</el-col>
            </el-row>
            <el-row>
              <el-col :span="8">消费者IP：</el-col>
              <el-col :span='8'>
                {{router_info.consumer_host_equal}}
              </el-col>
              <el-col :span='8'>
                {{router_info.consumer_host_not_equal}}
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="8">消费者应用：</el-col>
              <el-col :span='8'>
                {{router_info.consumer_application_equal}}
              </el-col>
              <el-col :span='8'>
                {{router_info.consumer_application_not_equal}}
              </el-col>
            </el-row>
<!--             <el-row>
              <el-col :span="8">消费者集群：</el-col>
              <el-col :span='8'>
                {{router_info.consumer_cluster_equal}}
              </el-col>
              <el-col :span='8'>{{router_info.consumer_cluster_not_equal}}
              </el-col>
            </el-row> -->
          </el-form-item>
          <el-form-item label="过滤条件">
            <el-row>
              <el-col :span="8">条件</el-col>
              <el-col :span="8">匹配</el-col>
              <el-col :span="8">不匹配</el-col>
            </el-row>
            <el-row>
              <el-col :span="8">提供者IP：</el-col>
              <el-col :span='8'>{{router_info.provider_host_equal}}
              </el-col>
              <el-col :span='8'>{{router_info.provider_host_not_equal}}
              </el-col>
            </el-row>
<!--             <el-row>
              <el-col :span="8">提供者集群：</el-col>
              <el-col :span='8'>{{router_info.provider_application_equal}}
              </el-col>
              <el-col :span='8'>
                {{router_info.provider_application_not_equal}}
              </el-col>
            </el-row> -->
            <el-row>
              <el-tag type="info" style="width:100%">     1. 当过滤条件为空时，代表拒绝匹配条件里的请求。</el-tag>   
              <el-tag type="info" style="width:100%">      2. 默认允许所有消费者访问。  </el-tag>
               <el-tag type="info" style="width:100%">     3. 当允许和拒绝的规则同时存在时，优先允许规则。</el-tag>
            </el-row>

          </el-form-item>

        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="show_modal = false">关闭</el-button>
          </span>
      </el-dialog>

      <el-dialog title="路由编辑" class="dialog-center" :visible.sync="show_edit_modal" width="65%" top="0%" close-on-press-escape close-on-click-modal>
        <el-form ref="form" label-width="150px" :model="router_info" :rules="rules">
          <el-form-item label="路由名称" prop="name">
            <el-input v-model="router_info.name"></el-input>
          </el-form-item>
          <el-form-item label="状态:" prop="enabled">
            <el-radio v-model="router_info.enabled" label="true">启用</el-radio>
            <el-radio v-model="router_info.enabled" label="false">禁用</el-radio>
          </el-form-item>
<!--           <el-form-item label="优先级">
            <el-input type="number" v-model="router_info.priority"></el-input>
          </el-form-item> -->
          <el-form-item label="服务名" prop="path">
            {{router_info.path}}
            <el-button type="primary" size="mini" @click="get_node_info('edit')">服务详情</el-button>
            <div v-for="(v,k) in nearinfo" style="margin:0;padding:0;display:none">
                {{k}}:  
                <span v-for="i,index in v">
                    <span style="color:purple;" v-if="index == 0">{{i}}</span>
                    <span v-else>, <span style="color:purple;">{{i}}</span></span>
                </span> 
            </div>
          </el-form-item>
  <el-tabs v-model="activeName2" type="card" @tab-click="tabHandleClick">
    <el-tab-pane label="黑白名单视图" name="blackwhite">
      <el-form-item label="允许访问IP列表" >
        <el-input type="textarea" v-model="accessData.allow_ips" :rows="2"></el-input>
      </el-form-item>
      <el-form-item label="拒绝访问IP列表">
        <el-input type="textarea" v-model="accessData.deny_ips" :rows="2"></el-input>
      </el-form-item>

    </el-tab-pane>

    <el-tab-pane label="路由视图" name="route">
           <el-form-item label="匹配规则">
            <el-row>
              <el-col :span="8">条件</el-col>
              <el-col :span="8">匹配</el-col>
              <el-col :span="8">不匹配</el-col>
            </el-row>
            <el-row>
              <el-col :span="8">消费者IP：</el-col>
              <el-col :span='8'>
                <el-input v-model="router_info.consumer_host_equal" placeholder="consumer ip"></el-input>
              </el-col>
              <el-col :span='8'>
                <el-input v-model="router_info.consumer_host_not_equal" placeholder="consumer ip"></el-input>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="8">消费者应用：</el-col>
              <el-col :span='8'>
                <el-input v-model="router_info.consumer_application_equal"></el-input>
              </el-col>
              <el-col :span='8'>
                <el-input v-model="router_info.consumer_application_not_equal"></el-input>
              </el-col>
            </el-row>
<!--             <el-row>
              <el-col :span="8">消费者集群：</el-col>
              <el-col :span='8'>
                <el-input v-model="router_info.consumer_cluster_equal"></el-input>
              </el-col>
              <el-col :span='8'>
                <el-input v-model="router_info.consumer_cluster_not_equal"></el-input>
              </el-col>
            </el-row> -->
          </el-form-item>
          <el-form-item label="过滤条件">
            <el-row>
              <el-col :span="8">条件</el-col>
              <el-col :span="8">匹配</el-col>
              <el-col :span="8">不匹配</el-col>
            </el-row>
            <el-row>
              <el-col :span="8">提供者IP：</el-col>
              <el-col :span='8'>
                <el-input v-model="router_info.provider_host_equal"></el-input>
              </el-col>
              <el-col :span='8'>
                <el-input v-model="router_info.provider_host_not_equal"></el-input>
              </el-col>
            </el-row>
 <!--            <el-row>
              <el-col :span="8">提供者集群：</el-col>
              <el-col :span='8'>
                <el-input v-model="router_info.provider_application_equal"></el-input>
              </el-col>
              <el-col :span='8'>
                <el-input v-model="router_info.provider_application_not_equal"></el-input>
              </el-col>
            </el-row> -->

            <el-row>
              <el-tag type="info" style="width:100%">     1. 当过滤条件为空时，代表拒绝匹配条件里的请求。</el-tag>   
              <el-tag type="info" style="width:100%">      2. 默认允许所有消费者访问。  </el-tag>
               <el-tag type="info" style="width:100%">     3. 当允许和拒绝的规则同时存在时，优先允许规则。</el-tag>
            </el-row>     
          </el-form-item>

    </el-tab-pane>
  </el-tabs>          

        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="show_edit_modal = false">关闭</el-button>
            <el-button type="primary" @click="save_edit_form('form')">提交</el-button>

          </span>
      </el-dialog>
      <el-dialog title="路由新增" class="dialog-center" :visible.sync="show_create_modal" width="65%" top="0%" close-on-press-escape close-on-click-modal>
        <el-form ref="routerForm" label-width="100px" :model="routerForm" :rules="rules">
          <el-form-item label="路由名称" prop="name">
            <el-input v-model="routerForm.name"></el-input>
          </el-form-item>
          <el-form-item label="状态:" prop="enabled">
            <el-radio v-model="routerForm.enabled" label="true">启用</el-radio>
            <el-radio v-model="routerForm.enabled" label="false">禁用</el-radio>
          </el-form-item>
<!--           <el-form-item label="优先级">
            <el-input type="number" v-model="routerForm.priority"></el-input>
          </el-form-item> -->
          <el-form-item label="服务名" prop="path">
            <!-- <el-input v-model="routerForm.path" ></el-input> -->
            <el-autocomplete
              v-model="routerForm.path"
              value-key="name"
              :fetch-suggestions="querySearch"
              placeholder="请输入服务名"
              style="width:100%"
              @select="get_node_info"></el-autocomplete>
            <el-button type="primary" size="mini" @click="get_node_info('create')">服务详情</el-button>
            <div v-for="(v,k) in nearinfo" style="margin:0;padding:0">
                {{k}}:  
                <span v-for="i,index in v">
                    <span style="color:purple;" v-if="index == 0">{{i}}</span>
                    <span v-else>, <span style="color:purple;">{{i}}</span></span>
                </span> 
            </div>

          </el-form-item>
          <el-form-item label="匹配规则">
            <el-row>
              <el-col :span="8">条件</el-col>
              <el-col :span="8">匹配</el-col>
              <el-col :span="8">不匹配</el-col>
            </el-row>
            <el-row>
              <el-col :span="8">消费者IP：</el-col>
              <el-col :span='8'>
                <el-input v-model="routerForm.consumer_host_equal"></el-input>
              </el-col>
              <el-col :span='8'>
                <el-input v-model="routerForm.consumer_host_not_equal"></el-input>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="8">消费者应用：</el-col>
              <el-col :span='8'>
                <el-input v-model="routerForm.consumer_application_equal"></el-input>
              </el-col>
              <el-col :span='8'>
                <el-input v-model="routerForm.consumer_application_not_equal"></el-input>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="8">消费者集群：</el-col>
              <el-col :span='8'>
                <el-input v-model="routerForm.consumer_cluster_equal"></el-input>
              </el-col>
              <el-col :span='8'>
                <el-input v-model="routerForm.consumer_cluster_not_equal"></el-input>
              </el-col>
            </el-row>
          </el-form-item>
          <el-form-item label="过滤条件">
            <el-row>
              <el-col :span="8">条件</el-col>
              <el-col :span="8">匹配</el-col>
              <el-col :span="8">不匹配</el-col>
            </el-row>
            <el-row>
              <el-col :span="8">提供者IP：</el-col>
              <el-col :span='8'>
                <el-input v-model="routerForm.provider_host_equal"></el-input>
              </el-col>
              <el-col :span='8'>
                <el-input v-model="routerForm.provider_host_not_equal"></el-input>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="8">提供者集群：</el-col>
              <el-col :span='8'>
                <el-input v-model="routerForm.provider_cluster_equal"></el-input>
              </el-col>
              <el-col :span='8'>
                <el-input v-model="routerForm.provider_cluster_not_equal"></el-input>
              </el-col>
            </el-row>
            <el-row>
              <el-tag type="info" style="width:100%">     1. 当过滤条件为空时，代表拒绝匹配条件里的请求。</el-tag>   
              <el-tag type="info" style="width:100%">      2. 默认允许所有消费者访问。  </el-tag>
               <el-tag type="info" style="width:100%">     3. 当允许和拒绝的规则同时存在时，优先允许规则。</el-tag>
            </el-row>

          </el-form-item>

        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="show_create_modal = false">关闭</el-button>
            <el-button type="primary" @click="save_create_form('routerForm')">提交</el-button>

          </span>
      </el-dialog>


      <el-dialog title="路由操作日志" class="dialog-center" :visible.sync="show_log_modal" width="65%" top="0%" close-on-press-escape close-on-click-modal>
        <data-tables :data="router_log_list">
        <el-table-column align="center" prop="name" label="名称"/>
        <el-table-column align="center" prop="username" label="操作人" />
        <el-table-column align="center" prop="msg" label="描述">
        </el-table-column>
        <el-table-column align="center" prop="status" label="状态" >
          <template slot-scope='scope'>
            <el-button size="mini" type="success" v-if="scope.row.status==1" circle icon="el-icon-success"></el-button>
            <el-button size="mini" type="danger" v-if="scope.row.status==0" circle icon="el-icon-error"></el-button>
          </template>          
          
        </el-table-column>

        <el-table-column align="center" prop="create_time" label="创建时间"  show-overflow-tooltip />
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
import { DubboRoutersApi, DubboConfigsApi, DubboTopologyApi, DubboTopologyNearInfoApi } from '@/http/url'
export default {
  name: 'router',
  data() {
    return {
      router_list: [],  //路由列表
      config_list: [],  //dubbo zk集群列表
      router_info: {},  //路由编辑表单
      service_list:[], //服务节点列表
      router_log_list:[], //路由操作日志列表
      nearinfo:{},
      show_modal: false,  
      show_edit_modal: false,
      show_create_modal: false,
      show_log_modal:false,
      sync_loading_status: false,
      activeName2:'blackwhite',
      routerForm: { //路由新增表单
        name: '',
        priority: 0,
        path: '',
        consumer_host_equal: '',
        consumer_host_not_equal: '',
        consumer_application_equal: '',
        consumer_application_not_equal: '',
        consumer_cluster_equal: '',
        consumer_cluster_not_equal: '',
        provider_host_equal: '',
        provider_host_not_equal: '',
        provider_cluster_equal: '',
        provider_cluster_not_equal: '',
        enabled: 'true',
      },
      accessData:{
        allow_ips:'',
        deny_ips:'',
      },
      tableProps: { 
        highlightCurrentRow: true,
        border: true,
      },
      query: {
        dubbo_id: '',
        name: '',
      },
      rules: {
        name: { required: true, message: '请输入名称！', trigger: 'blur' },
        path: { required: true, message: '请输入服务！', trigger: 'change' },
        enabled: { required: true, message: '请选择是否使能！', trigger: 'blur' },
      },

    }
  },
  methods: {
    save_edit_form() {
      var self = this
      this.$http.put(DubboRoutersApi + '/' + self.router_info.id, self.router_info).then((response) => {
        self.$message(response.data.msg)
        if (response.data.status == 1) {
          self.get_router_list()
          self.show_edit_modal = false
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
    get_service_list(){
      var self = this  
      var service_nodes_url = DubboTopologyApi+'/'+self.query.dubbo_id+'/service'
      this.$http.get(service_nodes_url).then((response)=>{
        self.service_list = response.data.result  
        console.log('service list ',self.service_list)
      })
    },
      querySearch(queryString, cb) {
        var restaurants = this.service_list;
        var results = []
        for (var n in restaurants){
          if(restaurants[n].name.toLowerCase().indexOf(queryString.toLowerCase()) != -1 ){
            results.push(restaurants[n])
          }
        }
        // var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      show_router_log(){
        this.show_log_modal = true  
        var self = this  
        self.$http.get(DubboRoutersApi+'/'+self.query.dubbo_id+'/logs').then((response)=>{
            self.router_log_list = response.data.result  

        })

      },
      get_node_info(item) {
        var self = this
        var d = {
          dubbo_id: this.query.dubbo_id,  
        }
        if( item == 'create'){
          d.path = this.routerForm.path  
        }else if(item=='edit'){
          d.path = this.router_info.path
        }else if(typeof item.name == 'string'){
          d.path = item.name
        }
        console.log('dict',d)
        this.nearinfo = {}
        this.$http.get(DubboTopologyNearInfoApi,{params:d}).then((response) => {
          self.nearinfo = Object.assign({},response.data.result)
        })
      },
      convert_blackwhite_to_router(){
          this.router_info.consumer_host_not_equal = this.accessData.allow_ips  
          this.router_info.consumer_host_equal = this.accessData.deny_ips  
      },
      tabHandleClick(tab,event){

        this.convert_blackwhite_to_router()
        console.log('tab',tab,event)
      }
  },
  mounted() {
    this.get_dubbo_config_list()
  },
}

</script>
