import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';
import 'quasar/dist/quasar.css';
import { Quasar } from 'quasar';
import quasarUserOptions from './quasar-user-options';
import '@/assets/css/main.scss';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faMortarPestle, faPrescriptionBottle, faWeightScale,
    faFlask, faPills, faMagnifyingGlass, faMagnifyingGlassPlus,
    faSkullCrossbones, faBottleDroplet, faGlassWaterDroplet, faHandDots,
    faHandHoldingDroplet, faBookMedical, faSnowflake, faTriangleExclamation, faClone, faChild } from '@fortawesome/free-solid-svg-icons';
import './registerServiceWorker'
import 'chart.js';
import 'vue-chartjs';


library.add(faMortarPestle, faPrescriptionBottle, faWeightScale, faFlask, faPills,
    faMagnifyingGlass, faMagnifyingGlassPlus, faSkullCrossbones, faBottleDroplet,
    faGlassWaterDroplet, faHandDots, faHandHoldingDroplet, faBookMedical, faSnowflake,
    faTriangleExclamation, faClone, faChild);

const app = createApp(App)
  .use(Quasar,
      quasarUserOptions)
  .use(router)
  .use(store)


app.component('font-awesome-icon', FontAwesomeIcon);

app.config.errorHandler = (err, vm, info) => {
    console.log('Captured in app.config.errorHandler: ', err, vm, info);
};

app.mount('#app');


// obtenir le CSRF token à partir des cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // est-ce que ce cookie stocke le CSRF token ?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.headers.post['X-CSRFToken'] = csrftoken;



