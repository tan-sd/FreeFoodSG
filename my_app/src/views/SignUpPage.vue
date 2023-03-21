<template>
    <div class="container-fluid bg-dark text-light" id="login-body">
        <img src="../assets/images/logos/large_logos/MakanBoleh_logo_stacked_light_large.png" class="logo_img">

        <form class="register-form" style="width: 350px">
            <div class="form-row mt-5">
                <div class="row">
                    <div class="col-md-6">
                        <div class="small form-floating mb-3 text-dark">
                            <input v-model="first_name" type="text" class="form-control" id="floatingInput" placeholder="First Name">
                            <label for="floatingInput">First Name</label>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="small form-floating mb-3 text-dark">
                            <input v-model="last_name" type="text" class="form-control" id="floatingInput" placeholder="Last Name">
                            <label for="floatingInput">Last Name</label>
                        </div>
                    </div>
                </div>
                <div class="small form-floating mb-3 text-dark">
                    <input v-model="user_name" type="text" class="form-control" id="floatingInput"
                    placeholder="Username">
                    <label for="floatingInput">Username</label>
                </div>

                <div class="small form-floating mb-3 text-dark">
                    <input v-model="password" type="password" class="form-control" id="floatingPassword" placeholder="Password">
                    <label for="floatingPassword">Password</label>
                </div>

                <div class="small form-floating text-dark mb-3">
                    <input v-model="confirm_password" type="password" class="form-control" id="floatingPassword" placeholder="Password">
                    <label for="floatingPassword">Confirm Password</label>
                </div>

                <div class="input-group">
                    <span class="input-group-text mb-3">+65</span>
                    <div class="small form-floating text-dark mb-3">
                        <input v-model="phone_number" type="number" class="form-control" id="floatingInputGroup1" placeholder="Phone Number">
                        <label for="floatingInputGroup1">Phone Number</label>
                    </div>
                </div>

                <div class="small form-floating text-dark mb-3">
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

                <div class="small form-floating text-dark mb-3">
                    <input v-model="user_email" type="email" class="form-control" id="floatingInput" placeholder="name@example.com">
                    <label for="floatingInput">Email address</label>
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
    import axios from 'axios'
    // import bcrypt from 'bcryptjs';
    const register_user_URL = "http://localhost:1111/user";

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
                travel_appetite: ''
            }
        },
        methods: {
            register_user() {
                // const salt = bcrypt.genSaltSync(10)
                // var hashed_password = bcrypt.hashSync(this.password, salt)

                console.log(this.dietary_type)

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

                    axios.post(`${register_user_URL}/${this.user_name}`,
                    json_data
                    )
                        .then(response => {
                            
                            console.log(response.data);
                        })
                        .catch( error => {
                            console.log(error.message);
                        });
                })
                .catch(error => {
                    console.log(error);
                })

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
</style>