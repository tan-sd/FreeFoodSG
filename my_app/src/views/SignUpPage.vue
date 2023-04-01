<template>
    <div class="container-fluid bg-dark text-light" id="login-body">
        <img src="../assets/images/logos/large_logos/MakanBoleh_logo_stacked_light_large.png" class="logo_img pt-5">

        <form class="register-form" style="width: 350px">
            <div class="form-row mt-5">
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <div class="small form-floating text-dark">
                            <input v-model="first_name" v-on:keypress="is_letter($event)" type="text" class="form-control" id="first_name_input" placeholder="First Name">
                            <label for="floatingInput">First Name</label>
                        </div>
                        <div id="first_name_signup_invalid" class="small form-floating mt-2 d-none">
                            Please enter your first name.
                        </div>
                    </div>
                    <div class="col-md-6 mb-3">
                        <div class="small form-floating text-dark">
                            <input v-model="last_name" v-on:keypress="is_letter($event)" type="text" class="form-control" id="last_name_input" placeholder="Last Name">
                            <label for="floatingInput">Last Name</label>
                        </div>
                        <div id="last_name_signup_invalid" class="small form-floating mt-2 d-none">
                            Please enter your last name.
                        </div>
                    </div>
                </div>
                <div class="mb-3">
                    <div class="small form-floating text-dark">
                        <input v-model="user_name" type="text" class="form-control" id="username_input"
                        placeholder="Username">
                        <label for="floatingInput">Username</label>
                    </div>
                    <div id="username_signup_invalid" class="small form-floating mt-2 d-none">
                    </div>
                </div>

                <div class="mb-3">
                    <div class="small form-floating mb-2 text-dark">
                        <input v-model="password" type="password" class="form-control" id="password_input" placeholder="Password">
                        <label for="floatingPassword">Password</label>
                    </div>
                    <div id="password_signup_invalid" class="small form-floating mt-2 d-none">
                    </div>
                </div>

                <div class="mb-3">
                    <div class="small form-floating text-dark mb-2">
                        <input v-model="confirm_password" type="password" class="form-control" id="confirm_password_input" placeholder="Password">
                        <label for="floatingPassword">Confirm Password</label>
                    </div>
                    <div id="confirm_password_signup_invalid" class="small form-floating mt-2 d-none">
                        Passwords does not match. Please try again.
                    </div>
                </div>

                <div class="mb-3">
                    <div class="input-group">
                        <span class="input-group-text">+65</span>
                        <div class="small form-floating text-dark">
                            <input v-model="phone_number" type="number" class="form-control" id="phone_number_input" placeholder="Phone Number">
                            <label for="floatingInputGroup1">Phone Number</label>
                        </div>
                    </div>
                    <div id="phone_number_signup_invalid" class="small form-floating mt-2 d-none">
                        Please enter a valid phone number.
                    </div>
                </div>

                <div class="mb-3">  
                    <div class="small form-floating text-dark">
                    <GMapAutocomplete
                        ref="gmap_autocomplete"
                        class="form-control"
                        placeholder=" "
                        id="googlemap_autocomplete_foodform"
                        type="text"
                        :options="autoCompleteOptions"
                        :value="location"
                    >
                    </GMapAutocomplete>
                    <label for="googlemap_autocomplete_foodform">Location</label>
                    </div>
                    <div id="location_signup_invalid" class="small form-floating mt-2 d-none">
                        Please enter a location.
                    </div>
                </div>

                <div class="mb-3">
                    <div class="small form-floating text-dark">
                        <input v-model="user_email" type="email" class="form-control" id="user_email_input" placeholder="name@example.com">
                        <label for="floatingInput">Email address</label>
                    </div>
                    <div id="user_email_signup_invalid" class="small form-floating mt-2 d-none">
                        Please enter a valid email address.
                    </div>
                </div>

                <div class="bg-white rounded ps-3 pt-3 pb-3 text-dark mb-3">
                    <label class="small form-label">Dietary Type</label>
                    <div class="d-flex justify-content-around">
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckbox1" value="Halal" v-model="dietary_type">
                            <label class="small form-check-label" for="inlineCheckbox1">Halal</label>
                            </div>
                            <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckbox2" value="Vegetarian"
                            v-model="dietary_type">
                            <label class="small form-check-label" for="inlineCheckbox2">Vegetarian</label>
                            </div>
                            <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="inlineCheckbox3" value="No beef"
                            v-model="dietary_type">
                            <label class="small form-check-label" for="inlineCheckbox3">No beef</label>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded ps-3 pt-3 pb-3 text-dark">
                    <label class="small form-label">Travel Appetite</label>
                    <br>
                    <div class="d-flex justify-content-around">
                        <div class="form-check form-check-inline">
                            <input v-model="travel_appetite" class="small form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="Near" checked>
                            <label class="small form-check-label" for="inlineRadio1">Near</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input v-model="travel_appetite" class="small form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2" value="Medium">
                            <label class="small form-check-label" for="inlineRadio2">Medium</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input v-model="travel_appetite" class="small form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio3" value="Far">
                            <label class="small form-check-label" for="inlineRadio3">Far</label>
                        </div>
                    </div>
                </div>
            </div>
        </form>

        <div class="d-flex justify-content-center">
            <button @click="register_user" v-on:submit.prevent="OnSubmit" class="btn btn-main mt-3">Sign up</button>
        </div>

        <hr class="mt-3" style="width: 340px">
        <div class="mt-3 mb-5 text-center">
            Have an account? <router-link to="/login">Log in</router-link>
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
    /* eslint-disable no-useless-escape */
    import axios from 'axios'
    // import bcrypt from 'bcryptjs';
    const register_user_URL = "http://localhost:5100/user";
    // 'http://localhost:5100/user'

    // "user_id": self.user_id,
    // "name": self.name,
    // "username": self.username,
    // "number": self.number,
    // "email": self.email,
    // "password": self.password,
    // "address": self.address,
    // "latitude": self.latitude,
    // "longitude":self.longitude,
    // "dietary_type": self.dietary_type,
    // "travel_appetite": self.travel_appetite

    export default{
        data() {
            return {
                first_name: '',
                last_name: '',
                user_name: '',
                password: '',
                confirm_password: '',
                phone_number: '',
                location: '',
                user_email: '',
                dietary_type: [],
                travel_appetite: 'Near',
                errors: 0,
                autoCompleteOptions: {
                    componentRestrictions: {
                        country: ["sg"],
                    }
                },
            }
        },
        methods: {
            is_letter(e) {
                let char = String.fromCharCode(e.keyCode); // Get the character
                if(/^[A-Za-z ]+$/.test(char)) return true; // Match with regex 
                else e.preventDefault(); // If not match, don't add to input text
            },
            register_user() {

                console.log(this.travel_appetite)
                // const salt = bcrypt.genSaltSync(10)
                // var hashed_password = bcrypt.hashSync(this.password, salt)

                this.errors = 0
                var first_name = document.getElementById('first_name_input');
                var first_name_invalid = document.getElementById('first_name_signup_invalid');
                var last_name = document.getElementById('last_name_input');
                var last_name_invalid = document.getElementById('last_name_signup_invalid');
                var username = document.getElementById('username_input');
                var username_invalid = document.getElementById('username_signup_invalid');
                var password = document.getElementById('password_input');
                var password_invalid = document.getElementById('password_signup_invalid');
                var confirm_password = document.getElementById('confirm_password_input');
                var confirm_password_invalid = document.getElementById('confirm_password_signup_invalid');
                var phone_number = document.getElementById('phone_number_input');
                var phone_number_invalid = document.getElementById('phone_number_signup_invalid');
                // var location = document.getElementById('location_input');
                var location_invalid = document.getElementById('location_signup_invalid');
                var email = document.getElementById('user_email_input');
                var email_invalid = document.getElementById('user_email_signup_invalid');

                if(this.first_name.length == 0) {
                    first_name.classList = 'form-control is-invalid';
                    first_name_invalid.classList.remove("d-none");
                    first_name.classList.add('errShake');
                    first_name.onaimationend = () => {
                        setTimeout(first_name.classList.remove("errShake", 200));
                    };
                    this.errors += 1
                } else {
                    first_name.classList = 'form-control is-valid';
                    first_name_invalid.classList.add("d-none");
                }

                if(this.last_name.length == 0) {
                    last_name.classList = 'form-control is-invalid';
                    last_name_invalid.classList.remove("d-none");
                    last_name.classList.add('errShake');
                    last_name.onaimationend = () => {
                        setTimeout(first_name.classList.remove("errShake", 200));
                    };
                    this.errors += 1
                } else {
                    last_name.classList = 'form-control is-valid';
                    last_name_invalid.classList.add("d-none");
                }

                if(this.user_name.length == 0) {
                    username.classList = 'form-control is-invalid';
                    username_invalid.classList.remove("d-none");
                    username.classList.add('errShake');
                    username.onaimationend = () => {
                        setTimeout(username.classList.remove("errShake", 200));
                    };
                    this.errors += 1
                    username_invalid.innerHTML = 'Please enter a username.'
                } else if(this.user_name.length < 6) {
                    username.classList = 'form-control is-invalid';
                    username_invalid.classList.remove("d-none");
                    username.classList.add('errShake');
                    username.onaimationend = () => {
                        setTimeout(username.classList.remove("errShake", 200));
                    };
                    this.errors += 1
                    username_invalid.innerHTML = 'Username must be least 6 characters.'
                } else {
                    username.classList = 'form-control is-valid';
                    username_invalid.classList.add("d-none");
                    this.user_name = this.user_name.toLowerCase();
                }

                if(this.password.length == 0) {
                    password.classList = 'form-control is-invalid';
                    password_invalid.classList.remove("d-none");
                    password.classList.add('errShake');
                    password.onaimationend = () => {
                        setTimeout(password.classList.remove("errShake", 200));
                    };
                    this.errors += 1
                    password_invalid.innerHTML = 'Please enter a password.'
                } else if(this.password.length < 8) {
                    password.classList = 'form-control is-invalid';
                    password_invalid.classList.remove("d-none");
                    password.classList.add('errShake');
                    password.onaimationend = () => {
                        setTimeout(password.classList.remove("errShake", 200));
                    };
                    this.errors += 1
                    password_invalid.innerHTML = 'Password must be at least 8 characters.'
                } else if(this.password != this.confirm_password) {
                    password.classList = 'form-control is-valid';
                    password_invalid.classList.add("d-none");
                    confirm_password.classList = 'form-control is-invalid';
                    confirm_password_invalid.classList.remove("d-none");
                    confirm_password.classList.add('errShake');
                    confirm_password.onaimationend = () => {
                        setTimeout(confirm_password.classList.remove("errShake", 200));
                    };
                    this.errors += 1
                } else {
                    password.classList = 'form-control is-valid';
                    confirm_password.classList = 'form-control is-valid';
                    confirm_password_invalid.classList.add("d-none");
                }

                if (this.phone_number.toString().length < 8 || this.phone_number.toString()[0] != 9) {
                    phone_number.classList = 'form-control is-invalid';
                    phone_number_invalid.classList.remove("d-none");
                    phone_number.classList.add('errShake');
                    phone_number.onaimationend = () => {
                        setTimeout(phone_number.classList.remove("errShake", 200));
                    };
                    this.errors += 1
                } else {
                    console.log(this.phone_number.toString()[0])
                    phone_number.classList = 'form-control is-valid';
                    phone_number_invalid.classList.add("d-none");
                }

                if (this.$refs.gmap_autocomplete.$refs.input.value.length == 0) {
                    // location.classList = 'form-control is-invalid';
                    location_invalid.classList.remove("d-none");
                    // location.classList.add('errShake');
                    // location.onaimationend = () => {
                    //     setTimeout(phone_number.classList.remove("errShake", 200));
                    // };
                    this.errors += 1
                } else {
                    // location.classList = 'form-control is-valid';
                    location_invalid.classList.add("d-none");
                }

                if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(this.user_email)) {
                    email.classList = 'form-control is-invalid';
                    email_invalid.classList.remove('d-none');
                    email.classList.add('errShake');
                    email.onaimationend = () => {
                        setTimeout(email.classList.remove("errShake", 200));
                    };
                    this.errors += 1
                } else {
                    email.classList = "form-control is-valid";
                    email_invalid.classList.add('d-none');
                }

                if(this.errors == 0) {

                    var json_data = {
                        "first_name": this.first_name,
                        "last_name": this.last_name,
                        "username": this.user_name,
                        "number": this.phone_number,
                        "email": this.user_email,
                        "password": this.password,
                        "address": this.$refs.gmap_autocomplete.$refs.input.value,
                        "latitude": null,
                        "longitude": null,
                        "dietary_type": this.dietary_type,
                        "travel_appetite": this.travel_appetite
                    };

                    console.log(this.$refs.gmap_autocomplete.$refs.input.value)

                    fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${this.$refs.gmap_autocomplete.$refs.input.value}&key=AIzaSyB_XNrepzj7pUf2-dp9vSkpAfjXkAB9yHI`)
                    .then((response) => {
                        return response.json();
                    }).then(jsonData => {
                        console.log(jsonData.results[0].geometry.location); // {lat: 45.425152, lng: -75.6998028}
                        json_data['latitude'] = jsonData.results[0].geometry.location.lat
                        json_data['longitude'] = jsonData.results[0].geometry.location.lng
                        console.log(json_data)

                        console.log(json_data)

                        console.log(`${register_user_URL}/${this.user_name}`)

                        axios.post(`${register_user_URL}`,
                        json_data
                        )
                            .then(response => {
                                console.log(response.data);
                                this.$router.push('/login');
                            })
                            .catch( error => {
                                console.log(error.message);
                            });
                    })
                    .catch(error => {
                        console.log(error);
                    })
                }

                // fetch(`${register_user_URL}/${this.new_user}`,
                //     {
                //         method: "POST",
                //         headers: {
                //             "Content-type": "application/json"
                //         },
                //         body: json_data
                //     })
                //     .then(response => response.json())
                //     .then(data => {
                //         console.log(data);
                //         var result = data.data;
                //         console.log(result)
                //     })

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

    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
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

    @media (min-width: 769px) {
        #first_name_signup_invalid, #last_name_signup_invalid {
            font-size: 12.5px
        }
    }
</style>