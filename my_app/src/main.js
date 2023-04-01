import { createApp } from "vue";
import App from "./App.vue";
import router from './router';
import VueGoogleMaps from '@fawmi/vue-google-maps';
import { GoogleSignInPlugin } from "vue3-google-signin";
import "../styling/sass/main.min.css";
import "../styling/style.css";
import store from './store';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { faBars, faBurger, faCircleArrowRight, faCircleStop, faCow, faHourglassHalf, faLeaf, faLocationDot, faPersonWalking, faPizzaSlice, faPlus, faStarAndCrescent, faUserSecret, faUtensils, faCrosshairs, faXmark, faCircleUser, faComments, faPaperPlane, faImage, faSpinner, faBowlFood, faFaceSadTear } from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(faSpinner, faCircleUser ,faPizzaSlice, faUserSecret, faLocationDot, faStarAndCrescent, faLeaf, faCow, faHourglassHalf, faPlus, faUtensils, faBurger, faBars, faPersonWalking, faCircleArrowRight ,faCircleStop, faCrosshairs, faXmark, faComments, faPaperPlane, faImage, faBowlFood, faFaceSadTear)

import "../node_modules/bootstrap/dist/js/bootstrap"

const app = createApp(App);
app.use(router).use(VueGoogleMaps, {
    load: {
        key: 'AIzaSyB_XNrepzj7pUf2-dp9vSkpAfjXkAB9yHI',
        libraries: 'places'
    },
})

app.component('VueDatePicker', VueDatePicker);

app.use(store)

app.use(GoogleSignInPlugin, {
    clientId: "407206605140-bssenou8lkjkhcbagqf95nqem39prulh.apps.googleusercontent.com"
});

app.component('font-awesome-icon', FontAwesomeIcon);
app.mount("#app");