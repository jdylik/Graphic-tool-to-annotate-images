import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config';
import Sidebar from 'primevue/sidebar';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';

const app = createApp(App);
app.config.globalProperties.is_allowed_to_log_in = true;
app.use(router);
app.use(PrimeVue);
app.component('Sidebar', Sidebar);
app.component('Button', Button);
app.component('InputText', InputText);
app.mount('#app');