import { createStore } from 'vuex';

export default createStore({
    state: {
        isAuthenticated: false
    },
    mutations: {

    },
    actions: {

    },
    getters: {
        isAuthenticated: state => {
            return state.isAuthenticated
        }
    },
    modules: {

    }
})