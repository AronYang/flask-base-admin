export default {
  items: [
    // {
    //   name: 'DUBBO管理',
    //   url: '/service/operations',
    //   icon: 'icon-speedometer',
    //   badge: {
    //     variant: 'primary',
    //     // text: 'NEW'
    //   }
    // },
    {
      name: 'DUBBO管理',
      url: '/dubbo',
      icon: 'icon-note',
      children: [
        {
          name: '拓扑',
          url: '/dubbo/topologies',
          icon: 'icon-arrow-right'
        },
        {
          name: '路由规则',
          url: '/dubbo/routers',
          icon: 'icon-arrow-right'
        },
        {
          name: '配置',
          url: '/dubbo/configs',
          icon: 'icon-arrow-right'
        },

      ]
    },


  ]
}
