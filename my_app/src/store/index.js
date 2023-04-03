import { createStore } from 'vuex';

export default createStore({
    state: {
        isAuthenticated: false, // RMB CHANGE BACK TO FALSE AFTER TESTING
        user_details: {
        },
        username: null,
        markerId: null,
        foodPostId: null,
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