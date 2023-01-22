<template>
<div id="Login">
  <button id="L" onclick="getElementById('logowanie').style.display='block';getElementById('rejestracja').style.display='none';
  getElementById('L').style.color='black'; getElementById('R').style.color='#778da9'" >Logowanie</button>
  <button id="R" onclick="getElementById('rejestracja').style.display='block';getElementById('logowanie').style.display='none';
  getElementById('R').style.color='black';getElementById('L').style.color='#778da9'">Rejestracja</button>
  <div id="logowanie">
    <label for="login_input">Login:</label>
    <InputText id="login_input" v-model="user_login" @keyup.enter.native="try_to_log_in()"/><br><br>
    <label for="password_input">Hasło:</label>
    <input type="password" id="password_input" v-model="user_password" @keyup.enter.native="try_to_log_in()"/><br><br>
    <Button label="Zaloguj się" @click="try_to_log_in()" id="submit"/>
  </div>

  <br/>
  <div id="rejestracja">
    <label for="new_login_input">Login:</label>
    <InputText id="new_login_input" v-model="new_user_login" @keyup.enter.native="try_to_sign_up()"/><br><br>
    <label for="new_password_input" >Hasło:</label>
    <input type="password" id="new_password_input" v-model="new_user_password" @keyup.enter.native="try_to_sign_up()"/><br><br>
    <Button label="Zarejestruj się" @click="try_to_sign_up()" id="submit"  />
  </div>

</div>
</template>

<script>

import {app} from '@/main';
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
        async try_to_log_in()
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
          if (gObject["logdatalist"].length === 0)
          {
            alert("Wygląda na to, że użytkownik o podanym loginie nie istnieje. Utwórz nowe konto!");
          }
          this.user_login = '';
          this.user_password = '';
        },
        async try_to_sign_up()
        {
          if (this.new_user_login === '' || this.new_user_password === '')
          {
            alert("Login i hasło nie mogą być puste!")
            return
          }
          else if (this.new_user_login.length > 15 || this.new_user_password.length > 15)
          {
            alert("Login i hasło nie mogą mieć więcej niż 15 znaków!")
          }
          else if (this.new_user_login.includes("\"") || this.new_user_password.includes("\"") || this.new_user_login.includes("\\") ||this.new_user_password.includes("\\"))
          {
            alert("Wykorzystano niedozwolony znak. \n Nie używaj: \\, \".")
            return
          }
          else
          {const gResponse = await fetch("http://localhost:5000/get_logins_and_passwords");
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
                alert("Użytkownik o podanym loginie już istnieje. Zaloguj się!");
                break;
              }
              if (this.new_user_login !== gObject["logdatalist"][i][0] && i === gObject["logdatalist"].length - 1) {
                this.new_data.push(this.new_user_login, this.new_user_password);
                axios.post("http://localhost:5000/insert_new_data", {params: JSON.stringify(this.new_data)});
                alert("Teraz możesz zalogować się na podane przez siebie dane.");
              }
              document.getElementById('rejestracja').style.display='none';
              document.getElementById('logowanie').style.display='block';
              document.getElementById('L').style.color='#6ce8ac';
              document.getElementById('R').style.color='#FFFF';
            }
          }
          this.new_user_login = '';
          this.new_user_password = '';}
        },
      },
}
</script>

<style>
#rejestracja,#logowanie{
  margin-left: auto;
  margin-right: auto;
  padding:20px;

}

#logowanie{
  display:none;
}
#rejestracja{
  display:none;
}
#L, #R {
  height: 50px;
  width: 150px;
  padding: 5px;
  font-size: 15px;
  text-align: center;
  cursor: pointer;
  outline: none;
  color: black;
  background-color: #e0e1dd;
  border-radius: 15px;
  margin-left: 5px;
  margin-right: 5px;
}

#L:hover {background-color: #415a77}

#L:active {
  background-color: #2c3e50;
  transform: translateY(4px);
}

#R:hover {background-color: #415a77}

#R:active {
  background-color: #2c3e50;
  transform: translateY(4px);
}

#Login{
  margin-left: auto;
  margin-right: auto;
  margin-bottom: -200px;
  padding: 20px;
  min-height:100vh;
}
#submit{
  height: 50px;
  width: 150px;
  padding: 5px;
  font-size: 15px;
  text-align: center;
  cursor: pointer;
  outline: none;
  color: black;
  background-color: #e0e1dd;
  border-radius: 15px;
  margin-left: 5px;
  margin-right: 5px;
}

#submit:hover {background-color: #415a77}

#submit:active {
  background-color: #2c3e50;
  transform: translateY(4px);
}

label{
  margin-right: 10px;
  color: #0d1b2a;
}
</style>