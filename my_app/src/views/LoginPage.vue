<template>
    <div class="container-fluid bg-dark text-light" id="login-body">
        <img src="../assets/images/logos/large_logos/MakanBoleh_logo_stacked_light_large.png" class="logo_img">

        <GoogleSignIn class="mt-5"/>

        <div class="d-flex align-items-center mt-3">
            <hr>
            <span id="text-divider">or</span>
            <hr>
        </div>

        <div class="small form-floating mt-3 mb-3 text-dark">
            <input v-model="user_name" type="text" class="form-control" id="floatingInput"
            placeholder="name@example.com">
            <label for="floatingInput">Username</label>
        </div>
        
        <div class="small form-floating text-dark">
            <input v-model="password" type="password" class="form-control" id="floatingPassword" placeholder="Password">
            <label for="floatingPassword">Password</label>
        </div>

        <div class="d-flex justify-content-center">
            <button class="btn btn-main mt-3" @click="login">Log in</button>
        </div>

        <hr class="mt-3" style="width: 340px">
        <div class="mt-3 text-center">
            Don't have an account?
        </div>
        
        <div class="d-flex justify-content-center">
            <router-link to="/signup"><button class="btn btn-main mt-3">Sign up for Makan Boleh</button></router-link>
        </div>

        <!-- <form action="" class="d-flex flex-column mt-3">
            <small>Username</small>
            <input type="text">

            <small>Password</small>
            <input type="password">

            <div class="d-flex justify-content-center">
                <button class="btn btn-main mt-3">Login</button>
            </div>
        </form> -->
    </div>
</template>


<script>
    import axios from 'axios'
    import GoogleSignIn from '../components/GoogleSignIn.vue';
    const login_URL = 'http://localhost:5100/login'

    export default{
        components: {
            GoogleSignIn,
        },
        data() {
            return {
                user_name: '',
                password:'',
                user_details:''
            }
        },
        methods: {
            login(){

                // user: rach123
                // pw: Password12345!

                axios.post(`${login_URL}`, {
                     
                        username:  this.user_name,
                        password: this.password
                    
                })
                    .then(response => {

                        // this response will give all user details
                        // store this to session or sth
                        console.log(response.data);
                        this.user_details = response.data
                    })
                    .catch( error => {
                        console.log(error.message);
                    });
            }
        }
    }
</script>


<style scoped>
    #login-body{
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .logo_img{
        width: 250px
    }

    hr {
        margin: 0px 15px;
        border-top: 2px solid;
        width: 145px;
    }

    #text-divider {
        flex: 0.3 1 0%;
    }

    .form-floating {
        width: 340px;
    }
</style>