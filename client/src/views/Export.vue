<template>
  <div class="wrap">
    <div>
      <p>{{"Podaj nazwę projektu:"}}</p>
        <input type="text" id="project_name" v-on:keyup.enter="loadAnnotatedImages(); img_visible=true;"/>
    </div>
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
  <div class="lista">
        <ul class="typy">
          <span v-if="string_visible">Podsumowanie liczności klas obiektów na wybranych zdjęciach:</span>
          <li v-for="(value, index) in labels_to_display"  id="lista1">
            <span>{{ value }} - {{nr_of_cases[index]}} wystąpień</span>
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
      produced_coco:null,
      files_names:null,
      labels_to_display:[],
      nr_of_cases:[],
      string_visible:'',
      annotated_ind_list:[],
    }
  },
  methods: {

    async saveZip(filename, urls) {
      await this.files_names;
      let zip = new JSZip();
      let folder = zip.folder(filename);
      for(let i=0;i<urls.length - 1;i++)
      {
        folder.file(this.files_names[i]+".jpg", urls[i]);
      }
      let json = new Blob([urls[urls.length-1]], {
      type: 'application/json'
      });
      folder.file(`${filename}-coco.json`, json);
      folder.generateAsync({ type: "blob" }).then(content => saveAs(content, filename));
    },
    async loadAnnotatedImages() {
      // this.p_name=document.getElementById('project_name').value;
      const dict = {
            "login": app.config.globalProperties.$login.value,
            "password": app.config.globalProperties.$password.value,
          };
          const annotated = [];
          const annotated_ind = [];
          const annotated_ind_list = [];
          await axios.post("http://localhost:5000/get_annotated_images_no_rects", {params: JSON.stringify(dict)}).then(function (response) {
            let data = response.data["images"];
            for(let i = 0; i < data.length; i++)
            {
              annotated.push("data:image/jpeg;base64," + data[i]);
              annotated_ind.push(response.data["indexes"][i][0]);
              annotated_ind_list.push(i);
            }
            return annotated;
          });
          this.annotated = annotated;
          this.annotated_ind=annotated_ind;
          this.displayed_annotated_images=annotated;
          this.annotated_ind_list = annotated_ind_list;
          const ext_dict = {
            "login": app.config.globalProperties.$login.value,
            "password": app.config.globalProperties.$password.value,
            "indexes": this.annotated_ind,
          }
          let response = await axios.post("http://localhost:5000/get_names_of_files", {params: JSON.stringify(ext_dict)})
          this.files_names = response.data["names"]
        },
    async exportAll(){
      await this.loadAnnotatedImages();
      this.chosen_ind = this.annotated_ind_list;
      await this.displayStats(this.chosen_ind);
      if(this.annotated)
      {
        const to_download=[];
        for(let i=0;i<this.annotated.length;i++)
        {
          let resizebase64 = require('resize-base64');
          let img = resizebase64(this.annotated[i], 666, 500);
          let blob = b64toBlob(img);
          to_download.push(blob);
        }
        this.to_download=to_download;
        await this.getCoco(this.to_download);
        this.to_download.push(this.produced_coco);
        await this.saveZip(this.p_name,this.to_download);
      }
    },

    async exportNotAll() {
      await this.loadAnnotatedImages();
      if (this.chosen_ind.length !== 0) {
        if (this.annotated) {
          const to_download = [];
          for (let i = 0; i < this.chosen_ind.length; i++) {
            let resizebase64 = require('resize-base64');
            let img = resizebase64(this.annotated[this.chosen_ind[i]], 666, 500);
            let blob = b64toBlob(img);
            to_download.push(blob);
          }
          this.to_download = to_download;
          await this.getCoco(this.to_download);
          this.to_download.push(this.produced_coco);
          await this.saveZip(this.p_name, this.to_download);
        }
      }
    },
     async selected(index)
     {
            this.labels_to_display = [];
            this.nr_of_cases = [];
            this.current_img = document.getElementById(index);
            if (this.chosen_ind.includes(index)) {
              this.current_img.style.border = "5px solid white";
              this.chosen_ind.splice(this.chosen_ind.indexOf(index), 1);
            }
            else {
              this.indexOfCurrentImage = index;
              this.current_img.style.border = "5px solid yellow";
              this.chosen_ind.push(index)
            }
            this.string_visible = true;
            await this.displayStats(this.chosen_ind);
        },
    async displayStats(table)
    {
      const ext_dict = {
            "login": app.config.globalProperties.$login.value,
            "password": app.config.globalProperties.$password.value,
            "indexes": table,
      }
      let elements_response = await axios.post("http://localhost:5000/count_classes", {params: JSON.stringify(ext_dict)});
      let data = elements_response.data;
      this.labels_to_display = Object.keys(data);
      this.nr_of_cases = Object.values(data);
      this.string_visible = true;
    },
    async getCoco(table)
    {
      this.p_name = document.getElementById("project_name").value;
      let ids = [];
      for(let i = 1; i < table.length + 1; i++)
        ids.push(i);
      let info = {"year": new Date().getFullYear(),"description": this.p_name,"date_created": new Date().toJSON().slice(0, 10)};
      const dict = {
            "login": app.config.globalProperties.$login.value,
            "password": app.config.globalProperties.$password.value,
          };
      let cat_response = await axios.post("http://localhost:5000/get_categories_coco", {params: JSON.stringify(dict)});
      let cat_data = cat_response.data["names"];
      let cats = [];
      for (let i = 0; i < cat_data.length; i++)
      {
        let cat={"id":cat_data[i][0], "name":cat_data[i][1]};
        cats.push(cat);
      }
      const ext_dict = {
            "login": app.config.globalProperties.$login.value,
            "password": app.config.globalProperties.$password.value,
            "indexes": this.chosen_ind,
      }
      let id_an = 0;
      let img_response = await axios.post("http://localhost:5000/get_image_and_annotation_info_coco", {params: JSON.stringify(ext_dict)});
      let img_ids = img_response.data["id_o"];
      let img_data = img_response.data["names"];
      let camera = img_response.data["camera"]
      let loc = img_response.data["location"]
      let ids_for_adns = img_response.data["ids_for_adns"]
      let adnid = img_response.data["adnid"]
      let id_kat = img_response.data["id_kat"]
      let x_start = img_response.data["x_start"]
      let y_start = img_response.data["y_start"]
      let szer = img_response.data["szer"]
      let wys = img_response.data["wys"]
      let imgs = [];
      for (let i = 0; i < img_data.length; i++)
      {
        let img= {"id": ids[i],"program_id": img_ids[i],"width": 666,"height": 550,"file_name": img_data[i]+".jpg","camera": camera[i],"location": loc[i],"metadata": "brak"};
        imgs.push(img);
      }
      let anns = []
      for (let i = 0; i < wys.length; i++)
      {
        let ann={"id":ids_for_adns[i],"program_id":adnid[i],"image_id":img_ids[i],"category_id":id_kat[i],"segmentation":[x_start[i],y_start[i],(x_start[i]+szer[i]),y_start[i],(x_start[i]+szer[i]),(y_start[i]+wys[i]),x_start[i],(y_start[i]+wys[i])],"area":(szer[i]*wys[i]),"bbox": [x_start[i],y_start[i],szer[i],wys[i]],"iscrowd": 0};
        anns.push(ann);
      }
      this.produced_coco = JSON.stringify({"info": info,"categories": cats, "images": imgs, "annotations": anns});
    },
    mounted()
    {
      this.string_visible = false;
    }
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

