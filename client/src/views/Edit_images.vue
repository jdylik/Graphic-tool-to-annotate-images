
<template>
  <div id="pageWrap">

    <canvas id="myCanvas" width="666" height="500" style="border:5px solid black;"/>

    <div id="row1">
      <Button label="Rysuj" @click="drawRectangle();" id="draw" class="tools"/>
      <Button label="Usuń" @click="" class="tools"/>
      <Button label="Zapisz" @click="" class="tools"/>
    </div>

    <div id="row2">
      <Button label="Edytuj nieadnotowane zdjęcie" @click="visibleLeft = true; loadImportedImages();" id="edit" class="tools"/>
      <Button label="Edytuj adnotowane zdjęcie" @click="visibleRight = true; loadAnnotatedImages();" id="edit" class="tools"/>
    </div>

    <Sidebar v-model:visible="visibleLeft" position="left" class="sidebar_left" id="sidebar_left">
      <p>Wybierz zdjęcie do edycji</p>
      <ul>
      <li v-for="(image, index) in displayed_imported_images" id="import_list">
        <img v-bind:id="index" :src="image" v-if="image" width="200" height="150" @click="selected(index)"/>
      </li>
      </ul>
      <Button label="Załaduj więcej" @click="loadMoreImported()" id="moreL"/>
    </Sidebar>

    <Sidebar v-model:visible="visibleRight" position="right" class="sidebar_right" id="sidebar_right">
      <Button label="Załaduj więcej" @click="visibleRight = true; loadAnnotatedImages();" id="moreR"/>
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
      visibleLeft:false,
      visibleRight:false,
      imported:[],
      annotated:[],
      current_img: null,
      displayed_imported_images:[],
      displayed_annotated_images:[],
      canvas:null,
      context:null,
      rec_beg_x:[],
      rec_beg_y:[],
      rec_w:[],
      rec_h:[],
      rec_counter:0,
      ifButtonDrawClicked:false,
      indexOfCurrentImage:0,
    }
  },
  methods:
      {
        async loadImportedImages() {
          const dict = {
            "login": app.config.globalProperties.$login.value,
            "password": app.config.globalProperties.$password.value
          };
          const imported = [];
          await axios.post("http://localhost:5000/get_imported_images", {params: JSON.stringify(dict)}).then(function (response) {
            for (let i = 0; i < response.data["images"].length; i++) {
              imported.push("data:image/jpeg;base64," + response.data["images"][i]);
            }
            return imported;
          });
          this.imported = imported;
          if (this.imported.length < 4)
            this.displayed_imported_images = imported.slice(0, this.imported.length);
          else
            this.displayed_imported_images = imported.slice(0, 4);
        },
        async loadAnnotatedImages() {
          const dict = {
            "login": app.config.globalProperties.$login.value,
            "password": app.config.globalProperties.$password.value
          };
          const annotated = [];
          await axios.post("http://localhost:5000/get_annotated_images", {params: JSON.stringify(dict)}).then(function (response) {
            for (let i = 0; i < response.data["images"].length; i++) {
              annotated.push("data:image/jpeg;base64," + response.data["images"][i]);
            }
            return annotated;
          });
          this.annotated = annotated;
          if (this.annotated.length < 4)
            this.displayed_annotated_images = annotated.slice(0, this.annotated.length);
          else
            this.displayed_annotated_images = annotated.slice(0, 4);
        },
        async loadMoreImported(e) {
          const length = this.displayed_imported_images.length;
          if (length < 4) {
          } else if (this.imported.length < length + 4)
            this.displayed_imported_images.push.apply(this.displayed_imported_images, this.imported.slice(length, this.imported.length));
          else
            this.displayed_imported_images.push.apply(this.displayed_imported_images, this.imported.slice(length, length + 4));
        },
        async selected(index) {
          this.indexOfCurrentImage = index;
          this.rec_counter = 0;
          this.rec_beg_x = [];
          this.rec_beg_y = [];
          this.rec_w = [];
          this.rec_h = [];
          this.ifButtonDrawClicked = false;
          this.current_img = document.getElementById(index);
          this.context.globalAlpha = 1;
          this.context.clearRect(0, 0, this.current_img.width * 3.33, this.current_img.height * 3.33)
          this.context.drawImage(this.current_img, 0, 0, this.current_img.width * 3.33, this.current_img.height * 3.33);
        },
        drawAllRects()
        {
          this.context.beginPath();
          this.context.strokeStyle = "rgb(0, 0, 255)";
          this.context.fillStyle = "rgba(255,0,0, 0.2)";
          this.context.drawImage(this.current_img, 0, 0, this.current_img.width * 3.33, this.current_img.height * 3.33);
          for(let i = 0; i < this.rec_counter; i++)
          {
            this.context.strokeRect(this.rec_beg_x[i], this.rec_beg_y[i], this.rec_w[i], this.rec_h[i]);
            this.context.fillRect(this.rec_beg_x[i], this.rec_beg_y[i], this.rec_w[i], this.rec_h[i]);
          }

        },
        drawRectangle() {
          if (this.current_img != null ) {
            this.ifButtonDrawClicked = true;
            let beginning_x = null;
            let beginning_y = null;
            let previous_x = null;
            let previous_y = null;
            let current_x = null;
            let current_y = null;
            this.context.lineWidth = 1;
            let draw = false;
            let is_rect_finished = false;
            window.addEventListener("mousedown", (e) => {
              if (e.target.localName === 'canvas') {
                is_rect_finished = false;
                draw = true;
              }
            });
            window.addEventListener("mouseup", (e) => {
              if (e.target.localName === 'canvas') {
                is_rect_finished = true;
                this.rec_beg_x[this.rec_counter] = beginning_x;
                this.rec_beg_y[this.rec_counter] = beginning_y;
                this.rec_w[this.rec_counter] = previous_x - beginning_x;
                this.rec_h[this.rec_counter] = previous_y - beginning_y;
                this.rec_counter += 1;
              }
                this.drawAllRects();
                this.context.stroke();
                this.context.closePath();
                //realnie po prawej  - dynamiczny podgląd
              //wydaje się to jednak niepotrzebnym featurem - przycisk do zapisu po prostu wrzuci to zdjęcie na koniec zaadnotowanych
                //this.displayed_imported_images[this.indexOfCurrentImage] = document.getElementById('myCanvas').toDataURL('image/jpeg');
                draw = false;
            });
            window.addEventListener("mousemove", (e) => {
              if (e.target.localName !== 'canvas' && !is_rect_finished)   {
                draw = false;
                this.drawAllRects();
                this.context.stroke();
                this.context.closePath();
                return
              }
              if (previous_x == null || previous_y == null || !draw) {
                beginning_x = e.offsetX;
                beginning_y = e.offsetY;
                previous_x = e.offsetX;
                previous_y = e.offsetY;
                return
              }
              let current_x = e.offsetX;
              let current_y = e.offsetY;
              //this.context.globalAlpha = 0.4;
              //this.context.clearRect(beginning_x, beginning_y, previous_x - beginning_x, previous_y - beginning_y);
              this.drawAllRects();
              this.context.strokeRect(beginning_x, beginning_y, current_x - beginning_x, current_y - beginning_y);
              this.context.fillRect(beginning_x, beginning_y, current_x - beginning_x, current_y - beginning_y);
              //this.context.beginPath();
              this.context.stroke();
              this.context.closePath();

              previous_x = current_x;
              previous_y = current_y;
            });
          }
        },
      },
      mounted()
      {
        this.canvas = document.getElementById("myCanvas");
        this.context = this.canvas.getContext("2d");
      }
}
</script>

<style>

canvas{
  margin-left: auto;
  margin-right: auto;
}
.tools {
  height: 60px;
  width: 220px;
  padding: 5px;
  font-size: 15px;
  text-align: center;
  cursor: pointer;
  outline: none;
  color: #fff;
  background-color: steelblue;
  border-radius: 15px;
  margin-left: 5px;
  margin-right: 5px;
}

.tools:hover {background-color: #2c3e50}

.tools:active {
  background-color: #2c3e50;
  transform: translateY(4px);
}

ul
{
  list-style-tuple:none;
}

#row1{
  padding: 10px;
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

#moreL {
  height: 60px;
  width: 220px;
  position: fixed;
  bottom: 5px;
  left: 3.5%;
  padding: 5px;
  font-size: 15px;
  text-align: center;
  cursor: pointer;
  outline: none;
  color: #fff;
  background-color: steelblue;
  border-radius: 15px;
  margin-left: 5px;
  margin-right: 5px;
}

#moreL:hover {background-color: #2c3e50}

#moreL:active {
  background-color: #2c3e50;
  transform: translateY(4px);
}
#moreR {
  height: 60px;
  width: 220px;
  position: fixed;
  bottom: 5px;
  right: 3.5%;
  padding: 5px;
  font-size: 15px;
  text-align: center;
  cursor: pointer;
  outline: none;
  color: #fff;
  background-color: steelblue;
  border-radius: 15px;
  margin-left: 5px;
  margin-right: 5px;
}

#moreR:hover {background-color: #2c3e50}

#moreR:active {
  background-color: #2c3e50;
  transform: translateY(4px);
}

a{
  padding: 15px;
}

</style>