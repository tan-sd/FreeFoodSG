<template>
    <div class="fill-space">
        <div class="container-fluid bg-extra-light text-dark" id="user-profile-body">
            <button class="btn btn-main-fixed m-3" id="user-profile-edit-btn" @click="toggle_edit()">
                <font-awesome-icon icon="fa-solid fa-pen-to-square" v-if="!edit_mode" />
                <font-awesome-icon icon="fa-solid fa-xmark" v-if="edit_mode" />&nbsp;
                <span v-if="!edit_mode">Edit</span>
                <span v-if="edit_mode">Cancel</span>
            </button>

            <!-- IMG, FULLNAME AND USERNAME -->
            <div class="row justify-content-center py-5">
                <div class="rounded-circle profile-circle col-auto">
                    {{ first_name.slice(0,1) }}
                </div>
    
                <div class="col-auto d-flex justify-content-center flex-column">
                    <h1>{{ first_name }} {{ last_name }}</h1>
                    <h4 class="fst-italic fw-semibold">@{{ username }}</h4>
                </div>
            </div>

            <!-- VIEW MODE -->
            <div v-if="!edit_mode" class="mb-5">
        
                <!-- DISPLAY: ALL USER DETAILS -->
        
                <!-- First Name -->
                <div class="row justify-content-center">
                    <div class="col-6">
                        <p class="fw-bold text-end">
                            First Name:
                        </p>
                    </div>
        
                    <div class="col-6">
                        <p>
                            {{ first_name }}
                        </p>
                    </div>
                </div>
        
                <!-- Last Name -->
                <div class="row justify-content-center">
                    <div class="col-6">
                        <p class="fw-bold text-end">
                            Last Name:
                        </p>
                    </div>
        
                    <div class="col-6">
                        <p>
                            {{ last_name }}
                        </p>
                    </div>
                </div>
        
                <!-- Default Adress -->
                <div class="row justify-content-center">
                    <div class="col-6">
                        <p class="fw-bold text-end">
                            Default Adress:
                        </p>
                    </div>
        
                    <div class="col-6">
                        <p>
                            {{ address }}
                        </p>
                    </div>
                </div>
        
                <!-- Phone Number -->
                <div class="row justify-content-center">
                    <div class="col-6">
                        <p class="fw-bold text-end">
                            Phone Number:
                        </p>
                    </div>
        
                    <div class="col-6">
                        <p>
                            {{ number }}
                        </p>
                    </div>
                </div>
        
                <!-- Email -->
                <div class="row justify-content-center">
                    <div class="col-6">
                        <p class="fw-bold text-end">
                            Email:
                        </p>
                    </div>
        
                    <div class="col-6">
                        <p>
                            {{ email }}
                        </p>
                    </div>
                </div>
        
                <!-- Travel Appetite -->
                <div class="row justify-content-center">
                    <div class="col-6">
                        <p class="fw-bold text-end">
                            Travel Appetite:
                        </p>
                    </div>
        
                    <div class="col-6">
                        <p>
                            {{ travel_appetite }} km
                        </p>
                    </div>
                </div>
        
                <!-- Dietary Restrictions -->
                <div class="row justify-content-center">
                    <div class="col-6">
                        <p class="fw-bold text-end">
                            Dietary Restrictions:
                        </p>
                    </div>
        
                    <div class="col-6">
                        <p>
                            {{ dietary_res.join(', ') }}
                        </p>
                    </div>
                </div>
            </div>
    
            <!-- EDIT MODE -->
            <div v-if="edit_mode">
                <!-- First Name -->
                <div class="form-floating mb-2">
                    <input type="text" v-model="form_first_name" class="form-control">
                    <label for="floatingInput">First Name</label>
                </div>
        
                <!-- First Name -->
                <div class="form-floating mb-2">
                    <input type="text" v-model="form_last_name" class="form-control">
                    <label for="floatingInput">Last Name</label>
                </div>

                <!-- POST ADDRESS -->
                <div class="form-floating mb-2">
                    <GMapAutocomplete
                        class="form-control"
                        :value="form_address"
                        placeholder=" "
                        id="googlemap_autocomplete_profile"
                        type="text"
                        :options="autoCompleteOptions"
                        @place_changed="setPlace"
                    >
                    </GMapAutocomplete>

                    <label for="googlemap_autocomplete_profile"><font-awesome-icon icon="fa-solid fa-location-dot" />&nbsp;Default Location</label>
                </div>
        
                <!-- Phone Number -->
                <div class="mb-2">
                    <div class="input-group">
                        <span class="input-group-text">+65</span>
                        <div class="small form-floating text-dark">
                            <input v-model="form_number" type="number" class="form-control" placeholder=" ">
                            <label for="floatingInputGroup1">Phone Number</label>
                        </div>
                    </div>
                </div>
        
                <!-- Email -->
                <div class="form-floating mb-2">
                    <input type="text" v-model="form_email" class="form-control">
                    <label for="floatingInput">Email</label>
                </div>
        
                <!-- Travel Appetite -->
                <div class="form-floating mb-2">
                    <input type="number" v-model="form_travel_appetite" class="form-control">
                    <label for="floatingInput">Travel Appetite (km)</label>
                </div>
        
                <!-- Dietary Restrictions START -->
                <div class="d-flex justify-content-center mb-3">
                    <div class="form-check mx-2">
                        <input class="form-check-input" type="checkbox" value="halal" id="user-foodform-halal-checkbox" v-model="form_dietary_res">
                        <label class="form-check-label" for="user-foodform-halal-checkbox">
                            <font-awesome-icon icon="fa-solid fa-star-and-crescent" />&nbsp;Halal
                        </label>
                    </div>
        
                    <div class="form-check mx-2">
                        <input class="form-check-input" type="checkbox" value="vegetarian" id="user-foodform-vege-checkbox" v-model="form_dietary_res">
                        <label class="form-check-label" for="user-foodform-vege-checkbox">
                            <font-awesome-icon icon="fa-solid fa-leaf" />&nbsp;Vegetarian
                        </label>
                    </div>
        
                    <div class="form-check mx-2">
                        <input class="form-check-input" type="checkbox" value="nobeef" id="user-foodform-nobeef-checkbox" v-model="form_dietary_res">
                        <label class="form-check-label" for="user-foodform-nobeef-checkbox">
                            <font-awesome-icon icon="fa-solid fa-cow" />&nbsp;No Beef
                        </label>
                    </div>
                </div>
                <!-- Dietary Restrictions END -->

                <!-- EMAIL AND SMS NOTIF -->
                <div class="d-flex justify-content-center mb-3">
                    <div class="form-check mx-2">
                        <input class="form-check-input" type="checkbox" id="user-profile-email-checkbox" v-model="form_email_notif" value="1">
                        <label class="form-check-label" for="user-profile-email-checkbox">Get Email Notifications</label>
                    </div>

                    <div class="form-check mx-2">
                        <input class="form-check-input" type="checkbox" id="user-profile-sms-checkbox" v-model="form_sms_notif">
                        <label class="form-check-label" for="user-profile-sms-checkbox">Get SMS Notifications</label>
                    </div>
                </div>

                <!-- SUBMIT BUTTON -->
                <div class="mb-5 d-flex justify-content-center">
                    <button class="btn btn-main-fixed" @click="submit_new_user_details()">Save Changes</button>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
    import axios from 'axios'
    import router from '@/router';

    export default{
        data() {
            return {
                first_name: '',
                last_name: '',
                username: '',
                number: '',
                address: '',
                dietary_res: [],
                email: '',
                travel_appetite: '',
                sms_notif: '',
                email_notif: '',
                lat: '',
                lng: '',

                form_first_name: '',
                form_last_name: '',
                form_username: '',
                form_number: '',
                form_address: '',
                form_dietary_res: [],
                form_email: '',
                form_travel_appetite: '',
                form_lat: '',
                form_lng: '',
                form_sms_notif: '',
                form_email_notif: '',

                edit_mode: false,
                autoCompleteOptions: {
                    componentRestrictions: {
                        country: ["sg"],
                    }
                },
            }
        },

        methods: {
            update_user_details() {
                var user_deets = this.$store.state.user_details

                this.first_name = user_deets.first_name
                this.last_name = user_deets.last_name
                this.username = user_deets.username
                this.number = parseInt(user_deets.number)
                this.address = user_deets.address
                this.email = user_deets.email
                this.travel_appetite = user_deets.travel_appetite
                this.username = user_deets.username
                this.sms_notif = ((user_deets.sms_notif == 1) ? true : false)
                this.email_notif = ((user_deets.email_notif == 1) ? true : false)
                this.lat = user_deets.latitude
                this.lng = user_deets.longitude

                this.form_first_name = user_deets.first_name
                this.form_last_name = user_deets.last_name
                this.form_username = user_deets.username
                this.form_number = parseInt(user_deets.number)
                this.form_address = user_deets.address
                this.form_email = user_deets.email
                this.form_travel_appetite = user_deets.travel_appetite
                this.form_username = user_deets.username
                this.form_sms_notif = ((user_deets.sms_notif == 1) ? true : false)
                this.form_email_notif = ((user_deets.email_notif == 1) ? true : false)

                this.dietary_res = []
                this.form_dietary_res = []
                
                var str_dietres = user_deets.dietary_type
                if (str_dietres == '') {
                    return
                } else {

                    for (var e_diet_res of str_dietres.split(",")) {
                        this.dietary_res.push(e_diet_res.toLowerCase())
                        this.form_dietary_res.push(e_diet_res.toLowerCase())
                    }
                }
            },

            toggle_edit() {
                this.edit_mode = !this.edit_mode
                this.reset_fields()
            },

            reset_fields() {
                this.form_first_name = this.first_name,
                this.form_last_name = this.last_name,
                this.form_username = this.username,
                this.form_number = this.number,
                this.form_address = this.address,
                this.form_email = this.email,
                this.form_travel_appetite = this.travel_appetite,
                this.form_username = this.username
                this.form_dietary_res = this.dietary_res
            },

            submit_new_user_details() {
                console.log(`=== [START] submit_new_user_details() ===`)

                var to_check = [
                    this.form_first_name,
                    this.form_last_name,
                    this.form_username,
                    this.form_number,
                    this.form_address,
                    this.form_email,
                    this.form_travel_appetite
                ]

                // console.log(to_check)

                for (var e_var of to_check) {
                    if (e_var.length == 0) {
                        return false
                    }
                }

                var new_user_deets = {
                    first_name: this.form_first_name,
                    last_name: this.form_last_name,
                    username: this.form_username,
                    number: this.form_number,
                    address: this.form_address,
                    dietary_type: (this.form_dietary_res).join(','),
                    email: this.form_email,
                    travel_appetite: this.form_travel_appetite,
                    email_notif: (this.form_email_notif ? 1 : 0),
                    sms_notif: (this.form_sms_notif ? 1 : 0),
                    latitude: (this.form_lat == '') ? this.lat : this.form_lat,
                    longitude: (this.form_lng == '') ? this.lng : this.form_lng,
                    user_id: this.$store.state.user_details.user_id
                }

                console.log("new user deets", new_user_deets)

                var vm = this

                axios.put("http://127.0.0.1:1111/profile/update", new_user_deets)
                .then(function(response) {
                    console.log(response)
                    vm.$store.state.user_details = new_user_deets
                    vm.update_user_details()
                    vm.edit_mode = false
                })
                .catch(function(error) {
                    console.log(error)
                })
            },

            setPlace(place) {
                this.form_address = place.formatted_address
                this.form_lat = place.geometry.location.lat()
                this.form_lng = place.geometry.location.lng()
            }
        },

        created() {
            
            if (!(this.$store.state.isAuthenticated)) {
                router.push({path: '/login'})
            } else {
                this.update_user_details()
            }
        }
    }
</script>


<style scoped>
    #user-profile-body{
        height: 100%;
        overflow-y: scroll;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
    }

    .profile-circle {
        background: white;
        color: #f3704b;
        width: 150px;
        height: 150px;
        border-radius: 50%;
        font-size: 90px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .fill-space{
        height: 100%;
        position: relative;
    }

    #user-profile-edit-btn{
        position: absolute;
        top: 0;
        right: 0;
    }
</style>