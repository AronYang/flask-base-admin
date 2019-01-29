<template>
  <div class="card">
    <div class="card-body">
      <el-row>
        <el-input  v-model="search" style="width:500px" placeholder="请输入集群名称"></el-input>
        <el-button type="primary" icon="el-icon-search" @click="get_dubbo_configs_list">搜索</el-button>
        <el-button type="primary" @click="show_create_modal=true" style="margin-bottom:15px;">_新增</el-button>
      </el-row>
      <el-row :gutter="32"  v-for="config in config_list" :key="config.id" >
        <el-col :span="8" style="margin-bottom: 24px;height:220px;padding:30px;">
          <el-card class="box-card" style=" text-align: center;">
            <h5 style="margin-bottom:20px">{{config.name}}</h5>
            <p style="padding: 5px 10px 10px;margin-bottom: 20px;border-bottom: 1px solid #dbdddf;" />
            <small style="color:gray;overflow:hidden;white-space:nowrap; ">{{config.address}}</small>
            <el-row>
              <el-tooltip class="item" effect="dark" content="同步当前集群的所有节点以及路由规则，大概需要几分钟时间。" placement="top-start">
                <el-button type="text" style="float:left" icon="el-icon-refresh" :loading="loading_status(config.id)" @click="sync_dubbo_config(config.id)">同步</el-button>
              </el-tooltip>
              <el-dropdown @command="handleDropdownCommand($event, config)" style="float: right">
                <span class="el-dropdown-link">
                    <small></small>
                    <i class="el-icon-arrow-down el-icon--right" />
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="edit">
                    编 辑
                  </el-dropdown-item>
                  <el-dropdown-item command="delete">
                    删 除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </el-row>
          </el-card>
        </el-col>
        <el-col :span="12" style="margin-left:24px;">
          <div style="height:250px;width:700px;">
            <div v-bind:id="config.id" style="height:200px;width:700px"></div>
          </div>
        </el-col>
      </el-row>

      <el-dialog title="新增dubbo配置" :visible.sync="show_create_modal" width="50%" top="0%" close-on-press-escape close-on-click-modal>
        <el-form :model="createForm" :rules="rules" ref="create_form" label-width="120px">
          <el-form-item label="名称：" prop="name">
            <el-input v-model="createForm.name"></el-input>
          </el-form-item>
          <el-form-item label="zk地址：" placeholder="ip:port  多个地址时以逗号分隔" prop="address">
            <el-input v-model="createForm.address"></el-input>
          </el-form-item>
          <el-form-item label="dubbo根节点：" placeholder="默认/dubbo">
            <el-input v-model="createForm.node"></el-input>
          </el-form-item>
          <el-form-item label="描述：">
            <el-input v-model="createForm.description"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="show_create_modal = false">关闭</el-button>
            <el-button type="primary" @click="create_form('create_form')">保存</el-button>

          </span>
      </el-dialog>
      <el-dialog title="编辑dubbo配置" :visible.sync="show_edit_modal" width="50%" top="0%" close-on-press-escape close-on-click-modal>
        <el-form :model="editForm" :rules="rules" ref="editForm" label-width="120px">
          <el-form-item label="名称：" prop="name">
            <el-input v-model="editForm.name"></el-input>
          </el-form-item>
          <el-form-item label="zk地址：" placeholder="ip:port  多个地址时以逗号分隔" prop="address">
            <el-input v-model="editForm.address"></el-input>
          </el-form-item>
          <el-form-item label="dubbo根节点：" placeholder="默认/dubbo">
            <el-input v-model="editForm.node"></el-input>
          </el-form-item>
          <el-form-item label="描述：">
            <el-input v-model="editForm.description"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="show_edit_modal = false">关闭</el-button>
            <el-button type="primary" @click="save_edit_form('editForm')">保存</el-button>

          </span>
      </el-dialog>
    </div>
  </div>
</template>
<script>
import { DubboConfigsApi } from '@/http/url'
import echarts from 'echarts'

export default {
  name: 'router',
  data() {
    return {
      config_list: [],
      show_create_modal: false,
      show_edit_modal: false,
      sync_dubbo_id: '',
      search:'',
      editForm: {
        name: '',
        address: '',
        node: '',
        description: '',
      },
      createForm: {
        name: '',
        address: '',
        node: '/dubbo',
        description: '',
      },
      rules: {
        name: { required: true, message: '请输入名称', trigger: 'blur' },
        address: { required: true, message: '请输入地址', trigger: 'blur' },
      },

    }
  },
  methods: {
    loading_status(id) {
      if (this.sync_dubbo_id == id) {
        return true
      } else { return false }
    },
    handleDropdownCommand(event, config) {
      if (event == 'edit') {
        this.show_edit_modal = true
        this.editForm = config
      }
      if (event == 'delete') {
        this.del_dubbo_config(config.id)
      }

    },
    sync_dubbo_config(id) {
      var self = this
      this.sync_dubbo_id = id
      this.$http.post(DubboConfigsApi + '/' + id + '/sync').then((response) => {
        self.$message(response.data.msg)
        self.sync_dubbo_id = ''
      })
    },
    create_form(formName) {
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.$http.post(DubboConfigsApi, self.createForm).then((response) => {
            self.$message(response.data.msg)
            if (response.data.status == 1) {
              self.show_create_modal = false
              self.get_dubbo_configs_list()
            }
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    save_edit_form(formName) {
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          self.$http.put(DubboConfigsApi + '/' + self.editForm.id, self.editForm).then((response) => {
            self.$message(response.data.msg)
            if (response.data.status == 1) {
              self.show_edit_modal = false
              self.get_dubbo_configs_list()
            }
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    get_dubbo_configs_list() {
      var self = this
      var data = {
        name:this.search,
      }
      this.$http.get(DubboConfigsApi,{params:data}).then((response) => {
        self.config_list = response.data.result
        // self.create_multi_graph()


      })
    },
    del_dubbo_config(id) {
      var self = this
      this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {

        self.$http.delete(DubboConfigsApi + '/' + id).then((response) => {
          self.$message(response.data.msg)
          if (response.data.status == 1) {
            self.get_dubbo_configs_list()
          }
        })
      })
    },
    create_echart_graph(row) {
      var chart = 'chart_'+row.id
      var self = this 
      var url = this.$http.get(DubboConfigsApi+'/'+row.id+'/stats').then((response)=>{
          var series = response.data.result.series  
          var x_data = response.data.result.x_data
          console.log('series',series)
          console.log('x_data',x_data)

          self[chart] = echarts.init(document.getElementById(''+row.id))
          this[chart].showLoading()
          var option = {
            // title: {
            //   text: row.name,
            //   align:'center',
            // },
            tooltip: {
              trigger: 'axis'
            },
            // legend: {
            //   data: ['邮件营销', '联盟广告', '视频广告', '直接访问', '搜索引擎']
            // },
            grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
            },
            // toolbox: {
            //   feature: {
            //     saveAsImage: {}
            //   }
            // },
            xAxis: {
              type: 'category',
              boundaryGap: false,
              // data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
              data:x_data,
            },
            yAxis: {
              type: 'value'
            },
            series: series,
            // [{
            //     name: '邮件营销',
            //     type: 'line',
            //     smooth: true,

            //     stack: '总量',
            //     data: ['', '' , 101, 134, 90, 230, 210]
            //   },
            //   {
            //     name: '联盟广告',
            //     smooth: true,
            //     type: 'line',
            //     stack: '总量',
            //     data: [220, 182, 191, 234, 290, 330, 310]
            //   },
            // ]
          };
          this[chart].setOption(option)
          this[chart].hideLoading()
          // myChart.setOption(option)
          // myChart.hideLoading()


      })

    },
    create_multi_echart_graph(){
      for (var n in this.config_list){
        this.create_echart_graph(this.config_list[n])
      }
    }

  },
  mounted() {
    this.get_dubbo_configs_list()

  },
  updated(){
    this.create_multi_echart_graph()
  }
}

</script>
