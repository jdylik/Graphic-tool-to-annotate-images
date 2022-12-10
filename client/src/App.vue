<!--<script setup>-->
<!--import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'-->
<!--</script>-->

<template>
<div id="app">
    <button v-on:click="">Import folder</button>
</div>
</template>

<script>
export default {
    data: function(){
        return {
            greeting: 'Hello, Vue!',
            flaskGreeting: ''
        }
    },
    created: async function(){
        const gResponse = await fetch("http://localhost:5000/greeting");
        const gObject = await gResponse.json();
        this.flaskGreeting = gObject.greeting;
    }
}
</script>