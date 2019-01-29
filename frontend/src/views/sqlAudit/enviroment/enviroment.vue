<template>
  <div>
    <router-link :to="EnviromentCreatePage">
      <el-button style="margin:0 0 10px 0"> <i class="icon-plus"></i>&nbsp添加环境</el-button>
    </router-link>
    <div class="card">
      <div class="card-body">
        <data-tables :data="tableData">
          <el-table-column sortable prop="name" label="环境">
          </el-table-column>
          <el-table-column sortable prop="describe" label="描述">
          </el-table-column>
          <el-table-column prop="id" label="操作">
            <template scope="scope">
              <router-link :to="EnviromentsPage+'/'+scope.row.id">
                <el-button type="text" size="small">
                  编辑&nbsp
                </el-button>
              </router-link>
              <el-button type="text" size="small" @click="del_enviroments(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </data-tables>
      </div>
    </div>
  </div>
</template>
<script>
import { EnviromentListApiUrl, EnviromentCreatePage, EnviromentsPage } from '@/http/url'
export default {
  name: 'enviroments',
  data() {
    return {
      tableData: [],
      EnviromentsPage: EnviromentsPage,
      EnviromentCreatePage: EnviromentCreatePage,
    }
  },
  methods: {
    get_enviroments() {
      //获取环境列表数据
      var self = this
      self.$http.get(EnviromentListApiUrl).then((response) => {
        self.tableData = response.data.result
      })
    },
    del_enviroments(id) {
      //删除环境
      var self = this
      this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {
        self.$http.delete(EnviromentListApiUrl + '/' + id).then((response) => {
          self.$message(response.data.msg)
          if (response.data.status == 1) {
            self.get_enviroments()
          }
        })
      }).catch(() => {})
    }
  },
  mounted() {
    this.get_enviroments()
  }
}

</script>
