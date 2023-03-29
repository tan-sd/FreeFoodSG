import { createStore } from 'vuex';

export default createStore({
    state: {
        isAuthenticated: false, // RMB CHANGE BACK TO FALSE AFTER TESTING
        user_details: {
            // "address": "Singapore Management University",
            // "dietary_type": "na",
            // "email": "dancer@gmail.com",
            // "first_name": "Dancer",
            // "last_name": "Adam",
            // "latitude": 41.023472,
            // "longitude": -91.967133,
            // "number": "+6590229185",
            // "travel_appetite": "far",
            // "user_id": 2,
            // "username": "DA123"
        }
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