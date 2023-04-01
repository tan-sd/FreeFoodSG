// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-analytics.js";
import { getStorage, ref, getDownloadURL, uploadBytes } from 'https://www.gstatic.com/firebasejs/9.18.0/firebase-storage.js'
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

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Initialize Cloud Storage and get a reference to the service
const storage = getStorage(app);

// add a reference pointer to the particular file you want in the storage by using
// this syntax, ref(storage, "file_name")
const storageRef = ref(storage);


const root = Vue.createApp({
    data() {
        return{
            img_name: ""
        }
    },
    
    methods: {
        retrieve_img(){
            // retrieve an img from firebase storage

            // test reference
            const testphoto = ref(storage, "cambodian_tourist.jpg")
        
            // get download url to get your img
            getDownloadURL(testphoto)
            .then((url) => {
                // `url` is the download URL for testphoto
    
                const img = document.getElementById('myimg');
                img.setAttribute('src', url);
            })
            .catch((error) => {
                // Handle any errors
                console.log(error)
                console.log("you got an error")
            });
        },
        
        format_file(){
            console.log(document.getElementById("img_input").files[0])
            var img_file = document.getElementById("img_input").files[0]

            this.upload_img(img_file)
        },

        upload_img(input_file){
            // upload img to firebase storage
            // the input "input_file" takes in a "File" object data type

            // step 1: define what file you want to label this image as
            // (put it as the food ID)
            var file_name = "food_ID"

            // step 2: nothing, the code will take care of the rest
            var uploadRef = ref(storage, file_name)
            uploadBytes(uploadRef, input_file).then((snapshot) => {
                console.log('Uploaded a blob or file!');
            }); 
        }
    }


})


//Mount
root.mount('#mount')
