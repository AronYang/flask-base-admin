/**
 * Created by superman on 17/2/16.
 * http配置
 */

import axios from 'axios'
import router from '../router'
import store from '../store'
import qs from 'qs'

// axios 配置
axios.defaults.timeout = 30000; //超时30s
// axios.defaults.baseURL = 'http://172.20.99.44:8000';
axios.defaults.responseType = 'json'

// http request 拦截器
axios.interceptors.request.use(
  config => {
    if (localStorage.token) {
      // 在每个请求中都添加上token            
      config.auth = {
        username: localStorage.token,
        password: 'unset'
      }
    }

    return config;
  },
  err => {
    console.log('request error. ' + err)
    return Promise.reject(err);
  });

// http response 拦截器
axios.interceptors.response.use(
  response => {
    // response.data = eval(response.data)
    // var response = qs.parse(response)
    return response;
  },
  error => {
    console.log('response error')

    console.log(error)
    if (error.response) {
      switch (error.response.status) {
        case 401:
          console.log('return 401')
          // 401 清除token信息并跳转到登录页面
          // store.commit(types.LOGOUT);
          router.replace({
            path: '/pages/login',
            // query: {redirect: router.currentRoute.fullPath}
          })
        case 402:
          router.replace({
            path: '/pages/login',
            // query: {redirect: router.currentRoute.fullPath}
          })
      }
    }
    // console.log(JSON.stringify(error));//console : Error: Request failed with status code 402
    return Promise.reject(error.response.data)
  });

export default axios;
