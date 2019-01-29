import Vue from 'vue'
// import Router from 'vue-router'
import VueRouter from 'vue-router'
// Containers
import Full from '@/containers/Full'

// Views
import Dashboard from '@/views/Dashboard'

// // Views - Pages
import Login from '@/views/pages/Login'
import store from '../store'

import DubboTopology from '@/views/dubbo/topology/topology'
import DubboRouter from '@/views/dubbo/router/router'
import DubboConfigs from '@/views/dubbo/config/config'


Vue.use(VueRouter)


const routes = [{
    path: '/',
    name: '首页',
    component: Full,
    redirect: '/dubbo/topologies',
    children: [
      {
        path: '/dubbo',
        name: 'DUBBO管理',
        redirect:'/dubbo/topologies',
        component: { render(c) { return c('router-view') } },
        children:[
          {
            path: 'topologies',
            name: '拓扑',
            component: DubboTopology,
          },
          {
            path: 'routers',
            name: '路由规则',
            component: DubboRouter,
          },
          {
            path:'configs',
            name:'配置',
            component:DubboConfigs,
          },

        ]
      },

    ]
  },
  {
    path: '/pages/login',
    name: '登陆',
    component: Login,
    children:[]
  },
];


const router = new VueRouter({
  mode: 'hash', // Demo is living in GitHub.io, so required!
  linkActiveClass: 'open active',
  scrollBehavior: () => ({ y: 0 }),
  routes
});

// const whiteList = ['/login']
// 路由token判断
router.beforeEach((to, from, next) => {
  if (localStorage.token) {
    // console.log('befor each')
    next();

  } else {
    console.log('redirect to login.')
    if (to.path == '/pages/login') {
      next()
    } else {
      next({
        path: '/pages/login',
        query: { redirect: to.fullPath }
      })
    }
  }
})

export default router;

// export default new Router({
//   mode: 'hash', // Demo is living in GitHub.io, so required!
//   linkActiveClass: 'open active',
//   scrollBehavior: () => ({ y: 0 }),
//   routes: [
//     {
//       path: '/',
//       redirect: '/dashboard',
//       name: '首页',
//       component: Full,
//       children: [
//         {
//           path: 'dashboard',
//           name: 'Dashboard',
//           component: Dashboard
//         },
//         {
//           path: 'charts',
//           name: 'Charts',
//           component: Charts
//         },
//         {
//           path: 'widgets',
//           name: 'Widgets',
//           component: Widgets
//         },
//         {
//           path: 'components',
//           redirect: '/components/buttons',
//           name: 'Components',
//           component: {
//             render (c) { return c('router-view') }
//           },
//           children: [
//             {
//               path: 'buttons',
//               name: 'Buttons',
//               component: Buttons
//             },
//             {
//               path: 'social-buttons',
//               name: 'Social Buttons',
//               component: SocialButtons
//             },
//             {
//               path: 'cards',
//               name: 'Cards',
//               component: Cards
//             },
//             {
//               path: 'forms',
//               name: 'Forms',
//               component: Forms
//             },
//             {
//               path: 'modals',
//               name: 'Modals',
//               component: Modals
//             },
//             {
//               path: 'switches',
//               name: 'Switches',
//               component: Switches
//             },
//             {
//               path: 'tables',
//               name: 'Tables',
//               component: Tables
//             }
//           ]
//         },
//         {
//           path: 'icons',
//           redirect: '/icons/font-awesome',
//           name: 'Icons',
//           component: {
//             render (c) { return c('router-view') }
//           },
//           children: [
//             {
//               path: 'font-awesome',
//               name: 'Font Awesome',
//               component: FontAwesome
//             },
//             {
//               path: 'simple-line-icons',
//               name: 'Simple Line Icons',
//               component: SimpleLineIcons
//             }
//           ]
//         }
//       ]
//     },
//     {
//       path: '/pages',
//       redirect: '/pages/p404',
//       name: 'Pages',
//       component: {
//         render (c) { return c('router-view') }
//       },
//       children: [
//         {
//           path: '404',
//           name: 'Page404',
//           component: Page404
//         },
//         {
//           path: '500',
//           name: 'Page500',
//           component: Page500
//         },
//         {
//           path: 'login',
//           name: 'Login',
//           component: Login
//         },
//         {
//           path: 'register',
//           name: 'Register',
//           component: Register
//         }
//       ]
//     }
//   ]
// })
