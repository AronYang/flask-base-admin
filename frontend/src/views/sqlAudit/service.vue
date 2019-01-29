<template>
  <div>
    <router-link :to="flowCreatePage">
      <el-button style="margin:0 0 10px 0"> <i class="icon-plus"></i>&nbsp添加业务配置</el-button>
    </router-link>
    <div class="card">
      <div class="card-body">
        <data-tables :data="tableData">
          <el-table-column sortable prop="name" label="业务名">
          </el-table-column>
          <el-table-column sortable prop="description" label="描述">
          </el-table-column>
          <el-table-column prop="id" label="操作">
            <template scope="scope">
              <el-button type="text" size="small" @click="showFlowInfo(scope.row.id)">查看</el-button>
              <!-- <el-button type="text" size="small" @click="$router.push(flowCreatePage+'?copy='+scope.row.id)">复制</el-button> -->
              <el-button type="text" size="small" @click="$router.push(flowUpdatePage+scope.row.id)">编辑</el-button>
              <el-button type="text" size="small" @click="del_flow(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </data-tables>
      </div>
    </div>
  </div>
</template>
<script>
import { flowListApiUrl, flowCreatePage, flowUpdatePage } from '../../http/url'
export default {
  name: 'flow',
  data() {
    return {
      tableData: [],
      flowCreatePage: flowCreatePage,
      flowUpdatePage: flowUpdatePage,
    }
  },
  methods: {
    get_flows() {
      var self = this
      this.$http.get(flowListApiUrl).then(function(response) {
        self.tableData = response.data.result
        // console.log(response,'test')
      })
    },
    del_flow(id) {
      var self = this
      this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {
        this.$http.delete(flowListApiUrl + '/' + id).then(function(response) {
          self.$message(response.data.msg)
          if (response.data.status == 1) {
            self.get_flows()
          }
        })
      }).catch(() => {})
    },
    showFlowInfo(id){
      this.$message('暂时未做该功能')
    },
    action(action_name, id) {
      // 执行的动作，支持copy和check,用post方式提交
      var self = this
      this.$http.post(InstanceActionUrl, { name: action_name, id: id }).then(function(response) {
        self.$message(response.data.msg)
        if (response.data.status == 1) {
          self.get_flows()
        }
      })
    },
    envfilter(value, row) {
      return row.env === value
    },
    typefilter(value, row) {
      return row.type === value
    }
  },
  mounted() {
    this.get_flows()
  }
}

</script>
