import { createRouter, createWebHistory } from "vue-router";
import Home from '../views/Home.vue';
import Login from '../views/LoginPage.vue';
import User from '../views/UserProfile.vue';
import Signup from '../views/SignUpPage.vue';
import Forum from '../views/Forum.vue';
import FoodForm from '../components/FoodForm.vue';
import store from '../store';

const routes = [
    {
        path: '/',
        name: 'MakanBoleh',
        component: Home
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/user',
        name: 'User Profile',
        component: User,
    },
    {
        path: '/signup',
        name: 'Sign Up',
        component: Signup
    },
    {
        path: '/forum',
        name: 'Forum',
        component: Forum
    },
    {
        path: '/foodform',
        name: 'FoodForm',
        components: FoodForm,
        meta: {
            needsAuth: true,
            showModal: false,
        }
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    document.title = to.name;
    if (to.meta.needsAuth) {
        if(store.getters.isAuthenticated) {
            next();
        } else {
            next('/login')
        }
    } else {
        next();
    }
});

export default router