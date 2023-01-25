<template>
  <div class="wrap">
    <Button label="Eksportuj wszystkie" @click="loadAnnotatedImages(); exportAll()" class="tools"/>
    <Button v-if="!img_visible" label="Wybierz zdjęcia do eksportu" @click="loadAnnotatedImages(); img_visible=true;" class="tools"/>
    <Button v-if="img_visible" label="Eksportuj wybrane" @click=" exportNotAll()" class="tools" id="exp"/>
  </div>
  <div class="imggrid">
    <ul>
      <li v-if="img_visible" v-for="(image, imageIndex) in displayed_annotated_images" >
        <img v-bind:id="imageIndex" :src="image" v-if="image" width="200" height="150" class="img-grid"/>
      </li>
    </ul>
  </div>
</template>

<script>
import {app} from "@/main";
import axios from "axios";

export default {
  name: "Export",
  data: function ()
  {
    return{
      img_visible:false,
      annotated:[],
      displayed_annotated_images:[],
      to_download:[],
    }
  },
  methods: {
    async loadAnnotatedImages() {
          const dict = {
            "login": app.config.globalProperties.$login.value,
            "password": app.config.globalProperties.$password.value,
          };
          const annotated = [];
          const annotated_ind = [];                                                                                                                                                                                                                                                                                                                                                                                                                                                                             0
          await axios.post("http://localhost:5000/get_annotated_images_no_rects",
              {params: JSON.stringify(dict)}).then(function (response) {
            let data = response.data["images"];
            for(let i = 0; i < data.length; i++)
            {
              annotated.push("data:image/jpeg;base64," + data[i]);
              annotated_ind.push(response.data["indexes"][i][0]);
            }
            return annotated;
          });
          this.annotated = annotated;
          this.annotated_ind=annotated_ind;
          this.displayed_annotated_images=annotated;
        },
    async exportNotAll(){
      // tu jeszcze nic nie ma
    },
    async exportAll() {
      // tu beda zdjecia resizowane
      const to_download=[];
      for(let i=0;i<this.annotated.length;i++)
      {
        var resizebase64 = require('resize-base64');
        var  img = resizebase64(this.annotated[i], 200, 150);
        to_download.push(img);
      }
      this.to_download=to_download;

      // testowy download jednego zdj
      var a = document.createElement("a"); //Create <a>
      a.href = this.to_download[0]; //Image Base64 Goes here
      a.download = "Image.png"; //File name Here
      a.click(); //Downloaded file
    },
}}
</script>

<style scoped>

.imggrid{
  margin-top:10px;
  width: 100vw;
}
.imggrid ul li{
  display: inline;
  margin: 10px 10px 10px 10px;
}
.img-grid{
  margin-top:15px;
  box-shadow: 2px 2px 4px rgba(70, 70, 70, 0.6);
}
.img-grid:hover{
  box-shadow: 3px 3px 6px rgba(70, 70, 70, 0.8);
  cursor: pointer;
}

</style>

