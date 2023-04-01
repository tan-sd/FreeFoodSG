<template>
    <button class="btn btn-main" data-bs-toggle="modal" :data-bs-target="isAuthenticated ? `#new-foodpost` : ``" @click="reroute_to_login()"><font-awesome-icon icon="fa-solid fa-utensils" /> Share Food</button>
    
    <div class="modal fade" id="new-foodpost" tabindex="-1" aria-labelledby="modal-title-foodform" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content bg-light text-dark">
          <!-- TITLE AND CLOSE BTN -->
          <div class="modal-header bg-dark text-extra-light">
            <h5 class="modal-title" id="modal-title-foodform"><font-awesome-icon icon="fa-solid fa-utensils" /> Create Food Post</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>

          <!-- FORM -->
          <div class="modal-body justify-content-center">
            <form>
              <!-- POST TITLE -->
              <div class="form-floating mb-3">
                  <input type="text" class="form-control" id="floatingInput" placeholder="Title" v-model="post_title">
                  <label for="floatingInput">Title</label>
              </div>
              
              <!-- POST DESC -->
              <div class="form-floating mb-3">
                  <textarea class="form-control" id="floatingInput" placeholder="Description" style="height: 80px; resize: none;" v-model="post_desc"></textarea>
                  <label for="floatingInput">Description</label>
              </div>
  
              <!-- POST ADDRESS -->
              <div class="form-floating mb-3">
                  <GMapAutocomplete
                      class="form-control"
                      placeholder=" "
                      id="googlemap_autocomplete_foodform"
                      type="text"
                      :options="autoCompleteOptions"
                      @place_changed="setPlace"
                  >
                  </GMapAutocomplete>

                  <label for="googlemap_autocomplete_foodform"><font-awesome-icon icon="fa-solid fa-location-dot" />&nbsp;Location</label>
              </div>

              <!-- DATETIME -->
              <VueDatePicker v-model="post_datetime" :format="format" placeholder="Buffet End Time" utc></VueDatePicker>
  
              <!-- Dietary Restrictions START -->
              <div class="d-flex justify-content-center mt-3">
                <div class="form-check mx-2">
                    <input class="form-check-input" type="checkbox" value="halal" id="foodform-halal-checkbox" v-model="diet_res">
                    <label class="form-check-label" for="foodform-halal-checkbox">
                      <font-awesome-icon icon="fa-solid fa-star-and-crescent" />&nbsp;Halal
                    </label>
                </div>
    
                <div class="form-check mx-2">
                    <input class="form-check-input" type="checkbox" value="vegetarian" id="foodform-vege-checkbox" v-model="diet_res">
                    <label class="form-check-label" for="foodform-vege-checkbox">
                      <font-awesome-icon icon="fa-solid fa-leaf" />&nbsp;Vegetarian
                    </label>
                </div>
    
                <div class="form-check mx-2">
                    <input class="form-check-input" type="checkbox" value="nobeef" id="foodform-nobeef-checkbox" v-model="diet_res">
                    <label class="form-check-label" for="foodform-nobeef-checkbox">
                      <font-awesome-icon icon="fa-solid fa-cow" />&nbsp;No Beef
                    </label>
                </div>
              </div>
              <!-- Dietary Restrictions END -->
  
              <!-- UPLOAD IMG -->
              <div class="input-group custom-file-button my-4">
                  <label class="input-group-text bg-dark text-extra-light" for="foodform-upload-img-btn">
                    <font-awesome-icon icon="fa-solid fa-image" />&nbsp;Upload Image
                  </label>
                  
                  <input class="form-control" type="file" id="foodform-upload-img-btn" accept="image/*" multiple>
              </div>
  
              <!-- SUBMIT BTN -->
              <div class="d-flex justify-content-center mt-3">
                  <button class="btn btn-main" type="button" @click="submit_new_post()"><font-awesome-icon icon="fa-solid fa-paper-plane" />&nbsp;&nbsp;Post</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
  import router from '@/router';
  import axios from 'axios';
  import VueDatePicker from '@vuepic/vue-datepicker';
  import '@vuepic/vue-datepicker/dist/main.css';

  // Firebase Stuff
  // Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getStorage, ref, uploadBytes } from 'firebase/storage'
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
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
    components: { VueDatePicker },
    data() {
      return{
        post_location: '',
        post_lat: null,
        post_lng: null,
        post_title: '',
        post_desc: '',
        diet_res: [],
        post_datetime: '',
        month_list: [
          'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ],

        autoCompleteOptions: {
            componentRestrictions: {
                country: ["sg"],
            }
        },
      }
    },
    computed: {
      isAuthenticated() {
        // console.log(this.$store.getters.isAuthenticated)
        return this.$store.getters.isAuthenticated;
      }
    },

    methods: {
      reroute_to_login() {
        if (!this.isAuthenticated) {
          router.push({path: '/login'})
        }
      },

      setPlace(place) {
        this.post_location = place.formatted_address
        this.post_lat = place.geometry.location.lat()
        this.post_lng = place.geometry.location.lng()
      },

      submit_new_post() {
        console.log(`=== [START] submit_new_post() ===`)

        //Handle errors
        if (
            this.post_location === '' ||
            this.post_title === '' ||
            this.post_desc === ''
        ) {
            console.log("FIELDS NOT FILLED ====")
            console.log(`=== [END] submit_new_post() ===`)
            return false
        }

        //Continue wo errors
        var vm = this

        axios.post("http://localhost:5100/post", {
            "username": this.$store.state.user_details.username,
            "post_name": this.post_title,
            "latitude": this.post_lat,
            "longitude": this.post_lng,
            "address": this.post_location,
            "description": this.post_desc,
            "end_time" : this.post_datetime.split(".")[0],
            "diets_available": this.diet_res
        })
        .then(function (response) {
            console.log("Success: ", response)
            console.log(`=== [END] submit_new_post() ===`)
            var generated_post_id = response.data.data.post_status.data.post.post_id

            vm.upload_img(generated_post_id)
        })
        .catch(function(error) {
            console.log(error)
            console.log(`=== [END] submit_new_post() ===`)
        })
      },

      format(date) {
        const today = new Date()
        var day_ends = ""

        if (
          date.getFullYear() === today.getFullYear() &&
          date.getMonth() === today.getMonth() &&
          date.getDate() === today.getDate()
        ) {
          day_ends = 'today'
        } else {
          const day = date.getDate();
          const month = this.month_list[date.getMonth()];
          const year = date.getFullYear();
          
          day_ends = `${day} ${month} ${year}`
        }

        return `Buffet ends ${day_ends} at ${date.getHours()}:${date.getMinutes()}`;
      },

      upload_img(food_id) {
        console.log(`=== [START] upload_img() ===`)
        var img_files = document.getElementById("foodform-upload-img-btn").files
        
        // for loop to upload each file selected
        for(let i = 0; i< img_files.length; i++){
            // upload img to firebase storage
            // the input "input_file" takes in a "File" object data type
            var img_file = img_files[i]

            // step 1: define what file you want to label this image as
            // (put it as the food ID)
            var file_name = `${food_id}/img_${i}`

            // step 2: nothing, the code will take care of the rest
            var uploadRef = ref(storage, file_name)
            uploadBytes(uploadRef, img_file).then(() => {
                console.log('Uploaded a blob or file!');
                console.log('this is file number ' + i)
            })
        }
      }
    }
  }
</script>

<style scoped>
  .custom-file-button input[type="file"]{
      margin-left: -2px !important;
  }

  .custom-file-button input[type="file"]:hover label{
        background-color: #dde0e3;
        cursor: pointer;
  }

  .custom-file-button input[type="file"]::-webkit-file-upload-button {
      display: none;
  }

  .custom-file-button input[type="file"]::file-selector-button {
      display: none;
  }
</style>

<style>
  .pac-container {
        z-index: 10000 !important;
    }
  
  ::-webkit-scrollbar {
    display: none;
    }
</style>