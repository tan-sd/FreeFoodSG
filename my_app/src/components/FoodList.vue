<template>
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-sm">
            <div class="modal-content">
                <div class="modal-header bg-dark text-extra-light">
                    <h5 class="modal-title" id="modal-title-confirm">
                        Confirm?
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="d-flex justify-content-around mt-3 mb-3">
                    <button type="button" class="btn btn-main btn-size"
                    data-bs-dismiss="modal"  
                    @click="cancelFood">Yes</button>
                    <button type="button" class="btn btn-main btn-size"
                    data-bs-dismiss="modal" >No</button>
                </div>
            </div>
        </div>
    </div>

    <div class="accordion accordion-flush text-extra-dark bg-extra-light bg-opacity-75" id="food_accordian">
        <!-- HEADER W BUTTONS -->
        <div class="accordion-item bg-dark text-light py-3 m-0 row" v-if="user_food.length > 0">
            <div class="col-6 d-flex justify-content-center">
                <button class="btn" :class="{'fw-bold btn-main-secondary-fixed': to_display == 'mine', 'btn-main-light-fixed': to_display != 'mine'}" @click="to_display = 'mine' ">My Buffets</button>
            </div>

            <div class="col-6 d-flex justify-content-center">
                <button class="btn" :class="{'fw-bold btn-main-secondary-fixed': to_display == 'other', 'btn-main-light-fixed': to_display != 'other'}" @click="to_display = 'other' ">Other Buffets</button>
            </div>
        </div>

        <!-- MY BUFFETS -->
        <div v-if="to_display == 'mine' ">
            <!-- V-FOR MY_BUFFETS STARTS HERE -->
            <div class="accordion-item" v-for="(e_buff, index) in user_food" :key="`userfood-${e_buff.post_id}`">
                <h2 class="accordion-header" :id="`mybuff-flush-heading${index}`">
    
                    <!-- HEADER GOES HERE v -->
                    <button class="accordion-button collapsed bg-light" type="button" data-bs-toggle="collapse" :data-bs-target="`#mybuff-flush-collapse${index}`" aria-expanded="false" :aria-controls="`mybuff-flush-collapse${index}`" @click="onPostClick(index+1, e_buff)">
                        <div class="row vw-100">
                            <!-- IMAGE CAROUSEL -->
                            <div class="col-6 col-md-7 col-lg-8">
                                <div :id="`mybuff-foodlist-img-carousel-${e_buff.post_id}`" class="carousel slide" data-bs-ride="carousel">
                                    <div class="carousel-inner" data-bs-interval="2000">
                                        <!-- VFOR IMGS -->
                                        <div class="carousel-item" :class="(img_index==0) ? 'active' : ''" v-for="(e_imgsrc, img_index) in e_buff.img" :key="`userfood-${e_buff.post_id}-${img_index}`">
                                            <img :src="e_imgsrc" class="d-block w-100">
                                        </div>

                                        <!-- PLACEHOLDER IMG -->
                                        <div class="carousel-item active" v-if="e_buff.img.length == 0">
                                            <img :src="placeholder_img_url" class="d-block w-100">
                                        </div>
                                    </div>
        
                                    <button class="carousel-control-prev" type="button" :data-bs-target="`#mybuff-foodlist-img-carousel-${e_buff.post_id}`" data-bs-slide="prev">
                                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                        <span class="visually-hidden">Previous</span>
                                    </button>
                                    <button class="carousel-control-next" type="button" :data-bs-target="`#mybuff-foodlist-img-carousel-${e_buff.post_id}`" data-bs-slide="next">
                                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                        <span class="visually-hidden">Next</span>
                                    </button>
                                </div>
                            </div>

                            <!-- DETAILS -->
                            <div class="col-6 col-md-5 col-lg-4">
                                <div class="row">
                                    <!-- DIET RESTRICTIONS -->
                                    <div class="col-12">
                                        <h6>
                                            <i v-for="(e_diet, index) in e_buff.diets_available" :key="index">
                                                <font-awesome-icon :icon="diet_icons[e_diet]" />&nbsp;
                                            </i>
                                        </h6>
                                    </div>

                                    <!-- TIME LEFT -->
                                    <div class="col-12">
                                        <h6><font-awesome-icon icon="fa-solid fa-hourglass-half" /> {{ e_buff.time_left }} </h6>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </button>
    
                </h2>
                <div :id="`mybuff-flush-collapse${index}`" class="accordion-collapse collapse" :aria-labelledby="`flush-heading${index}`" data-bs-parent="#food_accordian">
                
                <!-- BODY GOES HERE v -->
                <div class="accordion-body bg-light-gradient">
                    <div class="container-fluid">
                        <div class="row">
                            <div class="col-12">
                                <h6>
                                    <font-awesome-icon icon="fa-solid fa-bowl-food" /> {{ e_buff.post_name }}
                                </h6>
                                <h6>
                                    <font-awesome-icon icon="fa-solid fa-location-dot" /> {{ e_buff.address }}
                                </h6>

                                <p>
                                    {{ e_buff.description }}
                                </p>
                            </div>
                            <div class="col-12 d-flex justify-content-center align-items-center">
                                <div>
                                    <button type="button" class="btn btn-warning btn-expand" data-bs-toggle="modal" data-bs-target="#exampleModal" @click="passFoodID(e_buff.post_id)">
                                        <font-awesome-icon icon="fa-solid fa-circle-stop" />&nbsp;&nbsp;End Event
                                    </button>
                                    <!-- <button class="btn btn-warning btn-expand">
                                        <font-awesome-icon icon="fa-solid fa-circle-stop" />&nbsp;&nbsp;End Buffet
                                    </button> -->
                                </div>
                            </div>
                        </div>
                    </div>
                        
                </div>
                </div>
            </div>       
        </div>

        <!-- OTHER BUFFETS -->
        <div v-if="to_display == 'other' ">
            <!-- V-FOR BUFFETS STARTS HERE -->
            <div v-if="food.length > 0">
                <div class="accordion-item" v-for="(e_buff, index) in food" :key="`food-${e_buff.post_id}`">
                    <h2 class="accordion-header" :id="`flush-heading${index}`">
        
                        <!-- HEADER GOES HERE v -->
                        <button class="accordion-button collapsed bg-light" type="button" data-bs-toggle="collapse" :data-bs-target="`#flush-collapse${index}`" aria-expanded="false" :aria-controls="`flush-collapse${index}`" @click="onPostClick(index, e_buff)" :id="`accordionList${index+1}`">
                            <div class="row vw-100">
                                <!-- IMAGE CAROUSEL -->
                                <div class="col-6 col-md-7 col-lg-8">
                                    <div :id="`foodlist-img-carousel-${e_buff.post_id}`" class="carousel slide" data-bs-ride="carousel">
                                        <div class="carousel-inner" data-bs-interval="2000">
                                            <!-- VFOR IMGS -->
                                            <div class="carousel-item" :class="(img_index==0) ? 'active' : ''" v-for="(e_imgsrc, img_index) in e_buff.img" :key="`food-${e_buff.post_id}-${img_index}`">
                                                <img :src="e_imgsrc" class="d-block w-100">
                                            </div>

                                            <!-- PLACEHOLDER IMG -->
                                            <div class="carousel-item active" v-if="e_buff.img.length == 0">
                                                <img :src="placeholder_img_url" class="d-block w-100">
                                            </div>
                                        </div>
            
                                        <button class="carousel-control-prev" type="button" :data-bs-target="`#foodlist-img-carousel-${e_buff.post_id}`" data-bs-slide="prev">
                                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                            <span class="visually-hidden">Previous</span>
                                        </button>
                                        <button class="carousel-control-next" type="button" :data-bs-target="`#foodlist-img-carousel-${e_buff.post_id}`" data-bs-slide="next">
                                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                            <span class="visually-hidden">Next</span>
                                        </button>
                                    </div>
                                </div>

                                <!-- DETAILS -->
                                <div class="col-6 col-md-5 col-lg-4">
                                    <div class="row">
                                        <!-- DIET RESTRICTIONS -->
                                        <div class="col-12">
                                            <h6>
                                                <i v-for="(e_diet, index) in e_buff.diets_available" :key="index">
                                                    <font-awesome-icon :icon="diet_icons[e_diet]" />&nbsp;
                                                </i>
                                            </h6>
                                        </div>

                                        <!-- TIME LEFT -->
                                        <div class="col-12">
                                            <h6><font-awesome-icon icon="fa-solid fa-hourglass-half" /> {{ e_buff.time_left }} </h6>
                                        </div>

                                        <!-- DISTANCE -->
                                        <div class="col-12" v-if="user_lat">
                                            <h6><font-awesome-icon icon="fa-solid fa-person-walking" /> {{ e_buff.distance }}</h6>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </button>
        
                    </h2>

                    <div :id="`flush-collapse${index}`" class="accordion-collapse collapse" :aria-labelledby="`flush-heading${index}`" data-bs-parent="#food_accordian"  :class="`accordionBody${index+1}`">
                    
                        <!-- BODY GOES HERE v -->
                        <div class="accordion-body bg-light-gradient">
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-12">
                                        <h6>
                                            <font-awesome-icon icon="fa-solid fa-bowl-food" /> {{ e_buff.post_name }}
                                        </h6>
                                    </div>
                                    <div class="col-12">
                                        <h6>
                                            <font-awesome-icon icon="fa-solid fa-location-dot" /> {{ e_buff.address }}
                                        </h6>

                                        <p>
                                            {{ e_buff.description }}
                                        </p>
                                    </div>
                                
                                    <div class="col-12 d-flex justify-content-center align-items-center">
                                        <div>
                                            <a :href="`https://www.google.com/maps/dir/${ this.user_lat },${ this.user_long }/${ e_buff.latitude },${ e_buff.longitude }`" target="_blank">
                                                <button class="btn btn-main">
                                                    <font-awesome-icon icon="fa-solid fa-circle-arrow-right" />&nbsp;&nbsp;Route to Buffet
                                                </button>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="accordion-collapse collapse" :aria-labelledby="`flush-heading${index}`" data-bs-parent="#food_accordian" :data-index="`${index+1}`" :id="`flush-collapse${index}`">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else>
                <div class="d-flex align-items-center justify-content-center my-auto fst-italic text-dark" style="height: 90vh; font-size: 23px;">
                    <span class="text-primary"><font-awesome-icon icon="fa-solid fa-heart-crack" /></span>&nbsp;&nbsp;No available food...
                </div>
            </div>
        </div>
    </div>
           
</template>


<script>
    const get_all_food_URL = "http://127.0.0.1:5101/guest/available_food";
    const get_all_user_food_URL = "http://localhost:1112/filter_user";
    const cancel_food_post_URL = "http://localhost:1112/remove";
    const get_all_food_logged_in_URL = "http://127.0.0.1:5101/available_food"

    import axios from "axios";

    // FIREBASE STUFF
    import { initializeApp } from "firebase/app";
    import { getStorage, ref, getDownloadURL, listAll } from 'firebase/storage'
    
    // MITT STUFF
    import emitter from '../mitt/mitt.js'

    const firebaseConfig = {
        apiKey: "AIzaSyA2QXxpg-1ODMfSKKKGdWLrKnDVi1yWFr8",
        authDomain: "makanboleh-1311.firebaseapp.com",
        projectId: "makanboleh-1311",
        storageBucket: "makanboleh-1311.appspot.com",
        messagingSenderId: "269223674891",
        appId: "1:269223674891:web:b089695c57872fc6fab30e",
        measurementId: "G-17HRT79G1H"
    };

    const app = initializeApp(firebaseConfig);
    const storage = getStorage(app);

    export default{
        props: [],

        data() {
            return {
                food: [],
                user_food: [],

                pulling_food: true,
                pulling_my_food: true,

                diet_icons: {
                    'halal': 'fa-solid fa-star-and-crescent',
                    'vegetarian': 'fa-solid fa-leaf',
                    'nobeef': 'fa-solid fa-cow'
                },

                curr_focused: 0,

                user_lat: 1.296168,
                user_long: 103.8500437,

                to_display: 'other',
                foodID: null,
                placeholder_img_url: "https://placehold.co/600x400?text=No+Image"
            }
        },

        methods: {
            onPostClick(index, buff_obj) {
                this.$store.state.foodPostId = index
                // console.log(this.$store.state.foodPostId)

                emitter.emit("zoomHere", {
                    "lat": buff_obj.latitude, 
                    "lng": buff_obj.longitude
                })
            },
            cancelFood() {
                var vm = this
                fetch(`${cancel_food_post_URL}/${this.foodID}`,{
                    method: 'PUT'
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Success:', data);
                        vm.get_all_user_food()
                        vm.get_all_food()
                        emitter.emit('updateFoodlistPosts')
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
            },
            passFoodID(foodID) {
                this.foodID = foodID
                console.log(this.foodID)
                document.querySelector(".modal-backdrop").style.zIndex = 0;
            },
            delete_specific_food_post(food_id) {
                fetch(`${cancel_food_post_URL}/${food_id}`,{
                    method: 'PUT'
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            },
            get_all_food() {
                console.log(`=== [START] get_all_food() ===`)

                var vm = this
                var is_loggedin = this.$store.state.isAuthenticated

                if (is_loggedin) {
                    // USER IS LOGGED IN
                    axios.post(get_all_food_logged_in_URL, {
                        "latitude": this.user_lat,
                        "longitude":this.user_long,
                        "travel_appetite": this.$store.state.user_details.travel_appetite,
                        "dietary_type": (this.$store.state.user_details.dietary_type)=="" ? [] : (this.$store.state.user_details.dietary_type).split(",")
                    })
                    .then(function(response) {
                        console.log("RESPONSE OBJ: ", response.data.data.food_result.data.posts)
                        vm.food = response.data.data.food_result.data.posts
                        vm.pulling_food = false
                        vm.update_buffet_images()
                        vm.update_buffet_distance()
                        vm.update_buffet_time_left()
                    })
                    .catch(function(error) {
                        console.log("get_all_food() error: ", error)
                        vm.pulling_food = false
                        vm.update_buffet_images()
                        vm.update_buffet_distance()
                        vm.update_buffet_time_left()
                    })
                } else {
                    // WHEN USER NOT LOGGED IN
                    axios.post(get_all_food_URL, {
                        "latitude": this.user_lat,
                        "longitude":this.user_long
                    })
                    .then(function(response) {
                        vm.food = response.data.data.food_result.data.posts
                        vm.pulling_food = false
                        vm.update_buffet_images()
                        vm.update_buffet_distance()
                        vm.update_buffet_time_left()
                    })
                    .catch(function(error) {
                        console.log("get_all_food() error: ", error)
                        vm.pulling_food = false
                        vm.update_buffet_images()
                        vm.update_buffet_distance()
                        vm.update_buffet_time_left()
                    })
                }
            },

            get_all_user_food() {
                console.log(`=== [START] get_all_user_food() ===`)

                const response = fetch(`${get_all_user_food_URL}/${this.$store.state.user_details.username}`)
                    .then(response => response.json())
                    .then(data => {
                        console.log("get_all_user_food() response: ", response);
                        if (data.code === 404) {
                            console.log("get_all_user_food() - error!");
                            this.pulling_my_food = false
                            this.update_buffet_images()
                            this.update_buffet_distance()
                            this.update_buffet_time_left()
                        } else {
                            this.user_food = data
                            this.pulling_my_food = false
                            this.update_buffet_images()
                            this.update_buffet_distance()
                            this.update_buffet_time_left()
                        }
                    })
            },

            update_buffet_time_left() {
                // BREAK IF STILL PULLING DATA
                if (this.pulling_food || this.pulling_my_food) {
                    return
                }

                // BREAK IF NOT ON HOME PAGE
                if (this.$route.fullPath != "/") {
                    return
                }

                let curr_time = new Date();

                var temp_food = []

                for (let e_buff of this.food) {
                    // UPDATES TIME_LEFT
                    let end_time = new Date(e_buff.end_time);
    
                    let hr_left = Math.floor( (Math.max(end_time-curr_time, 0)) / 1000 / 60 / 60 );
                    let min_left = Math.floor( (Math.max(end_time-curr_time, 0)) / 1000 / 60 % 60 );
                    let sec_left = Math.floor( (Math.max(end_time-curr_time, 0)) / 1000 % 60 );

                    e_buff.time_left = `${hr_left}hr ${min_left}min ${sec_left}s`;

                    if ((hr_left + min_left + sec_left) != 0) {
                        temp_food.push(e_buff)
                    } else {
                        this.delete_specific_food_post(e_buff.post_id)
                    }
                }

                this.food = temp_food
                temp_food = []

                for (let e_buff of this.user_food) {
                    // UPDATES TIME_LEFT
                    let end_time = new Date(e_buff.end_time);
    
                    let hr_left = Math.floor( (Math.max(end_time-curr_time, 0)) / 1000 / 60 / 60 );
                    let min_left = Math.floor( (Math.max(end_time-curr_time, 0)) / 1000 / 60 % 60 );
                    let sec_left = Math.floor( (Math.max(end_time-curr_time, 0)) / 1000 % 60 );

                    e_buff.time_left = `${hr_left}hr ${min_left}min ${sec_left}s`;

                    if ((hr_left + min_left + sec_left) != 0) {
                        temp_food.push(e_buff)
                    } else {
                        this.delete_specific_food_post(e_buff.post_id)
                    }
                }

                this.user_food = temp_food

                setTimeout(this.update_buffet_time_left, 1000)
            },

            update_buffet_distance() {
                console.log(`=== [START] update_buffet_distance() ===`)
                
                // BREAK IF STILL PULLING DATA
                if (this.pulling_food || this.pulling_my_food) {
                    console.log("update_buffet_distance() - Not done uploading")
                    return
                }

                console.log("update_buffet_distance() - this.food: ", this.food)

                for (let e_buff of this.food) {
                    // UPDATES DISTANCE
                    let target_lat = e_buff.latitude
                    let target_long = e_buff.longitude
                    let distance_km = this.get_distance_km(target_lat, target_long, this.user_lat, this.user_long)

                    if (distance_km >= 1) {
                        e_buff.distance = distance_km.toFixed(1).toString() + "km"
                    } else {
                        e_buff.distance = Math.round(distance_km * 1000).toString() + 'm'
                    }
                }

                console.log(`=== [END] update_buffet_distance() ===`)
            },

            update_buffet_images() {
                console.log(`=== [START] update_buffet_images() ===`)
                
                // BREAK IF STILL PULLING DATA
                if (this.pulling_food || this.pulling_my_food) {
                    console.log("update_buffet_images() - Not done uploading")
                    return
                }

                var img_arr = []

                for (let e_buff of this.food) {
                    img_arr = this.return_buffet_imgs_arr(e_buff.post_id)
                    e_buff.img = img_arr
                }

                for  (let e_buff of this.user_food) {
                    img_arr = this.return_buffet_imgs_arr(e_buff.post_id)
                    e_buff.img = img_arr
                }

                console.log(`=== [END] update_buffet_images() ===`)
            },

            current_expanded() {
                console.log(`=== [START] expanded() ===`)
                
                let accordian_elem = document.getElementById("food_accordian")

                if (accordian_elem == null) {return -1}

                let accordian_children = accordian_elem.children

                let e_idx = -1

                for (let e_child of accordian_children) {
                    e_idx += 1

                    let is_expanded = e_child.querySelector(`[aria-expanded='true']`)
                    
                    if (is_expanded) {
                        return e_idx
                    }
                }

                return -1
            },
            update_user_latlong(position) {
                console.log(`=== [START] update_user_latlong() ===`)
                
                this.user_lat = position.coords.latitude
                this.user_long =  position.coords.longitude
                this.get_all_food()
                this.get_all_user_food()
                this.update_buffet_distance()

                console.log(`=== [END] update_user_latlong() ===`)
            },

            getLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(this.update_user_latlong);
                } else {
                    this.user_lat = 1.296168
                    this.user_long = 103.8500437
                }
            },

            get_distance_km(lat1, lon1, lat2, lon2) {
                var R = 6371; // Radius of the earth in km
                var dLat = this.deg2rad(lat2-lat1);  // deg2rad below
                var dLon = this.deg2rad(lon2-lon1); 
                var a = 
                    Math.sin(dLat/2) * Math.sin(dLat/2) +
                    Math.cos(this.deg2rad(lat1)) * Math.cos(this.deg2rad(lat2)) * 
                    Math.sin(dLon/2) * Math.sin(dLon/2)
                    ; 
                var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
                var d = R * c; // Distance in km
                return d;
            },

            deg2rad(deg) {
                return deg * (Math.PI/180)
            },

            return_buffet_imgs_arr(food_id) {
                // retrieve a list of imges from firebase storage
                var to_return = []

                // test reference to the folder
                const list_ref = ref(storage, `${food_id}/`)

                listAll(list_ref)
                .then((res) => {
                res.items.forEach((itemRef) => {
                    // All the items under listRef.
                    // console.log(res.items.length)

                    getDownloadURL(itemRef)
                    .then((url) => {
                        // `url` is the download URL for testphoto
                        console.log(`return_buffet_imgs_arr() url: ${url}`)
                        to_return.push(url)
                    })
                    .catch((error) => {
                        // Handle any errors
                        console.log("return_buffet_imgs_arr() error: ", error)
                    });
                });
                }).catch((error) => {
                    // Uh-oh, an error occurred!
                    console.log("return_buffet_imgs_arr() error: ", error)
                });

                console.log(`=== [END] return_buffet_imgs_arr(${food_id}) ===`)
                return to_return
            },
        },

        mounted() {
            var vm = this
            emitter.on('updateFoodlistPosts', function(){
                console.log("EMITTING NOW FROM FOODLIST.VUE=========")
                vm.get_all_food()
                vm.get_all_user_food()
            })
        },

        created() {
            this.getLocation();
            this.get_all_food();
            this.get_all_user_food();
        }
    }
</script>


<style scoped>
    .modal-header {
        text-align: center;
    }

    .btn-size {
        width: 100px;
    }

    /* Up to LG */
    @media (max-width: 769px) {
        #food_accordian{
            /* position: fixed;
            bottom: 0;
            right: 0;
            left: 0; */
            margin-top: 25px;
            overflow-y: scroll;
            max-height: 40vh;
            transition: all .8s ease-in-out;
            border-radius: 12px 12px 0px 0px;
        }

        #food_accordian:has(.accordion-button[aria-expanded='true']) {
            max-height: 60vh;
        }
    }

    /* Past LG */
    @media (min-width: 769px) {
        #food_accordian{
            position: absolute;
            bottom: 0;
            left: 0;
            overflow-y: scroll;
            height: 100%;
            width: 40vw;
        }
    }
    img{
        aspect-ratio: 120/ 70;
        object-fit: cover;
        border-radius: 10px;
    }

    .accordion-button[aria-expanded='true'] {
        background-color: #FFC23F !important;
        color: #1e2e1e;
    }

</style>