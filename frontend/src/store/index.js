/**
 * Created by superman on 17/2/16.
 */
import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)
export default new Vuex.Store({
    state: {
        username:null,
        token: null,
    },
    mutations: {
        login: (state, data) => {
            state.username = data.username
            state.token = data.token
            localStorage.token = data.token
            localStorage.username = data.username
        },
        logout: (state) => {
            state.username=null
            state.token = null
            localStorage.removeItem('token');
            localStorage.removeItem('username');
            state.token = null
        },
    }
})


