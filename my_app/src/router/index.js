import { createRouter, createWebHistory } from "vue-router";
import Home from '../views/Home.vue'
import Login from '../views/LoginPage.vue'
import User from '../views/UserProfile.vue'
import Signup from '../views/SignUpPage.vue'
import Forum from '../views/Forum.vue'

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
        meta: {
            requiresAuth: true
        }
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
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    document.title = to.name;
    next();
});

export default router