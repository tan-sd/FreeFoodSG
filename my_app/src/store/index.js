// import Vue from 'vue'
// import Vuex from 'vuex'
// import { createStore } from 'vuex';
// import VuexPersistence from "vuex-persist";

// // const vuexLocal = new VuexPersistence({
// //   storage: window.localStorage,
// // });

// Vue.use(Vuex)

// export default createStore({
//     state: {
//         isAuthenticated: false, // RMB CHANGE BACK TO FALSE AFTER TESTING
//         user_details: {
//         },
//         username: null,
//         markerId: null,
//         foodPostId: null,
//         user_food: [],
//     },
//     mutations: {

//     },
//     actions: {

//     },
//     getters: {
//         isAuthenticated: state => {
//             return state.isAuthenticated
//         }
//     },
//     modules: {

//     },
//     plugins: [new VuexPersistence().plugin]
// });

// import Vue from 'vue'
// import Vuex, { Payload, Store } from 'vuex'
// import VuexPersistence from 'vuex-persist'
// import Cookies from 'js-cookie'
// import { module as userModule, UserState } from './user'
// import navModule, { NavigationState } from './navigation'
 
// export interface State {
//   user: UserState
//   navigation: NavigationState
// }
 
// Vue.use(Vuex)
 
// const vuexCookie = new VuexPersistence<State, Payload>({
//   restoreState: (key, storage) => Cookies.getJSON(key),
//   saveState: (key, state, storage) =>
//     Cookies.set(key, state, {
//       expires: 3
//     }),
//   modules: ['user'], //only save user module
//   filter: (mutation) => mutation.type == 'logIn' || mutation.type == 'logOut'
// })
// const vuexLocal = new VuexPersistence<State, Payload>({
//   storage: window.localStorage,
//   reducer: (state) => ({ navigation: state.navigation }), //only save navigation module
//   filter: (mutation) => mutation.type == 'addNavItem'
// })
 
// const store = new Vuex.Store<State>({
//   modules: {
//     user: userModule,
//     navigation: navModule
//   },
//   plugins: [vuexCookie.plugin, vuexLocal.plugin]
// })
 
// export default store

// import Vue from 'vue'
// import Vuex from 'vuex'
// import VuexPersistence from 'vuex-persist'

// Vue.use(Vuex)

// Define your store modules
// const counterModule = {
//   namespaced: true,
//   state: {
//     count: 0
//   },
//   mutations: {
//     increment(state) {
//       state.count++
//     }
//   }
// }

// const userModule = {
//   namespaced: true,
//   state: {
//         isAuthenticated: false, // RMB CHANGE BACK TO FALSE AFTER TESTING
//         user_details: {
//         },
//         username: null,
//         markerId: null,
//         foodPostId: null,
//         user_food: [],
//     },
//   mutations: {
//     setName(state, newName) {
//       state.name = newName
//     },
//     setEmail(state, newEmail) {
//       state.email = newEmail
//     }
//   }
// }

// // Create a Vuex store
// const store = new Vuex.Store({
//   modules: {
//     counter: counterModule,
//     user: userModule
//   },
//   plugins: [
//     // Create a new instance of VuexPersistence to save the entire store state to localStorage
//     new VuexPersistence({
//       storage: window.localStorage
//     }).plugin
//   ]
// })

// // Use the store in your components
// new Vue({
//   el: '#app',
//   store,
//   computed: {
//     count() {
//       return this.$store.state.counter.count
//     },
//     name() {
//       return this.$store.state.user.name
//     },
//     email() {
//       return this.$store.state.user.email
//     }
//   },
//   methods: {
//     increment() {
//       this.$store.commit('counter/increment')
//     },
//     setName(newName) {
//       this.$store.commit('user/setName', newName)
//     },
//     setEmail(newEmail) {
//       this.$store.commit('user/setEmail', newEmail)
//     }
//   }
// })

// import Vue from 'vue'
// import Vuex from 'vuex'

// Vue.use(Vuex)

// const store = new Vuex.Store({
//   state: {
//     isAuthenticated: false, // RMB CHANGE BACK TO FALSE AFTER TESTING
//         user_details: {
//         },
//         username: null,
//         markerId: null,
//         foodPostId: null,
//         user_food: [],
//   },
//   mutations: {
//     increment(state) {
//       state.count++
//     },
//     decrement(state) {
//       state.count--
//     }
//   },
//   actions: {
//     asyncIncrement(context) {
//       setTimeout(() => {
//         context.commit('increment')
//       }, 1000)
//     }
//   },
//   getters: {
//     doubleCount(state) {
//       return state.count * 2
//     }
//   }
// })

// export default store

import {createStore} from 'vuex'
import VuexPersistence from "vuex-persist";

const storage = createStore({
	state: {
		isAuthenticated: false,
        user_details: {},
        username: null,
        markerId: null,
        foodPostId: null,
        user_food: [],
	}, 
	plugins: [
        new VuexPersistence({
            storage: window.localStorage
        }).plugin
    // createPersistedState({
    //   storage: {
    //     getItem: (key) => ls.get(key),
    //     setItem: (key, value) => ls.set(key, value),
    //     removeItem: (key) => ls.remove(key),
    //   },
    // }),
  ],
	mutations:{
		setAuthenticated(state, value)
        {
            state.isAuthenticated = value;
        },
        setUsername(state, username)
        {
            state.username = username
        },
        logout(state)
        {
            this.$router.push('/');
            state.isAuthenticated = false;
            localStorage.removeItem('user_details');
            state.username = '';
        }
	}
})

export default storage