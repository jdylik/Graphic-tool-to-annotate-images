
<template>
  <div id="edit">
    <Button label="Edytuj nieadnotowane zdjęcie" @click="visibleLeft = true; displayImportedImages();" id="edit"/>
    <Button label="Edytuj adnotowane zdjęcie" @click="visibleRight = true; displayAnnotatedImages();" id="edit"/>
    <Sidebar v-model:visible="visibleLeft" position="left" class="sidebar_left" id="sidebar_left">
      <p>Wybierz zdjęcie do edycji</p>
<!--
          Tu miniaturki zdjęć:
      <img :src="img_i" v-if="img_i"/>
-->

    </Sidebar>
    <Sidebar v-model:visible="visibleRight" position="right" class="sidebar_right" id="sidebar_right">
      <a href="#">About</a>
      <a href="#">Services</a>
      <a href="#">Clients</a>
      <a href="#">Contact</a>
      <img :src="img_a" v-if="img_a"/>
    </Sidebar>
  </div>
</template>

<script>
import {app} from "@/main";
import axios from "axios";

export default {
  name: "Edit_images",
  data: function() {
    return {
      info: "",
      std:"",
      img_i:"",
      imn_a:"",
      visibleLeft:false,
      visibleRight:false,
    }
  },
  methods:
      {
        async displayImportedImages()//zaczęte
        {
          //const dict = {"login": app.config.globalProperties.$login.value, "password":app.config.globalProperties.$password.value};
          //axios.get("http://localhost:5000/get_imported_images")
          //axios.post("http://localhost:5000/insert_new_image", {params:JSON.stringify(dict)});
        },
        async displayAnnotatedImages()
        {

        },
      }
}
</script>

<style>

#edit{
  height: 100px;
}

#sidebar_left
{
  width: 20%;
  height: 100%;
  color:#111;
  background-color: #2c3e50;
  text-align: center;
}
.p-sidebar-header{
      margin-left: auto;
    margin-right: auto;
}
.p-sidebar-close{
  width: 100px;
  height: 20px;
  background-color: black;
  border: solid 2px white;
  color: white;
  padding: 20px;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  margin: 4px 4px;
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
#sidebar_right
{
  width: 20%;
  height: 100%;
  color:#111;
  background-color: #2c3e50;
  text-align: center;
}

.p-sidebar-close:before{
  content: "X";
}


p{
  color: white;
}
a{
  color: white;
}



</style>