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
            :icon="m.icon"
        />
        <GMapCircle
            :radius="2000"
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
    const food_info_url = 'http://localhost:1112/all'
    // const guest_url = 'http://localhost:1112/nearby_food'
    export default {
        inheritAttrs: true,
        methods: {
            onInput() {
                this.showClearButton = this.$refs.autocomplete.$refs.input.value.length > 0;
            },
            // Adam, will need you to use this function and pass the values from FoodList.vue line 167 to the panTo() function
            // the values should be in the form of a JSON object, can refer to line 143 in this vue file.
            re_center() {
                const map = this.$refs.map
                map.panTo(this.currentLocation)
                this.zoomValue = 15
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
                // return all regardless of user or guest
                axios.get(`${food_info_url}`, {
                        latitude: this.markers[0].position.lat,
                        longitude: this.markers[0].position.lng
                })
                    .then(response => {
                        // this response stores the JSON returned as {"code", "data": {"data": {"food"}}}
                        // console.log(response.data.data.food)
                        var foods = response.data.data.food
                        // store each food JSON in the markers array
                        for (let i = 0; i<foods.length; i++) {
                            this.markers.push({
                                            position: {
                                                lat: foods[i].latitude,
                                                lng: foods[i].longitude,
                                            },
                                            post_id: foods[i].post_id,
                                            icon: require("../assets/images/flaticon/food.png")
                                        })
                        }
                        console.log("All markers created!")
                    })
                    .catch(error => {
                        console.log(error.message);
                        console.log(error.response.data.code == 404)
                        document.getElementById("errors").innerHTML = error.response.data.msg
                    });
                // check if user is a guest
                // if (!this.$store.state.isAuthenticated) {
                //     console.log("It's a guest user! Calling food post for guest.")
                //     axios.get(`${guest_url}`, {
                //         latitude: this.markers[0].position.lat,
                //         longitude: this.markers[0].position.lng
                // })
                //     .then(response => {
                //         // this response stores the JSON returned as {"code", "data": {"data": {"food"}}}
                //         // console.log(response.data.data.food)
                //         var foods = response.data.data.food
                //         // store each food JSON in the markers array
                //         for (let i = 0; i<foods.length; i++) {
                //             this.markers.push({
                //                             position: {
                //                                 lat: foods[i].latitude,
                //                                 lng: foods[i].longitude,
                //                             },
                //                             post_id: foods[i].post_id,
                //                             icon: require("../assets/images/flaticon/food.png")
                //                         })
                //         }
                //         console.log("All markers created!")
                //     })
                //     .catch(error => {
                //         console.log(error.message);
                //         console.log(error.response.data.code == 404)
                //         document.getElementById("errors").innerHTML = error.response.data.msg
                //     });
                // } else {
                //     console.log("It's a registered user! Calling food post for user.")
                //     axios.get(`${food_info_url}`, {
                //         latitude: this.markers[0].position.lat,
                //         longitude: this.markers[0].position.lng,
                //         travel_appetite: this.$store.state.user_details.travel_appetite
                // })
                //     .then(response => {
                //         // this response stores the JSON returned as {"code", "data": {"data": {"food"}}}
                //         // console.log(response.data.data.food)
                //         var foods = response.data.data.food
                //         // store each food JSON in the markers array
                //         for (let i = 0; i<foods.length; i++) {
                //             this.markers.push({
                //                             position: {
                //                                 lat: foods[i].latitude,
                //                                 lng: foods[i].longitude,
                //                             },
                //                             post_id: foods[i].post_id,
                //                             icon: require("../assets/images/flaticon/food.png")
                //                         })
                //         }
                //         console.log("All markers created!")
                //     })
                //     .catch(error => {
                //         console.log(error.message);
                //         console.log(error.response.data.code == 404)
                //         document.getElementById("errors").innerHTML = error.response.data.msg
                //     });
                console.log(this.markers[0].position.lat)
                
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
            });
            console.log("Got user's current location")
            console.log("Getting food post information from dB")
            this.get_nearest_food()
            console.log("Got food post information from dB")
        },
        data() {
            return {
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