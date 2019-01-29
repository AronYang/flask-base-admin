<template>
  <div class="card">
    <div class="card-body">
      <div style="margin-bottom:15px;">
        <el-select v-model="query.dubbo_id" @change.passive="create_all_node_chart" style="width:120px;">
          <el-option :value='config.id' :key="config.id" v-for="config in config_list" :label="config.name"></el-option>
        </el-select>
        <el-select v-model="query.category" style="width:120px;">
          <el-option value='' label="--节点类型--"></el-option>
          <el-option v-for="category in categories" :key="category.name" :value='category.name' :label="category.name"></el-option>
        </el-select>
        <el-select v-model="query.deep" style="width:120px;">
          <el-option value='0' label="深度(0级)">深度(0级)</el-option>
          <el-option value='1' label="深度(1级)">深度(1级)</el-option>
          <!--           <el-option value='2' label="深度(2级)">深度(2级)</el-option>
          <el-option value='3' label="深度(3级)">深度(3级)</el-option>
 -->
        </el-select>
        <el-input class="inline-input" style="width:220px" @keyup.enter.native="create_all_node_chart" v-model="query.name" placeholder="请输入节点名称"></el-input>
        <el-button @click.passive="create_all_node_chart()">搜索</el-button>
        <div style="float:right">
          <el-tag v-for="(v,k) in stat_node" :style="{'color':v.color}">{{k}}:{{v.value}}</el-tag>
          <!--           <el-tag >application:{{stat_node.application}}</el-tag>
          <el-tag type="success">service:{{stat_node.service}}</el-tag>
          <el-tag type="success">provider:{{stat_node.provider}}</el-tag>
          <el-tag type="success">consumer:{{stat_node.consumer}}</el-tag>
 -->
        </div>
      </div>
      <div v-bind:style="{'height':autoHeight+'px','width':autoWidth+'px'}">
        <div id="operation" v-bind:style="{'height':autoHeight+'px','width':autoWidth+'px'}">
        </div>
      </div>
    </div>
    <div id="menu" style="display:none">
      <el-dropdown-item><a href="javascript:;" @click="get_node_info">预览</a></el-dropdown-item>
      <el-dropdown-item><a href="javascript:;" @click="deny_allow_host">禁止/允许</a></el-dropdown-item>
    </div>

    <el-dialog :title="contextmenu_data.name" :visible.sync="show_node_info_modal" width="70%" top="0%" close-on-press-escape close-on-click-modal>
      <el-row>
        <el-col :span="12">          
          <span v-if="contextmenu_data.category=='service'">Fullname: &nbsp{{contextmenu_data.oldname}}</span>
          <div v-for="(v,k) in nodesData">
            <strong><hr>{{k}}: 
              <span ><a href="javascript:;">{{v.values.length}}</a></span><br/>
            </strong> 
            <div >
              <span v-for="i in v.values" >{{i}}<br/></span>
            </div>
          </div>
        </el-col>
        <el-col :span="12">
          <div style="float:right">
            <el-tag v-for="(v,k) in nodesData" :style="{'color':v.color}">
              {{k}} {{v.values.length}}
            </el-tag>
          </div>

          <div id="near_node_chart" style="height:500px; width:500px;">
          </div>
        </el-col>
      </el-row>
    </el-dialog>
<!-- 
    <el-dialog title="新增路由" :visible.sync="show_node_info_modal" width="70%" top="0%" close-on-press-escape close-on-click-modal>
      <el-row>
        <el-col :span="12">          
          <span v-if="contextmenu_data.category=='service'">Fullname: &nbsp{{contextmenu_data.oldname}}</span>
          <div v-for="(v,k) in nodesData">
            <strong><hr>{{k}}:<br/></strong> 
            <span v-for="i in v.values">{{i}}<br/></span>
          </div>
        </el-col>
        <el-col :span="12">
          <div style="float:right">
            <el-tag v-for="(v,k) in nodesData" :style="{'color':v.color}">
              {{k}} {{v.values.length}}
            </el-tag>
          </div>

          <div id="near_node_chart" style="height:500px; width:500px;">
          </div>
        </el-col>
      </el-row>
    </el-dialog> -->


  </div>
</template>
<style>
/*.el-dialog {
  right: 0;
  top: 0px;
  transform: initial;
  left: initial;
}*/

.list-group {
  display: none;
  padding: 0
}

.list-group-item {
  position: relative;
  display: block;
  padding: 0.25rem 0.75rem;
  margin-bottom: -1px;
  background-color: #fff;
  border: 1px solid rgba(0, 0, 0, 0.125);
}

</style>
<script>
import echarts from 'echarts'
// var echarts = require('echarts');

import { DubboTopologyApi, DubboConfigsApi } from '@/http/url'

export default {
  name: 'operation',
  data() {
    return {
      nodes: [], // 图中所有的节点列表
      links: [], // 图中展示的链接关系
      state2: '',
      config_list: [],
      categories: [
        { name: 'application', itemStyle: { color: '#B8860B' } },
        { name: 'service', itemStyle: { color: '#55AA00' } },
        { name: 'provider', itemStyle: { color: '#6495ED' } },
        { name: 'consumer', itemStyle: { color: '#0088A8' } },
      ], // 图中展示的分类
      myChart: {}, // 图表实例
      all_nodes: [], // 所有节点的列表，在搜索框里显示
      near_nodes: {}, // 节点相关的列表，在表中查看时显示
      show_service_detail: false,
      contextmenu_data: {}, // 当前选中的节点名称
      show_node_info_modal: false,
      query: {
        // filter_tag: '',  //
        name: '', //搜索的节点名称
        category: 'application', //搜索节点分类  
        deep: '0', // 查询深度
        dubbo_id: '', //dubbo zk集群id
      }
    }
  },
  computed: {
    stat_node() {
      var categoryColorDict = {}
      for (var n in this.categories) {
        categoryColorDict[this.categories[n].name] = this.categories[n].itemStyle.color
      }

      var d = {}
      for (var n in this.nodes) {
        var node = this.nodes[n]
        if (node.category in d) {
          d[node.category].value += 1
        } else {
          d[node.category] = { value: 1, color: categoryColorDict[node.category] }
        }
      }
      return d
    },
    nodesData() {
      var categoryColorDict = {}
      for (var n in this.categories) {
        categoryColorDict[this.categories[n].name] = this.categories[n].itemStyle.color
      }

      var data = {}
      for (var n in this.near_nodes.nodes) {
        var node = this.near_nodes.nodes[n]
        if(node.category == 'service'){
          node.name = node.oldname  
        }

        if (node.category in data) {
          data[node.category].values.push(node.name)
        } else {
          data[node.category] = { 
            values: [node.name], 
            color: categoryColorDict[node.category], 
            show:0 }
        }
      }
      return data
    },
    // compute_near_node_consumers() {
    //   var consumer_ips = []
    //   for (var n in this.near_nodes.nodes) {
    //     if (this.near_nodes.nodes[n].category == 'service') {
    //       var ips = this.near_nodes.nodes[n].consumer_ips
    //       for (var i in ips) {
    //         consumer_ips.push(ips[i])
    //       }
    //     }
    //   }
    //   ips = Array.from(new Set(consumer_ips)); //去重
    //   return ips
    // },
    autoHeight() {
      var height = document.documentElement.clientHeight;
      console.log(height, 'height')
      return height - 200
    },
    autoWidth() {
      var width = document.documentElement.clientWidth;
      console.log(width, 'width')
      return width - 200
    },

  },
  methods: {
    query_index() {
      var index = 1
      var self = this
      for (var n in self.nodes) {
        if (self.nodes[n].name == self.query.name) {
          index = n
          break
        }
      }
      return index
    },
    relate_echart() {
      var myChart = echarts.init(document.getElementById('operation'))
      this.myChart = myChart
      var self = this

      this.myChart.showLoading()
      self.nodes = []
      self.links = []
      this.$http.get(DubboTopologyApi, { params: self.query }).then((response) => {
        self.nodes = response.data.result.nodes

        if (self.nodes.length == 0) {
          self.$message('未搜索到数据... 请重新搜索')
        }
        self.links = response.data.result.links



        console.log('nodes:', self.nodes)
        console.log('links:', self.links)
        console.log('categories', self.categories)

        self.myChart.hideLoading()


        for (var n in self.nodes) {
          if (self.nodes[n].category == self.query.category) {
            self.nodes[n].symbolSize = 30
            self.nodes[n].label = {
              normal: {
                show: true
              }
            }
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
          // polar:{
          //         tooltip: {
          //             formatter: function (param) {
          //                 param = param[0];
          //                 console.log(param,'param')
          //                 return [
          //                     'Date: ' + param.name + '<hr size=1 style="margin: 3px 0">',
          //                     'Open: ' + param.category + '<br/>',
          //                 ].join('');
          //             }
          //         }          
          // },
          // animation: false,
          animationDuration: 500,
          animationEasingUpdate: 'quinticInOut',

          series: [{
            name: 'dubbo',
            type: 'graph',
            layout: 'force',
            data: self.nodes,
            links: self.links,
            categories: self.categories,
            useWorker: false,
            minRadius: 30,
            maxRadius: 100,
            gravity: 1.1,
            scaling: 1.1,
            ribbonType: false,
            itemStyle: {
              normal: {
                label: {
                  // show: true,
                  textStyle: {
                    color: '#333'
                  }
                },
              },
              emphasis: {
                label: {
                  show: false
                  // textStyle: null      // 默认使用全局文本样式，详见TEXTSTYLE
                },
                nodeStyle: {
                  //r: 30
                },
                linkStyle: {}
              }
            },
            roam: true,
            // legendHoverLink:true,
            focusNodeAdjacency: true, // 选中高亮周周的线

            label: {
              normal: {
                // position: 'right',
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
            // edgeLabel: { // 显示方向线的值
            //   normal: {
            //     show: true,
            //     position: 'middle',
            //     formatter: function(param) { return param.data.category },
            //     textStyle: {
            //       fontSize: 8
            //     },
            //     verticalAlign: 'bottom'
            //   }
            // },
            // tooltip: {
            //   trigger:'axis',
            //   position: [10, 10],  
            //   formatter: function(param) {
            //     if ('target' in param.data) {
            //       return [param.data.source + ' > ' + param.data.target]
            //     }
            //     return [
            //       'name: ' + param.data.id + '<hr size=1 style="margin: 3px 0">',
            //       'category: ' + param.data.category + '<br/>',
            //     ].join('');
            //   }
            // }
          }]
        }
        self.myChart.setOption(option)
        // self.myChart.on('dblclick', function(params) {
        //   // 控制台打印数据的名称
        //   var name = params.data.name
        //   if (name != undefined) {
        //     self.query.name = name
        //   }
        //   console.log(params, 'double', name)
        // })

        // 去除图形中默认的鼠标事件
        // document.getElementById("operation").oncontextmenu=function(){return false}

        // document.getElementById("operation").onclick=function(){
        //    var menu  = document.getElementById("menu");
        //    menu.style.display = "none";
        //    console.log(' on click.  close ')
        // }

        // self.myChart.on('click',function(params){
        //    self.contextmenu_data = params.data
        //    var menu  = document.getElementById("menu");
        //    menu.style.display = "block";
        // })

        // window.onresize = self.myChart.resize()
        // self.highlight_echart()
      })
    },
    create_chart(id, nodes, links, show_all_node) {
      var self = this
      var myChart = echarts.init(document.getElementById(id))
      this[id] = myChart
      var self = this
      // self.nodes = nodes
      // self.links = links
      self[id].showLoading()
      if (nodes.length == 0) {
        self.$message('未搜索到数据... 请重新搜索')
      }

      self[id].hideLoading()

      for (var n in nodes) {
        if (nodes[n].category == self.query.category) {
          nodes[n].symbolSize = 30
          nodes[n].label = {
            normal: {
              show: true
            }
          }
        } else {

          if (nodes[n].category == 'application') {
            if (self.query.category == "") {
              nodes[n].symbolSize = 30
              nodes[n].label = {
                normal: {
                  show: true
                }
              }
            } else {
              nodes[n].symbolSize = 30
            }
          } else if (nodes[n].category == 'service') {
            nodes[n].symbolSize = 20
            // self.nodes[n].itemStyle = {color:'#99FF99'}
          } else if (nodes[n].category == 'provider') {
            nodes[n].symbolSize = 15
            // self.nodes[n].itemStyle = {color:'#CCCCFF'}
          } else {
            nodes[n].symbolSize = 15
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
        // legend: [{
        //   // selectedMode: 'single',
        //   // align:'right',
        //   left: 'right',
        //   data: self.categories.map(function(a) {
        //     return a.name
        //   })
        // }],
        animationDuration: 500,
        animationEasingUpdate: 'quinticInOut',

        series: [{
          name: 'dubbo',
          type: 'graph',
          layout: 'force',
          data: nodes,
          links: links,
          categories: self.categories,
          useWorker: false,
          minRadius: 30,
          maxRadius: 100,
          gravity: 1.1,
          scaling: 1.1,
          ribbonType: false,
          itemStyle: {
            normal: {
              label: {
                show: true,
                textStyle: {
                  color: '#333'
                }
              },
            },
          },
          roam: true,
          // legendHoverLink:true,
          focusNodeAdjacency: true, // 选中高亮周周的线

          label: {
            normal: {
              // position: 'right',
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

        }]
      }
      self[id].setOption(option)
      // 新加上鼠标划入事件


      self[id].on('click', function(params) {
        console.log('右键事件')
        var event = params.event
        var menu = document.getElementById('menu')
        menu.style.left = event.offsetX + 230 + 'px'
        menu.style.top = event.offsetY + 150 + 'px'
        menu.style.display = 'block'
        menu.style.position = 'fixed'
        menu.style.opacity = '0.7'
        self.contextmenu_data = params.data
        self.click_count = 1

        function abc() {
          menu.style.display = 'none'
        }
        // setTimeout(abc, 2000)
        console.log(params)
      })

      // 当鼠标在图形中其他位置点击的时候，隐藏菜单栏。  
      document.getElementById("operation").onclick = function() {
        var menu = document.getElementById('menu')

        if (self.click_count == 1) {
          self.click_count += 1
        } else {
          menu.style.display = "none"
        }
        console.log('chart ....', menu.style.display)

      }
      self[id].on('dblclick', function(params) {
        // 控制台打印数据的名称
        var name = params.data.name
        var oldname = params.data.oldname  
        if (oldname != undefined){
          name = oldname
        }
        if (name != undefined) {
          self.query.name = name
          self.query.deep = '1'
          self.query.category = params.data.category
          self.create_all_node_chart()
        }
        console.log(params, 'double', name)
      })

    },
    show_modal_function(params) {

    },
    create_all_node_chart() {
      var self = this
      var id = 'operation'
      this.$http.get(DubboTopologyApi, { params: self.query }).then((response) => {
        var nodes = response.data.result.nodes
        var links = response.data.result.links
        self.nodes = nodes  
        self.links = links
        self.create_chart(id, nodes, links)
      })
    },
    // create_near_info_chart_in_modal(){
    //   var self = this
    //   var id = 'operation'
    //   this.$http.get(DubboTopologyApi, { params: self.query }).then((response) => {
    //     var nodes = response.data.result.nodes  
    //     var links = response.data.result.links  
    //     self.create_chart(id,nodes,links)
    //   })

    // },

    // highlight_echart() {
    //   var self = this
    //   this.myChart.dispatchAction({
    //     type: 'focusNodeAdjacency',

    //     // 使用 seriesId 或 seriesIndex 或 seriesName 来定位 series.
    //     // seriesId: '10.4.8.3',
    //     // seriesIndex: 0,
    //     // seriesName: '10.4.8.3',

    //     // 使用 dataIndex 来定位节点。
    //     dataIndex: self.query_index()
    //   })
    // },
    // get_nodes_list() {
    //   var self = this
    //   this.$http.get(DubboTopologyApi).then((response) => {
    //     self.all_nodes = response.data.result.nodes
    //     console.log(self.all_nodes)
    //     // 默认选中第一个
    //   })
    // },
    get_node_info() {
      var self = this
      this.near_nodes = {}
      this.show_node_info_modal = true
      console.log(self.contextmenu_data)

      var id = self.contextmenu_data._id
      var chart_id = 'near_node_chart'
      this.$http.get(DubboTopologyApi + '/' + id).then((response) => {
        self.near_nodes = response.data.result
        var nodes = response.data.result.nodes
        var links = response.data.result.links
        console.log('near nodes...', self.near_nodes)
        self.create_chart(chart_id, nodes, links)

      })
    },
    get_dubbo_config_list() {
      var self = this
      this.$http.get(DubboConfigsApi).then((response) => {
        self.config_list = response.data.result
        self.query.dubbo_id = self.config_list[0].id
        self.create_all_node_chart()
      })
    },
    deny_allow_host(){
      this.$message.error('该功能未开放')
    }

  },
  mounted() {
    // this.init_echart()
    this.get_dubbo_config_list()
    // this.relate_echart()
  }

}

</script>
