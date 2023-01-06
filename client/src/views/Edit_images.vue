
<template>
  <div id="edit">
    <Button label="Edytuj nieadnotowane zdjęcie" @click="visibleLeft = true;displayImportedImages();" />
    <Button label="Edytuj adnotowane zdjęcie" @click="visibleRight = true;displayAnnotatedImages();" />
    <Sidebar v-model:visible="visibleLeft" position="left" class="sidebar_left" id="sidebar_left">
      <a href="#">About</a>
      <img :src="img_i" v-if="img_i"/>
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

<style scoped>
#sidebar_left
{
  color:#111;
  border: 2px solid powderblue;
}
</style>