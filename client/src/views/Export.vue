<template>
  <div class="wrap">
    <Button label="Eksportuj wszystkie" @click="loadAnnotatedImages(); exportAll()" class="tools"/>
    <Button label="Wybierz zdjęcia do eksportu" @click="loadAnnotatedImages(); exportNotAll(); img_visible=true;" class="tools"/>
  </div>

  <div class="imggrid">
    <ul>
      <li v-if="img_visible" v-for="(image, imageIndex) in displayed_annotated_images" >
        <img v-bind:id="imageIndex" :src="image" v-if="image" width="200" height="150"/>
      </li>
    </ul>
  </div>
</template>

<script>
import {app} from "@/main";
import axios from "axios";
import router from "@/router";
export default {
  name: "Export",
  data: function ()
  {
    return{
      img_visible:false,
      annotated:[],
      displayed_annotated_images:[],
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
          // if (this.annotated.length < 4)
          //   this.displayed_annotated_images = annotated.slice(0, this.annotated.length);
          // else
          //   this.displayed_annotated_images = annotated.slice(0, 4);
        },
    async exportNotAll(){},
    async exportAll() {
          var a = document.createElement("a"); //Create <a>
          console.log(this.annotated[0])
          a.href = this.annotated[0]; //Image Base64 Goes here
          a.download = "zdjecie.jpg"; //File name Here
          a.click(); //Downloaded file
        },
  }
}
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
</style>

