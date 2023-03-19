<template>
    <div class="container-fluid bg-dark text-light" id="login-body">
        <img src="../assets/images/logos/large_logos/MakanBoleh_logo_stacked_light_large.png" class="logo_img">

        <form class="register-form" style="width: 350px">
            <div class="form-row mt-5">
                <div class="row">
                    <div class="col-md-6">
                        <div class="small form-floating mb-3 text-dark">
                            <input type="text" class="form-control" id="floatingInput" placeholder="First Name">
                            <label for="floatingInput">First Name</label>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="small form-floating mb-3 text-dark">
                            <input type="text" class="form-control" id="floatingInput" placeholder="Last Name">
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
                    <input type="password" class="form-control" id="floatingPassword" placeholder="Password">
                    <label for="floatingPassword">Password</label>
                </div>

                <div class="small form-floating text-dark mb-3">
                    <input type="password" class="form-control" id="floatingPassword" placeholder="Password">
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
                    <input v-model="user_email" type="email" class="form-control" id="floatingInput" placeholder="name@example.com">
                    <label for="floatingInput">Email address</label>
                </div>

                <div class="bg-white rounded ps-3 pt-3 pb-3 text-dark">
                    <label class="small form-label">Travel Appetite</label>
                    <br>
                    <div class="d-flex justify-content-around">
                        <div class="form-check form-check-inline">
                            <input class="small form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="option1">
                            <label class="small form-check-label" for="inlineRadio1">Near</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="small form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2" value="option2">
                            <label class="small form-check-label" for="inlineRadio2">Medium</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input class="small form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio3" value="option3">
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
        <div class="mt-3 text-center">
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
    const register_user_URL = "http://localhost:1111/users";

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
                user_name: '',
                phone_number: '',
                user_email: '',
            }
        },
        methods: {
            register_user() {
                let json_data = JSON.stringify({
                    "name": "rachel",
                    "username": "rach123",
                    "number": "12312414",
                    "email": "dontemailme@gmail.com",
                    "password": "Password12345!",
                    "address": "Singapore Management University",
                    "latitude": 1.2312412,
                    "longitude": 2.4421412414,
                    "dietary_type": "halal",
                    "travel_appetite": "far"
                });

                fetch(`${register_user_URL}/${this.new_user}`,
                    {
                        method: "POST",
                        headers: {
                            "Content-type": "application/json"
                        },
                        body: json_data
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        var result = data.data;
                        console.log(result)
                    })

                
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