<template>
  <div class="wrap">
    <div v-if="!img_visible">
      <p>{{"Podaj nazwę projektu:"}}</p>
        <input type="text" id="project_name" defaultValue="Projekt"/>
    </div>
    <Button v-if="!img_visible" label="Dalej" @click="loadAnnotatedImages(); img_visible=true;" class="tools"/>
    <Button v-if="img_visible" label="Eksportuj wszystkie" @click="loadAnnotatedImages(); exportAll();" class="tools"/>
    <Button v-if="img_visible" label="Eksportuj wybrane" @click=" loadAnnotatedImages();exportNotAll()" class="tools" id="exp"/>
  </div>
  <div class="imggrid" >
    <ul class="imggridul">
      <li v-if="img_visible" v-for="(image, imageIndex) in displayed_annotated_images" class="imggridli">
        <img v-bind:id="imageIndex" :src="image" v-if="image" width="200" height="150" class="img-grid" @click="selected(imageIndex)"/>
      </li>
    </ul>
  </div>
</template>

<script>

import {app} from "@/main";
import axios from "axios";
import JSZip from "jszip";
import { saveAs } from 'file-saver';
import resizebase64 from "resize-base64";

function b64toBlob(dataURI) {

    var byteString = atob(dataURI.split(',')[1]);
    var ab = new ArrayBuffer(byteString.length);
    var ia = new Uint8Array(ab);

    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: 'image/jpeg' });
}

const saveZip = (filename, urls) => {
    let zip = new JSZip();
    let folder = zip.folder(filename);
    for(let i=0;i<urls.length;i++)
    {
      folder.file(`image${i}.jpg`, urls[i]);
    }
    folder.generateAsync({ type: "blob" }).then(content => saveAs(content, filename));
};



export default {
  name: "Export",

  data: function ()
  {
    return{
      img_visible:false,
      annotated:[],
      displayed_annotated_images:[],
      to_download:[],
      p_name:"project",
      indexOfCurrentImage:null,
      current_img:null,
      chosen_ind:[],
    }
  },
  methods: {
    async loadAnnotatedImages() {
      // this.p_name=document.getElementById('project_name').value;
      const dict = {
            "login": app.config.globalProperties.$login.value,
            "password": app.config.globalProperties.$password.value,
          };
          const annotated = [];
          const annotated_ind = [];                                                                                                                                                                                                                                                                                                                                                                                                                                                                             0
          await axios.post("http://localhost:5000/get_annotated_images_no_rects", {params: JSON.stringify(dict)}).then(function (response) {
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
    async exportAll(){
      await this.loadAnnotatedImages();
      if(this.annotated)
      {
        console.log(this.annotated);
        const to_download=[];
        for(let i=0;i<this.annotated.length;i++)
        {
          var resizebase64 = require('resize-base64');
          var  img = resizebase64(this.annotated[i], 666, 500);
          var blob = b64toBlob(img)
          to_download.push(blob);
        }
        this.to_download=to_download;
        saveZip(this.p_name,this.to_download);
      }
    },

    async exportNotAll() {
      await this.loadAnnotatedImages();
      // to nie jest przechwytywane jako faktyczna nazwa - nie dziala
      // this.p_name=document.getElementById('project_name').value;
      if(this.annotated)
      {
        console.log(this.chosen_ind);
        const to_download=[];
        for(let i=0;i<this.chosen_ind.length;i++)
        {
          var resizebase64 = require('resize-base64');
          var  img = resizebase64(this.annotated[this.chosen_ind[i]], 666, 500);
          var blob = b64toBlob(img);
          to_download.push(blob);
        }
        this.to_download=to_download;
        saveZip(this.p_name,this.to_download);
      }
    },
     async selected(index) {
            this.current_img = document.getElementById(index);
            console.log(this.annotated.length)
            console.log(this.chosen_ind)
            if (this.chosen_ind.includes(index)) {
              console.log(index)
              this.current_img.style.border = "5px solid white";
              this.chosen_ind.splice(this.chosen_ind.indexOf(index), 1);
            }
            else {
              this.indexOfCurrentImage = index;
              console.log(index)
              this.current_img.style.border = "5px solid yellow";
              this.chosen_ind.push(index)
            }
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

#project_name{
  margin-bottom: 30px;
}
</style>

