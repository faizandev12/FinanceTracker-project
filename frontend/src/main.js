import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from "axios";
import vuetify from './plugins/vuetify'
import '@mdi/font/css/materialdesignicons.css'
//import { library } from '@fortawesome/fontawesome-svg-core'
//import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
//import { faMoneyBillTrendUp } from '@fortawesome/pro-solid-svg-icons'
//library.add(faMoneyBillTrendUp)
//app.component('font-awesome-icon', FontAwesomeIcon)


//createApp(App).use(router).mount('#app')
const app = createApp(App)
app.use(router)
app.use(vuetify)
app.mount('#app')
  

axios.interceptors.response.use(
    (response) => response, // If the response is successful, return it
    (error) => {
      if (error.response && error.response.status === 401) {
        // If the backend returns 401 Unauthorized
        localStorage.removeItem("token"); // Clear token from localStorage
        delete axios.defaults.headers.common["Authorization"]; // Remove the header
        router.push("/login"); // Redirect to login page
      }
      return Promise.reject(error);
    }
  );