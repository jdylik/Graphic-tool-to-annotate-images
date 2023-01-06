<template>
<div id="Login">
  <br/>
  <br/>
  <label for="login_input">Login</label>
  <InputText id="login_input" v-model="user_login"/>
  <label for="password_input">Hasło</label>
  <InputText id="password_input" v-model="user_password"/>
  <Button label="Zaloguj się" @click="try_to_log_in()" />
  <br/>
  <br/>
  <br/>
  <br/>
  <br/>
  <br/>
  <label for="new_login_input">Login</label>
  <InputText id="new_login_input" v-model="new_user_login"/>
  <label for="new_password_input">Hasło</label>
  <InputText id="new_password_input" v-model="new_user_password"/>
  <Button label="Zarejestruj się" @click="try_to_sign_up()" />
</div>
</template>

<script>
import {app} from '../main.js';
import router from '../router/index.js';
import axios from 'axios';

export default {
  name: "Login",
  data: function(){
        return {
          user_login:'',
          user_password:'',
          new_user_login:'',
          new_user_password:'',
          new_data:[],
        }
    },
  methods:
      {
        async try_to_log_in(e)
        {
          app.config.globalProperties.$is_allowed_to_log_in.value = false;
          const gResponse = await fetch("http://localhost:5000/get_logins_and_passwords");
          const gObject = await gResponse.json();
          for(let i = 0; i < gObject["logdatalist"].length; i++) {
            if (this.user_login === gObject["logdatalist"][i][0] && this.user_password === gObject["logdatalist"][i][1]) {
              app.config.globalProperties.$is_allowed_to_log_in.value = true;
              app.config.globalProperties.$login.value = this.user_login;
              app.config.globalProperties.$password.value = this.user_password;
              router.push({path: '/import'});
              break;
            }
            if (this.user_login === gObject["logdatalist"][i][0] && this.user_password !== gObject["logdatalist"][i][1]) {
              alert("Wygląda na to, że wpisałeś błędne hasło!");
              break;
            }
            if (i === gObject["logdatalist"].length - 1)
              alert("Wygląda na to, że użytkownik o podanym loginie nie istnieje. Utwórz nowe konto!");
          }
          this.user_login = '';
          this.user_password = '';
        },
        async try_to_sign_up(e)
        {
          if (this.new_user_login.includes("\"") || this.new_user_password.includes("\"") || this.new_user_login === '' || this.new_user_password === '' || this.new_user_login.length > 15 || this.new_user_password.length > 15)
          {
            alert("Pamiętaj, twój login i hasło nie mogą zawierać cudzysłowiu ani być puste, a także mieć więcej niż 15 znaków. Popraw dane i spróbuj ponownie!")
            return
          }
          const gResponse = await fetch("http://localhost:5000/get_logins_and_passwords");
          const gObject = await gResponse.json();
          if (gObject["logdatalist"].length === 0)
          {
            this.new_data.push(this.new_user_login, this.new_user_password);
            axios.post("http://localhost:5000/insert_new_data", {params: JSON.stringify(this.new_data)});
            alert("Teraz możesz zalogować się na podane przez siebie dane.");
          }
          else {
            for (let i = 0; i < gObject["logdatalist"].length; i++) {
              if (this.new_user_login === gObject["logdatalist"][i][0]) {
                alert("Użytkownik o podanym loginie już istnieje. Wybierz inny!");
                break;
              }
              if (this.new_user_login !== gObject["logdatalist"][i][0] && i === gObject["logdatalist"].length - 1) {
                this.new_data.push(this.new_user_login, this.new_user_password);
                axios.post("http://localhost:5000/insert_new_data", {params: JSON.stringify(this.new_data)});
                alert("Teraz możesz zalogować się na podane przez siebie dane.");
              }
            }
          }
          this.new_user_login = '';
          this.new_user_password = '';
        },
      },
}
</script>

<style scoped>

</style>