<template>

</template>

<script>
import router from '../router/index.js';
import {app} from '../main.js';

export default {
  name: "Logout",
  mounted:async function()
  {
    alert("Nastąpiło wylogowanie.");
    app.config.globalProperties.$is_allowed_to_log_in.value = false;
    await router.push({path: '/login'});
  },
}
</script>

<style scoped>

</style>