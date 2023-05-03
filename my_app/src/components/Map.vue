<template>
    <div id="map">
        <GMapMap
            ref="map"
            v-bind="$attrs"
            :center="center"
            :zoom="zoomValue"
            map-type-id="terrain"
            :options="GMapOptions"
            class="map"
        >
        <GMapMarker
            class="current-location-marker"
            :key="index"
            v-for="(m, index) in markers"
            :position="m.position"
            :icon="{
                url: m.icon,
                scaledSize: m.scaledSize
            }"
            @click="toggleAccordion(index)"
        />
        <GMapCircle
            :radius="this.user_appetite*100"
            :center="currentLocation"
            :options="circleOptions"
        />
        </GMapMap>
    </div>

    <div class="autocomplete d-flex">
            <div class="form-floating mt-3 ms-3">
                <GMapAutocomplete
                    ref="autocomplete"
                    type="text"
                    @place_changed="setPlace"
                    :options="autoCompleteOptions"
                    :value="this.search"
                    placeholder=" "
                    class="form-control bg-autocomplete"
                    id="googleAutocomplete"
                    @input="onInput"
                    >
                </GMapAutocomplete>

                <label for="googleAutocomplete" class="text-dark">
                    <font-awesome-icon icon="fa-solid fa-pizza-slice" />&nbsp;&nbsp;Search Here
                </label>
            </div>

            <button
                id="clear-button"
                class="text-dark"
                @click="clear_search"
                v-if="showClearButton">
                <font-awesome-icon icon="fa-solid fa-xmark" />
            </button>
            <button @click="re_center()" class="text-dark bg-recenter ms-1 mt-4 rounded btn btn-light">
                <font-awesome-icon icon="fa-solid fa-crosshairs" />
            </button>
        </div>
  </template>

  <script>
    import axios from 'axios' 

    // MITT STUFF
    import emitter from '../mitt/mitt.js'

    const food_info_guest_url = 'http://127.0.0.1:5101/guest/available_food'
    const get_user_info_url = 'http://localhost:1111/profile'
    const get_all_food_logged_in_URL = "http://127.0.0.1:5101/available_food"
    // const guest_url = 'http://localhost:1112/nearby_food'
    export default {
        inheritAttrs: true,
        methods: {
            get_user_info(username) {
                // console.log(`${get_user_info_url}/${username}`)
                const response = fetch(`${get_user_info_url}/${username}`)
                    .then(response => response.json())
                    .then(data => {
                        console.log("get_user_info() -", response);
                        if (data.code === 404) {
                            console.log("get_user_info() - error!");
                        } else {
                            this.user_appetite = data.data.travel_appetite
                            // console.log(this.user_appetite)
                        }
                    })
            },
            toggleAccordion(index) {
                this.$store.state.markerId = index
                // console.log(this.$store.state.markerId)
                // console.log(`#accordionList${index}`)
                const selectedAccordion = document.querySelector(`#accordionList${index}`)
                // console.log(selectedAccordion)
                selectedAccordion.setAttribute('aria-expanded',"true")
                selectedAccordion.classList.remove('collapsed')

                const selectedAccordionBody = document.querySelector(`.accordionBody${index}`)
                // console.log(selectedAccordionBody)
                selectedAccordionBody.classList.add('show')
                // const accordionElement = this.$refs.index
                // accordionElement.classList.toggle('active')
            },
            onInput() {
                this.showClearButton = this.$refs.autocomplete.$refs.input.value.length > 0;
            },
            // Adam, will need you to use this function and pass the values from FoodList.vue line 167 to the panTo() function
            // the values should be in the form of a JSON object, can refer to line 143 in this vue file.
            re_center() {
                const map = this.$store.state.mapobj
                map.panTo(this.currentLocation)
                this.zoomValue = 14
            },
            re_center_custom(latlng) {
                console.log(`=== [START] re_center_custom(lat: ${latlng.lat}, lng: ${latlng.lng}) ===`)

                const map = this.$store.state.mapobj

                console.log("MAP: ", map)

                map.panTo({
                    "lat": latlng.lat,
                    "lng": latlng.lng 
                })
                this.zoomValue = 14
            },
            clear_search() {
                this.$refs.autocomplete.$refs.input.value = '';
                this.showClearButton = false
            },
            setPlace(place) {
                // this.actLocation = place.name;
                this.center = {
                    lat: place.geometry.location.lat(),
                    lng: place.geometry.location.lng(),
                }
            },
            async get_location() {
                return new Promise((resolve, reject) => {
                    navigator.geolocation.getCurrentPosition(resolve, reject);
                });
            },
            // '''
            // Function: getting all nearest food post
            // Input: user  current lat, lng from markers[0]
            // Output: all food posts will be stored from markers[1] onwards
            // '''
            async get_nearest_food() {
                var data_to_pass = {}

                // return GUEST
                if (!(this.$store.state.isAuthenticated)) {

                    data_to_pass = {
                            "latitude": this.markers[0].position.lat,
                            "longitude": this.markers[0].position.lng
                    }
    
                    axios.post(food_info_guest_url, data_to_pass)
                    .then(response => {
                        var foods = response.data.data.food_result.data.posts
                        this.markers = [this.markers[0] ]
                        // store each food JSON in the markers array
                        for (let i = 0; i<foods.length; i++) {
                            this.markers.push({
                                position: {
                                    lat: foods[i].latitude,
                                    lng: foods[i].longitude,
                                },
                                post_id: foods[i].post_id,
                                icon: require("../assets/images/flaticon/food.png"),
                                scaledSize: {width: 45, height: 45}
                            })
                        }
                        console.log("All markers created!")
                    })
                    .catch(error => {
                        console.log(error.message);
                        console.log(error.response.data.code == 404)
                        document.getElementById("errors").innerHTML = error.response.data.msg
                    });
                }
                // return LOGGED IN USER
                else {
                    data_to_pass = {
                        "latitude": this.markers[0].position.lat,
                        "longitude": this.markers[0].position.lng,
                        "travel_appetite": this.$store.state.user_details.travel_appetite,
                        "dietary_type": (this.$store.state.user_details.dietary_type)=="" ? [] : (this.$store.state.user_details.dietary_type).split(",")
                    }
    
                    axios.post(get_all_food_logged_in_URL, data_to_pass)
                    .then(response => {
                        var foods = response.data.data.food_result.data.posts
                        this.markers = [this.markers[0] ]
                        // store each food JSON in the markers array
                        for (let i = 0; i<foods.length; i++) {
                            this.markers.push({
                                position: {
                                    lat: foods[i].latitude,
                                    lng: foods[i].longitude,
                                },
                                post_id: foods[i].post_id,
                                icon: require("../assets/images/flaticon/food.png"),
                                scaledSize: {width: 45, height: 45}
                            })
                        }
                        console.log("All markers created!")
                    })
                    .catch(error => {
                        console.log(error.message);
                        console.log(error.response.data.code == 404)
                        document.getElementById("errors").innerHTML = error.response.data.msg
                    });
                }    
            }
        },
        mounted() {
            console.log("Getting user's current location")
            this.get_location().then(position => {
                this.markers[0].position.lat = position.coords.latitude;
                this.markers[0].position.lng = position.coords.longitude;
                this.center.lat = position.coords.latitude;
                this.center.lng = position.coords.longitude;
                this.currentLocation.lat = position.coords.latitude;
                this.currentLocation.lng = position.coords.longitude;
                this.get_user_info(this.$store.state.user_details.username)
                console.log("Getting food post information from dB")
                this.get_nearest_food()
                console.log("Got food post information from dB")

                this.$store.state.mapobj = this.$refs.map
            });
            console.log("Got user's current location")

            var vm = this
            emitter.on('updateFoodlistPosts', function(){
                console.log("RECEIVING UpdateFoodListPosts FROM MAP.VUE =========")
                vm.get_nearest_food()
            })

            emitter.on('zoomHere', function(latlng){
                console.log(`RECEIVING zoomHere FROM MAP.VUE (lat: ${latlng.lat}, lng: ${latlng.lng}) ========="`)
                vm.re_center_custom(latlng)
            })
        },
        data() {
            return {
                // appetites: {
                //     Near: 1000,
                //     Medium: 2500,
                //     Far: 5000,
                // },
                user_appetite: null,
                username: null,
                showClearButton: false,
                search: '',
                actLocation: "",
                currentLocation: {
                    lat: 1.300270,
                    lng: 103.851959,
                },
                currentLat: "",
                currentLng: "",
                zoomValue: 14,
                center: {lat: 1.300270, lng: 103.851959},
                markers:
                [
                    {
                        position: {
                            lat: null,
                            lng: null,
                        },
                        
                    }
                ],
                autoCompleteOptions: {
                    componentRestrictions: {
                        country: ["sg"],
                    }
                },
                GMapOptions: {
                    zoomControl: false,
                    mapTypeControl: false,
                    scaleControl: false,
                    streetViewControl: false,
                    rotateControl: false,
                    fullscreenControl: false,
                    styles: [
                        {
                            "elementType": "geometry",
                            "stylers": [
                            {
                                "color": "#ebe3cd"
                            }
                            ]
                        },
                        {
                            "elementType": "labels.text.fill",
                            "stylers": [
                            {
                                "color": "#523735"
                            }
                            ]
                        },
                        {
                            "elementType": "labels.text.stroke",
                            "stylers": [
                            {
                                "color": "#f5f1e6"
                            }
                            ]
                        },
                        {
                            "featureType": "administrative",
                            "elementType": "geometry.stroke",
                            "stylers": [
                            {
                                "color": "#c9b2a6"
                            }
                            ]
                        },
                        {
                            "featureType": "administrative.land_parcel",
                            "elementType": "geometry.stroke",
                            "stylers": [
                            {
                                "color": "#dcd2be"
                            }
                            ]
                        },
                        {
                            "featureType": "administrative.land_parcel",
                            "elementType": "labels.text.fill",
                            "stylers": [
                            {
                                "color": "#ae9e90"
                            }
                            ]
                        },
                        {
                            "featureType": "landscape.natural",
                            "elementType": "geometry",
                            "stylers": [
                            {
                                "color": "#dfd2ae"
                            }
                            ]
                        },
                        {
                            "featureType": "poi",
                            "elementType": "geometry",
                            "stylers": [
                            {
                                "color": "#dfd2ae"
                            }
                            ]
                        },
                        {
                            "featureType": "poi",
                            "elementType": "labels.text.fill",
                            "stylers": [
                            {
                                "color": "#93817c"
                            }
                            ]
                        },
                        {
                            "featureType": "poi.business",
                            "stylers": [
                            {
                                "visibility": "off"
                            }
                            ]
                        },
                        {
                            "featureType": "poi.park",
                            "elementType": "geometry.fill",
                            "stylers": [
                            {
                                "color": "#a5b076"
                            }
                            ]
                        },
                        {
                            "featureType": "poi.park",
                            "elementType": "labels.text",
                            "stylers": [
                            {
                                "visibility": "off"
                            }
                            ]
                        },
                        {
                            "featureType": "poi.park",
                            "elementType": "labels.text.fill",
                            "stylers": [
                            {
                                "color": "#447530"
                            }
                            ]
                        },
                        {
                            "featureType": "road",
                            "elementType": "geometry",
                            "stylers": [
                            {
                                "color": "#f5f1e6"
                            }
                            ]
                        },
                        {
                            "featureType": "road.arterial",
                            "elementType": "geometry",
                            "stylers": [
                            {
                                "color": "#fdfcf8"
                            }
                            ]
                        },
                        {
                            "featureType": "road.arterial",
                            "elementType": "labels",
                            "stylers": [
                            {
                                "visibility": "off"
                            }
                            ]
                        },
                        {
                            "featureType": "road.highway",
                            "elementType": "geometry",
                            "stylers": [
                            {
                                "color": "#f8c967"
                            }
                            ]
                        },
                        {
                            "featureType": "road.highway",
                            "elementType": "geometry.stroke",
                            "stylers": [
                            {
                                "color": "#e9bc62"
                            }
                            ]
                        },
                        {
                            "featureType": "road.highway",
                            "elementType": "labels",
                            "stylers": [
                            {
                                "visibility": "off"
                            }
                            ]
                        },
                        {
                            "featureType": "road.highway.controlled_access",
                            "elementType": "geometry",
                            "stylers": [
                            {
                                "color": "#e98d58"
                            }
                            ]
                        },
                        {
                            "featureType": "road.highway.controlled_access",
                            "elementType": "geometry.stroke",
                            "stylers": [
                            {
                                "color": "#db8555"
                            }
                            ]
                        },
                        {
                            "featureType": "road.local",
                            "stylers": [
                            {
                                "visibility": "off"
                            }
                            ]
                        },
                        {
                            "featureType": "road.local",
                            "elementType": "labels.text.fill",
                            "stylers": [
                            {
                                "color": "#806b63"
                            }
                            ]
                        },
                        {
                            "featureType": "transit.line",
                            "elementType": "geometry",
                            "stylers": [
                            {
                                "color": "#dfd2ae"
                            }
                            ]
                        },
                        {
                            "featureType": "transit.line",
                            "elementType": "labels.text.fill",
                            "stylers": [
                            {
                                "color": "#8f7d77"
                            }
                            ]
                        },
                        {
                            "featureType": "transit.line",
                            "elementType": "labels.text.stroke",
                            "stylers": [
                            {
                                "color": "#ebe3cd"
                            }
                            ]
                        },
                        {
                            "featureType": "transit.station",
                            "elementType": "geometry",
                            "stylers": [
                            {
                                "color": "#dfd2ae"
                            }
                            ]
                        },
                        {
                            "featureType": "water",
                            "elementType": "geometry.fill",
                            "stylers": [
                            {
                                "color": "#b9d3c2"
                            }
                            ]
                        },
                        {
                            "featureType": "water",
                            "elementType": "labels.text.fill",
                            "stylers": [
                            {
                                "color": "#92998d"
                            }
                            ]
                        }
                    ]
                },
                circleOptions: {
                    strokeWeight: 0,
                    fillColor: "#4285F4",
                    fillOpacity: 0.2,
                    clickable: false,
                    zIndex: -1,
                },
            }
        },
    }
    </script>


<style scoped>
#map{
    height: 100%;
    overflow: hidden;
}

.bg-autocomplete{
    background-color: white;
    opacity: 90%;
    width: 86vw;
}

.bg-recenter {
    background-color: white;
    opacity: 90%;
    width: 40px;
    height: 40px;
}

#clear-button {
    position: absolute;
    outline: none;
    border: none;
    background-color: transparent;
    top: 32px;
}

/* Up to LG */
@media (max-width: 769px) {
    .autocomplete{
        position: absolute;
        top: 0;
    }

    .map{
        height: calc(100% + 24px);
        width: 100vw;
        position: absolute;
    }

    #clear-button {
        right: 60px;
    }
}

/* Past LG */
@media (min-width: 769px) {
    .autocomplete{
        position: absolute;
        top: 0;
        margin-left: 40%;
    }

    .bg-autocomplete{
        background-color: white;
        opacity: 90%;
        width: 53vw;
    }

    .map{
        height: 100%;
        width: 140vw;
    }

    #clear-button {
        right: 60px;
    }
}

@keyframes pulse {
  0% {
    transform: scale(0.1);
    opacity: 0.7;
  }
  70% {
    transform: scale(1);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 0;
  }
}

</style>