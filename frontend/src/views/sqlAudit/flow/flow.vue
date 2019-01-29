<template>
  <div>
    <router-link :to="FlowCreatePage">
      <el-button style="margin:0 0 10px 0"> <i class="icon-plus"></i>&nbsp添加流程</el-button>
    </router-link>
    <div class="card">
      <div class="card-body">
        <data-tables :data="tableData">
          <el-table-column sortable prop="name" label="名称">
          </el-table-column>
          <el-table-column sortable prop="description" label="描述">
          </el-table-column>
          <el-table-column prop="id" label="操作">
            <template scope="scope">
              <router-link :to="FlowsPage+'/'+scope.row.id">
                <el-button type="text" size="small">
                  编辑
                </el-button>
              </router-link>
              <el-button type="text" size="small" @click="del_flows(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </data-tables>
      </div>
    </div>
  </div>
</template>
<script>
import { FlowListApiUrl, FlowCreatePage, FlowsPage } from '@/http/url'
export default {
  name: 'nodes',
  data() {
    return {
      tableData: [],
      FlowsPage: FlowsPage,
      FlowCreatePage: FlowCreatePage,
    }
  },
  methods: {
    get_flows() {
      //获取环境列表数据
      var self = this
      self.$http.get(FlowListApiUrl).then((response) => {
        self.tableData = response.data.result
      })
    },
    del_flows(id) {
      //删除环境
      var self = this
      this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {
        self.$http.delete(FlowListApiUrl + '/' + id).then((response) => {
          self.$alert(response.data.msg)
          if (response.data.status == 1) {
            self.get_flows()
          }
        })
      }).catch(() => {})
    }
  },
  mounted() {
    this.get_flows()
  }
}

</script>
