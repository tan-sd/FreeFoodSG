<template>
    <div class="fill-space">
        <div class="container-fluid bg-dark text-light py-5" id="login-body">
            <img src="../assets/images/logos/large_logos/MakanBoleh_logo_stacked_light_large.png" class="logo_img">
    
            <GoogleSignIn class="mt-5"/>
    
            <div class="d-flex align-items-center mt-3">
                <hr>
                <span id="text-divider">or</span>
                <hr>
            </div>
    
            <div class="small form-floating mt-3 text-dark">
                <input v-model="user_name" type="text" class="form-control" id="username_input"
                placeholder="name@example.com">
                <label for="floatingInput">Username</label>
            </div>
            <div id="username_login_invalid" class="small form-floating mt-2 d-none">
                Please enter your username.
            </div>
            
            <div class="small form-floating text-dark mt-3">
                <input v-model="password" type="password" class="form-control" id="password_input" placeholder="Password" @keyup.enter="login">
                <label for="floatingPassword">Password</label>
            </div>
            <div id="password_login_invalid" class="small form-floating mt-2 d-none">
                Please enter your password.
            </div>
    
            <div id="errors" class="small mt-3" style="height: 20px"></div>
    
            <div class="d-flex justify-content-center">
                <button class="btn btn-main mt-3" :disabled="login_loading" @click="login"><font-awesome-icon :icon="['fas', 'spinner']" v-if="login_loading" spin class="me-3" />Log in</button>
            </div>
    
            <hr class="mt-3" style="width: 340px">
            <div class="mt-3 text-center">
                Don't have an account?
            </div>
            
            <div class="d-flex justify-content-center">
                <router-link to="/signup"><button class="btn btn-main mt-3">Sign up for Makan Boleh</button></router-link>
            </div>
        </div>
    </div>
</template>


<script>
    import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
    import axios from 'axios'
    import GoogleSignIn from '../components/GoogleSignIn.vue';
    const login_URL = 'http://localhost:1111/login'

    export default{
        components: {
            GoogleSignIn,
            FontAwesomeIcon
        },
        data() {
            return {
                user_name: '',
                password:'',
                user_details:'',
                login_loading: false,
                sessionUserName: '',
            }
        },
        methods: {
            login(){
                this.login_loading = true

                var username = document.getElementById("username_input");
                var username_invalid = document.getElementById("username_login_invalid");
                var password = document.getElementById("password_input")
                var password_invalid = document.getElementById("password_login_invalid");

                if(this.user_name.length == 0) {
                    username.classList = "form-control is-invalid";
                    username.classList.add('errShake');
                    username.onanimationend = () => {
                        setTimeout(username.classList.remove("errShake", 200));
                    };
                    username_invalid.classList.remove("d-none")
                    document.getElementById("errors").innerHTML = ''
                    this.login_loading = false
                } else if(this.password.length == 0) {
                    username.classList = "form-control";
                    username_invalid.classList.add("d-none");
                    password.classList = 'form-control is-invalid';
                    password.classList.add('errShake');
                    password.onanimationend = () => {
                        setTimeout(password.classList.remove("errShake", 200));
                    };
                    password_invalid.classList.remove("d-none")
                    document.getElementById("errors").innerHTML = ''
                    this.login_loading = false
                }
                else {
                    username.classList = "form-control";
                    username_invalid.classList.add("d-none");
                    password.classList = 'form-control';
                    password_invalid.classList.add("d-none");

                    axios.post(`${login_URL}`, {
                        username: this.user_name,
                        password: this.password
                })
                    .then(response => {
                        // this response will give all user details
                        // store this to session or sth
                        console.log(response.data.user.username)
                        this.$store.state.user_details = response.data.user
                        this.$store.state.username = response.data.user.username
                        this.$store.state.isAuthenticated = true
                        // localStorage.setItem('username', response.data.user.user_name)

                        this.$router.push('/')
                    })
                    .catch(error => {
                        console.log("error response: ", error)
                        document.getElementById("errors").innerHTML = error.response.data.msg
                        this.login_loading = false
                    });
                }
            }
        }
    }
</script>


<style scoped>
    .fill-space{
        height: 100%;
        position: relative;
    }

    #login-body{
        height: 100%;
        display: flex;
        align-items: center;
        flex-direction: column;
        overflow-y: scroll;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        background-image: linear-gradient(180deg, #264726, #336033);
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

    .errShake {
    -webkit-animation: errorShake 0.4s 1 linear;
    -moz-animation: errorShake 0.4s 1 linear;
    -o-animation: errorShake 0.4s 1 linear;
    animation: errorShake 0.4s 1 linear;
    }

    @keyframes errorShake {
        0% {
            transform: translate(30px);
        }
        20% {
            transform: translate(-30px);
        }
        40% {
            transform: translate(15px);
        }
        60% {
            transform: translate(-15px);
        }
        80% {
            transform: translate(8px);
        }
        100% {
            transform: translate(0px);
        }
    }

    @-webkit-keyframes errorShake {
        0% {
            -webkit-transform: translate(30px);
        }
        20% {
            -webkit-transform: translate(-30px);
        }
        40% {
            -webkit-transform: translate(15px);
        }
        60% {
            -webkit-transform: translate(-15px);
        }
        80% {
            -webkit-transform: translate(8px);
        }
        100% {
            -webkit-transform: translate(0px);
        }
    }
    @-moz-keyframes errorShake {
        0% {
            -moz-transform: translate(30px);
        }
        20% {
            -moz-transform: translate(-30px);
        }
        40% {
            -moz-transform: translate(15px);
        }
        60% {
            -moz-transform: translate(-15px);
        }
        80% {
            -moz-transform: translate(8px);
        }
        100% {
            -moz-transform: translate(0px);
        }
    }
    @-o-keyframes errorShake {
        0% {
            -o-transform: translate(30px);
        }
        20% {
            -o-transform: translate(-30px);
        }
        40% {
            -o-transform: translate(15px);
        }
        60% {
            -o-transform: translate(-15px);
        }
        80% {
            -o-transform: translate(8px);
        }
        100% {
            -o-origin-transform: translate(0px);
        }
    }
</style>