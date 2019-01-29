<template>
  <div>
    <router-link :to="NodeCreatePage">
      <el-button style="margin:0 0 10px 0"> <i class="icon-plus"></i>&nbsp添加节点</el-button>
    </router-link>
    <div class="card">
      <div class="card-body">
        <data-tables :data="tableData">
          <el-table-column sortable prop="name" label="节点名称">
          </el-table-column>

          <el-table-column sortable prop="description" label="描述">
          </el-table-column>

          <el-table-column sortable prop="operatorNames" label="审核人">
          </el-table-column>
          <el-table-column sortable prop="step_type" label="审核方式">
            <template scope="scope">
               <el-tag type="primary" v-if="scope.row.step_type != 1">任一审核</el-tag>
               <el-tag type="warning" v-if="scope.row.step_type == 1">全部审核</el-tag>
            </template>
          </el-table-column>

           <el-table-column sortable prop="" label="是否执行">
            <template scope="scope">
               <el-tag type="danger" v-if="scope.row.exec_tag != 1">No</el-tag>
               <el-tag type="primary" v-if="scope.row.exec_tag == 1">Yes</el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="id" label="操作">
            <template scope="scope">
              <router-link :to="NodesPage+'/'+scope.row.id">
                <el-button type="text" size="small">
                  编辑
                </el-button>
              </router-link>
              <el-button type="text" size="small" @click="del_nodes(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </data-tables>
      </div>
    </div>
  </div>
</template>
<script>
import { NodeListApiUrl, NodeCreatePage, NodesPage } from '@/http/url'
export default {
  name: 'nodes',
  data() {
    return {
      tableData: [],
      NodesPage: NodesPage,
      NodeCreatePage: NodeCreatePage,
    }
  },
  methods: {
    get_nodes() {
      //获取环境列表数据
      var self = this
      self.$http.get(NodeListApiUrl).then((response) => {
        self.tableData = response.data.result
      })
    },
    del_nodes(id) {
      //删除环境
      var self = this
      this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {
        self.$http.delete(NodeListApiUrl + '/' + id).then((response) => {
          self.$message(response.data.msg)
          if (response.data.status == 1) {
            self.get_nodes()
          }
        })
      }).catch(() => {})
    }
  },
  mounted() {
    this.get_nodes()
  }
}

</script>
