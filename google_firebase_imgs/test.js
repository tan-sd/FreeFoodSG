// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-analytics.js";
import { getStorage, ref, getDownloadURL, uploadBytes, listAll } from 'https://www.gstatic.com/firebasejs/9.18.0/firebase-storage.js'
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
            const testphoto = ref(storage, "tuk_tuk.jpg")
        
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

        retrieve_list(){
            // retrieve a list of imges from firebase storage

            // test reference to the folder
            const list_ref = ref(storage, "cambodia/")

            listAll(list_ref)
            .then((res) => {
              res.prefixes.forEach((folderRef) => {
                // All the prefixes under listRef.
                // You may call listAll() recursively on them.
                console.log(folderRef)
              });
              res.items.forEach((itemRef) => {
                // All the items under listRef.
                console.log(res.items.length)
                console.log(itemRef)    
                getDownloadURL(itemRef)
                .then((url) => {
                    // `url` is the download URL for testphoto
        
                    const img = document.getElementById('listimg');
                    img.innerHTML += "<img src='" + url + "' class='img-fluid'>"
                    
                })
                .catch((error) => {
                    // Handle any errors
                    console.log(error)
                    console.log("you got an error")
                });
              });
            }).catch((error) => {
              // Uh-oh, an error occurred!
              console.log(error)
            });
        },

        upload_img(){
            console.log(document.getElementById("img_input").files[0])
            var img_files = document.getElementById("img_input").files
            
            // for loop to upload each file selected
            for(let i = 0; i< img_files.length; i++){
                // upload img to firebase storage
                // the input "input_file" takes in a "File" object data type
                var img_file = img_files[i]

                // step 1: define what file you want to label this image as
                // (put it as the food ID)
                var file_name = "file_" + i

                // step 2: nothing, the code will take care of the rest
                var uploadRef = ref(storage, file_name)
                uploadBytes(uploadRef, img_file).then((snapshot) => {
                    console.log('Uploaded a blob or file!');
                    console.log('this is file number ' + i)
                })
            }
        }
    }


})


//Mount
root.mount('#mount')
