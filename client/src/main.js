// import {createApp, VueElement} from 'vue'
// import App from './App.vue'
//
// import './assets/main.css'
//
// createApp(App).mount('#app')
// import {createApp} from "vue";

const { createApp } = Vue
const PhotoApp = {
    data(){
        return {
            message: "Hello World"
        }
    }
}
createApp(PhotoApp).mount('#app')

