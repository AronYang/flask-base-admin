<template>
  <div>
    <router-link :to="InstanceCreatePage">
      <el-button style="margin:0 0 10px 0"> <i class="icon-plus"></i>&nbsp添加实例</el-button>
    </router-link>
    <div class="card">
      <div class="card-body">
        <data-tables :data="tableData">
          <el-table-column sortable prop="ip" label="IP" width="150">
          </el-table-column>
          <el-table-column sortable prop="port" label="端口" width="80">
          </el-table-column>
          <el-table-column sortable prop="enviromentName" label="环境" width="150">
          </el-table-column>
          <el-table-column sortable prop="type" label="类型" :filters="[{ text: 'MySQL', value: 'MySQL' }, { text: 'Oracle', value: 'Oracle' }]" :filter-method="typefilter" width="120">
          </el-table-column>

          <el-table-column prop="dbNames" label="数据库" sortable>  
            <template scope="scope">
                <el-tooltip class="item" effect="dark" :content="scope.row.dbNames" placement="top-start" >
                  <div style="white-space:nowrap;overflow:hidden">{{scope.row.dbNames}}</div>
                </el-tooltip>
            </template>
          </el-table-column>
<!-- 
          <el-table-column prop="remark" label="描述" sortable>
          </el-table-column> -->

          <el-table-column prop="check_db" label="数据库检测" sortable >
            <template scope="scope">
              <span class="text-success" v-if="scope.row.check_db==1">已检测</span>
              <span class="text-danger" v-if="scope.row.check_db==0">检测失败</span>
            </template>
          </el-table-column>
          <el-table-column prop="id" label="操作" >
            <template scope="scope">
              <el-button type="text" size="small" :loading="loadingId == scope.row.id" @click="action(scope.row.id)">检测</el-button>
              <router-link :to="InstanceCreatePage+'?copy='+scope.row.id">
                <el-button type="text" size="small">
                  &nbsp复制&nbsp
                </el-button>
              </router-link>
              <router-link :to="InstancesPage+'/' + scope.row.id">
                <el-button type="text" size="small">
                  编辑&nbsp
                </el-button>
              </router-link>
              <el-button type="text" size="small" @click="del_instance(scope.row.id)">删除</el-button>
            </template>
          </el-table-column>
        </data-tables>
      </div>
    </div>
  </div>
</template>
<script>
import { InstanceListApiUrl, InstanceCreatePage, InstancesPage, InstanceCheckApiUrl } from '@/http/url'
export default {
  name: 'config',
  data() {
    return {
      tableData: [],
      InstanceCreatePage: InstanceCreatePage,
      InstancesPage: InstancesPage,
      loadingId: '',
    }
  },
  methods: {
    get_instances() {
      var self = this
      this.$http.get(InstanceListApiUrl).then(function(response) {
        self.tableData = response.data.result
      })
    },
    get_page() {
      console.log(this.paginationDef.currentPage, this.paginationDef.pageSize)
    },
    del_instance(id) {
      var self = this
      this.$confirm('此操作将永久删除该记录, 是否继续?', '警告').then(() => {
        this.$http.delete(InstanceListApiUrl+ '/' + id).then(function(response) {
          self.$message(response.data.msg)
          if (response.data.status == 1) {
            self.get_instances()

          }
        })
      }).catch(() => {})
    },
    action(id) {
      // 执行的动作，支持check,用put方式提交
      var self = this
      self.loadingId = id
      this.$http.put(InstanceCheckApiUrl + '/' + id).then(function(response) {
        self.loadingId = null
        if (response.data.status == 1) {
          self.$message(response.data.msg)
          self.get_instances()
        } else {
          self.$message(response.data.msg)
        }
      }).catch(() => {
        self.loadingId = null
        self.$messaeg('请求超时')
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
    this.get_instances()
  }
}

</script>
