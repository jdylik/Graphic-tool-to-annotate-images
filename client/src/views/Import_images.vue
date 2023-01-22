<template>
<div id="import">
    <p>{{"Załaduj folder ze zdjęciami"}}</p>
    <input type="file" id="input_folder" @change="onFolder" webkitdirectory directory multiple/>
    <p>{{"Załaduj zdjęcie"}}</p>
    <input type="file" id="input_file" @change="onFile"/>
</div>
</template>

<script>
import {app} from '../main.js';
import Edit_images from "@/views/Edit_images.vue";
import axios from "axios";
export default {
  name: "Import_images",
    data: function(){
        return {
          imgSrc:'',
        }
    },
  mounted:async function()
  {
  },
  methods:
      {
        onFile(e)
        {
          const reader = new FileReader();
          reader.readAsDataURL(e.target.files[0]);
          reader.onload = () =>
          {
            this.imgSrc = reader.result;
            const image = this.imgSrc.split(",")[1];
            const dict = {"img": image, "login": app.config.globalProperties.$login.value, "password":app.config.globalProperties.$password.value};
            axios.post("http://localhost:5000/insert_new_image", {params:JSON.stringify(dict)});
          };
        },
        async onFolder(e)
        {
          for (let i = 0; i < e.target.files.length;i++)
          {
             const reader = new FileReader();
              reader.readAsDataURL(e.target.files[i]);
              reader.onload = () =>
              {
                this.imgSrc = reader.result;
                const image = this.imgSrc.split(",")[1];
                const dict = {"img": image, "login": app.config.globalProperties.$login.value, "password":app.config.globalProperties.$password.value};
                axios.post("http://localhost:5000/insert_new_image", {params:JSON.stringify(dict)});
          };
          }
        },
      },

}
</script>
<style>
p{
  padding: 15px;
  font-size: large;
  color: #0d1b2a;
  margin-top: 30px;
}
input{
  font-size: medium;
}
#import{
  min-height: 100vh;
  margin-bottom: -200px;
}
</style>