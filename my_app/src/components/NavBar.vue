<template>
    <nav class="navbar navbar-expand-lg bg-dark navbar-dark">
        <div class="container-fluid">
            <router-link to="/" class="navbar-brand">
                <img src="../assets/images/logos/small_logos/MakanBoleh_logo_long_light_small.png" alt="MakanBoleh Logo" width="165">
            </router-link>

            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span><font-awesome-icon icon="fa-solid fa-burger" /></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link to="/login" class="nav-link">Login</router-link>
                    </li>

                    <li class="nav-item" v-if="!isLoggedIn">
                        <router-link to="/user" class="nav-link">User Profile</router-link>
                    </li>
                </ul>

                <div class="d-flex justify-content-center button-container mx-auto mx-lg-0">
                    <FoodForm class="btn btn-main"/>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
import FoodForm from '../components/FoodForm.vue';

    export default{
        components: {
            FoodForm
        },
        props: [],

        data() {
            return {
                isLoggedIn: true
            }
        }
    }
</script>


<style scoped>
    .button-container{
        width: 200px
    }
</style>