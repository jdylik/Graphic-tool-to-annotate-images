<template>
<div id="Login">
  <label for="login_input">Login</label>
  <InputText id="login_input" v-model="user_login"/>
  <label for="password_input">Hasło</label>
  <InputText id="password_input" v-model="user_password"/>
  <Button label="Zaloguj się" @click="try_to_log_in()" />
</div>
</template>

<script>
import router from '../router/index.js';


export default {
  name: "Login",
  data: function(){
        return {
          user_login:'',
          user_password:'',
          is_allowed_to_sign_up:false,
        }
    },
  methods:
      {
        async try_to_log_in(e)
        {
          this.is_allowed_to_log_in = false;
          const gResponse = await fetch("http://localhost:5000/get_logins_and_passwords");
          const gObject = await gResponse.json();
          for(let i = 0; i < gObject["logdatalist"].length; i++)
          {
            if (this.user_login === gObject["logdatalist"][i][0] && this.user_password === gObject["logdatalist"][i][1])
            {
              this.is_allowed_to_log_in = true;
              router.push('/import');
              break;
            }
            if (this.user_login === gObject["logdatalist"][i][0] && this.user_password !== gObject["logdatalist"][i][1])
            {
              alert("Wygląda na to, że wpisałeś błędne hasło!");
              break;
            }
            if (this.user_login !== gObject["logdatalist"][i][0] && this.user_password !== gObject["logdatalist"][i][1] && i === gObject["logdatalist"].length - 1)
            {
              alert("Wygląda na to, że użytkownik o podanym loginie nie istnieje. Utwórz nowe konto!");
            }
          }
        }
      },
}
</script>

<style scoped>

</style>