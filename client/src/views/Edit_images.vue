
<template>
  <div id="pageWrap">
    <div id="kanwas">
      <canvas id="myCanvas" width="666" height="500" style="border:5px solid black;"/>
      <!--ta lista oraz pole input poniżej ma się znaleźć obok canvasa-->
      <div id="lista">
        <p>{{"Określ typ adnotowanego obiektu"}}</p>
        <input type="text" id="object_type" v-on:keyup.enter="onEnter"/>
        <ul id="typy">
          <li v-for="(value, index) in unique_labels"  id="kolko">
          <!--<span class="clr" style="color:red"></span>-->
            <span>{{ value }}</span>
          </li>
        </ul>
      </div>

    </div>
    <div id="row1">
      <Button label="Rysuj" @click="drawRectangle();" id="draw" class="tools"/>
      <Button label="Usuń" @click="deleteRectangle();" class="tools"/>
      <Button label="Zapisz" @click="saveAnnotations()" class="tools"/>
    </div>

    <div id="row2">
      <Button label="Edytuj nieadnotowane zdjęcie" @click="visibleLeft = true; visibleRight = false; loadImportedImages();" id="edit" class="tools"/>
      <Button label="Edytuj adnotowane zdjęcie" @click="visibleRight = true;visibleLeft = false; loadAnnotatedImages();" id="edit" class="tools"/>
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
      <p>Wybierz zdjęcie do edycji</p>
      <ul>
      <li v-for="(image, index) in displayed_annotated_images" id="annotated_list">
        <img v-bind:id="index" :src="image" v-if="image" width="200" height="150" @click="selected(index)"/>
      </li>
      </ul>
      <Button label="Załaduj więcej" @click="loadMoreAnnotated()" id="moreR"/>
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
      imported_ind:[],
      annotated:[],
      current_img: null,
      current_real_id:0,
      displayed_imported_images:[],
      displayed_annotated_images:[],
      canvas:null,
      context:null,
      rec_beg_x:[],
      rec_beg_y:[],
      rec_w:[],
      rec_h:[],
      colors:['rgb(255,0,0)', 'rgb(0,128,0)'],
      current_label:'',
      labels:[],
      labels_counter:[],
      rec_counter:0,
      ifButtonDrawClicked:false,
      ifButtonRemoveClicked:false,
      indexOfCurrentImage:0,
      new_rect:false,
      is_rect_finished:false,
      previous_label:'',
      edition_count:0,
      unique_labels:[],
      nr_labels:[],
    }
  },
  methods:
      {
        onEnter:function() {
          if (document.getElementById("object_type").value !== '') {
            if (this.is_rect_finished) {
              this.current_label = document.getElementById("object_type").value;
              document.getElementById("object_type").value = '';
              if (this.edition_count !== 0)
                this.labels.splice(this.labels.length - 1, 1);
              this.labels.push(this.current_label);
              this.drawAllRects();
              if (Object.keys(this.labels_counter).length === 0) {
                this.labels_counter[this.current_label] = 1;
              } else {
                if (this.current_label in this.labels_counter)
                  this.labels_counter[this.current_label] += 1;
                else
                  this.labels_counter[this.current_label] = 1;
                if (this.previous_label !== '' && this.previous_label !== this.current_label && this.edition_count !== 0) {
                  if (this.labels_counter[this.previous_label] === 1)
                    delete this.labels_counter[this.previous_label];
                  else
                    this.labels_counter[this.previous_label] -= 1;
                }
              }
              this.previous_label = this.current_label;
              this.edition_count += 1;
              this.unique_labels = [];
              this.nr_labels = [];
              for (let key in this.labels_counter) {
                if (this.labels_counter.hasOwnProperty(key)) {
                  this.unique_labels.push(key);
                  this.nr_labels.push(this.current_label[key]);
                }
              }
            } else
              document.getElementById("object_type").value = '';
          }
        },

        async saveAnnotations() {
          const dict = {
            "login": app.config.globalProperties.$login.value,
            "password": app.config.globalProperties.$password.value,
            "labels": this.labels,
            "image index": this.current_real_id,
            "rec_beg_x": this.rec_beg_x,
            "rec_beg_y": this.rec_beg_y,
            "rec_w": this.rec_w,
            "rec_h": this.rec_h
          };
          await axios.post("http://localhost:5000/save_annotations", {params: JSON.stringify(dict)})
          return "Ojojoj";
        },

        async loadImportedImages() {
          const dict = {
            "login": app.config.globalProperties.$login.value,
            "password": app.config.globalProperties.$password.value
          };
          const imported = [];
          const imported_ind = [];
          await axios.post("http://localhost:5000/get_imported_images", {params: JSON.stringify(dict)}).then(function (response) {
            for (let i = 0; i < response.data["images"].length; i++) {
              imported.push("data:image/jpeg;base64," + response.data["images"][i]);
              imported_ind.push(response.data["indexes"][i][0]);
            }
            return imported;
          });
          this.imported = imported;
          this.imported_ind=imported_ind;
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
        async loadMoreAnnotated(e) {
          const length = this.displayed_annotated_images.length;
          if (length < 4) {
          } else if (this.annotated.length < length + 4)
            this.displayed_annotated_images.push.apply(this.displayed_annotated_images, this.annotated.slice(length, this.annotated.length));
          else
            this.displayed_annotated_images.push.apply(this.displayed_annotated_images, this.annotated.slice(length, length + 4));
        },
        async selected(index) {
          this.indexOfCurrentImage = index;
          this.current_real_id=this.imported_ind[index];
          this.rec_counter = 0;
          this.rec_beg_x = [];
          this.rec_beg_y = [];
          this.rec_w = [];
          this.rec_h = [];
          this.labels = [];
          this.current_label = '';
          this.labels_counter = [];
          this.unique_labels = [];
          this.nr_labels = [];
          this.ifButtonDrawClicked = false;
          this.ifButtonRemoveClicked = false;
          this.is_rect_finished = false;
          this.previous_label = '';
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
            this.context.fillRect(this.rec_beg_x[i], this.rec_beg_y[i], this.rec_w[i], this.rec_h[i]);
            this.context.strokeRect(this.rec_beg_x[i], this.rec_beg_y[i], this.rec_w[i], this.rec_h[i]);
            if (this.rec_w[i] > 0 && this.rec_h[i] > 0)
              this.context.strokeRect(this.rec_beg_x[i], this.rec_beg_y[i], this.rec_w[i], -20);
            else if (this.rec_w[i] > 0 && this.rec_h[i] < 0)
              this.context.strokeRect(this.rec_beg_x[i], this.rec_beg_y[i] + this.rec_h[i], this.rec_w[i], -20);
            else if (this.rec_w[i] < 0 && this.rec_h[i] > 0)
              this.context.strokeRect(this.rec_beg_x[i], this.rec_beg_y[i], this.rec_w[i], -20);
            else if (this.rec_w[i] < 0 && this.rec_h[i] < 0)
              this.context.strokeRect(this.rec_beg_x[i], this.rec_beg_y[i] + this.rec_h[i], this.rec_w[i], -20);
            this.context.font = "15px Georgia";
            if (this.labels[i] === undefined) {
              if (this.rec_w[i] > 0 && this.rec_h[i] > 0)
                this.context.fillText('', this.rec_beg_x[i] + 5, this.rec_beg_y[i] - 5);
              else if (this.rec_w[i] > 0 && this.rec_h[i] < 0)
                  this.context.fillText('', this.rec_beg_x[i] + 5, this.rec_beg_y[i]+ this.rec_h[i] - 5);
              else if (this.rec_w[i] < 0 && this.rec_h[i] > 0)
                  this.context.fillText('', this.rec_beg_x[i] + this.rec_w[i] + 5, this.rec_beg_y[i] - 5);
              else if (this.rec_w[i] < 0 && this.rec_h[i] < 0)
                  this.context.fillText('', this.rec_beg_x[i] + this.rec_w[i] + 5, this.rec_beg_y[i] + this.rec_h[i] - 5);
            }
            else {
              if (this.rec_w[i] > 0 && this.rec_h[i] > 0)
                this.context.fillText(this.labels[i], this.rec_beg_x[i] + 5, this.rec_beg_y[i] - 5);
              else if (this.rec_w[i] > 0 && this.rec_h[i] < 0)
                  this.context.fillText(this.labels[i], this.rec_beg_x[i] + 5, this.rec_beg_y[i]+ this.rec_h[i] - 5);
              else if (this.rec_w[i] < 0 && this.rec_h[i] > 0)
                  this.context.fillText(this.labels[i], this.rec_beg_x[i] + this.rec_w[i] + 5, this.rec_beg_y[i] - 5);
              else if (this.rec_w[i] < 0 && this.rec_h[i] < 0)
                  this.context.fillText(this.labels[i], this.rec_beg_x[i] + this.rec_w[i] + 5, this.rec_beg_y[i] + this.rec_h[i] - 5);
            }
            }
        },
        drawRectangle() {
            if (this.current_img != null) {
              this.ifButtonDrawClicked = true;
              this.ifButtonRemoveClicked = false;
              let beginning_x = null;
              let beginning_y = null;
              let previous_x = null;
              let previous_y = null;
              let current_x = null;
              let current_y = null;
              this.context.lineWidth = 1;
              let draw = false;
              this.is_rect_finished = false;
              window.addEventListener("mousedown", (e) => {
                if (this.rec_beg_x.length !== this.labels.length && e.target.localName === 'canvas') {
                  this.rec_beg_x.pop();
                  this.rec_beg_y.pop();
                  this.rec_w.pop();
                  this.rec_h.pop();
                  this.rec_counter -= 1;
                  this.drawAllRects();
                  this.context.stroke();
                  this.context.closePath();
                }
                if (e.target.localName === 'canvas' && this.ifButtonDrawClicked === true && this.labels[this.rec_counter - 1] !== '') {
                  this.edition_count = 0;
                  this.new_rect = true;
                  this.is_rect_finished = false;
                  draw = true;
                }
              });
              window.addEventListener("mouseup", (e) => {
                if (e.target.localName === 'canvas') {
                  this.new_rect = false;
                  if (this.ifButtonDrawClicked === true) {
                    if ((((previous_x - beginning_x) * (previous_y - beginning_y) > 1000) || ((previous_x - beginning_x) * (previous_y - beginning_y) < -1000))) {
                      this.is_rect_finished = true;
                      if (this.rec_beg_x.indexOf(beginning_x) === -1 && this.rec_beg_y.indexOf(beginning_y) === -1) {
                        this.rec_beg_x[this.rec_counter] = beginning_x;
                        this.rec_beg_y[this.rec_counter] = beginning_y;
                        this.rec_w[this.rec_counter] = previous_x - beginning_x;
                        this.rec_h[this.rec_counter] = previous_y - beginning_y;
                        this.rec_counter += 1;
                      }
                    }
                    this.drawAllRects();
                    this.context.stroke();
                    this.context.closePath();
                    //realnie po prawej  - dynamiczny podgląd
                    //wydaje się to jednak niepotrzebnym featurem - przycisk do zapisu po prostu wrzuci to zdjęcie na koniec zaadnotowanych
                    //this.displayed_imported_images[this.indexOfCurrentImage] = document.getElementById('myCanvas').toDataURL('image/jpeg');
                    draw = false;
                  } else
                    draw = false;
                }
              });
              window.addEventListener("mousemove", (e) => {
                if (this.ifButtonRemoveClicked !== true) {
                  if ((e.target.localName !== 'canvas' || e.offsetY - 20 < 0) && !this.is_rect_finished) {
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
                }
              });
            }
        },
        deleteRectangle()
        {
          this.ifButtonRemoveClicked = true;
          this.ifButtonDrawClicked = false;
          window.addEventListener("click", (e) => {
              if (e.target.localName === 'canvas' && this.ifButtonRemoveClicked === true) {
                for (let i = this.rec_counter - 1; i > -1; i--)
                {
                  if (((e.offsetX >= this.rec_beg_x[i] && e.offsetX <= this.rec_beg_x[i] + this.rec_w[i])||(e.offsetX <= this.rec_beg_x[i] && e.offsetX >= this.rec_beg_x[i] + this.rec_w[i])) && ((e.offsetY >= this.rec_beg_y[i] && e.offsetY <= this.rec_beg_y[i] + this.rec_h[i])||(e.offsetY <= this.rec_beg_y[i] && e.offsetY >= this.rec_beg_y[i] + this.rec_h[i])))
                  {
                    this.rec_beg_x.splice(i, 1);
                    this.rec_beg_y.splice(i, 1);
                    this.rec_w.splice(i, 1);
                    this.rec_h.splice(i, 1);
                    if (this.labels_counter[this.labels[i]] > 1)
                    {
                      this.labels_counter[this.labels[i]] -= 1;
                    }
                    else {
                      delete this.labels_counter[this.labels[i]];
                    }
                    this.labels.splice(this.labels.indexOf(this.labels[i]), 1);
                    this.unique_labels = [];
                    this.nr_labels = [];
                    for (let key in this.labels_counter) {
                      if (this.labels_counter.hasOwnProperty(key)) {
                        this.unique_labels.push(key);
                        this.nr_labels.push(this.current_label[key]);
                      }
                    }
                    this.rec_counter -= 1;
                  }
                }
                this.drawAllRects();
                this.context.stroke();
                this.context.closePath();
              }
            });
        }
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
  background: white;
}

#lista p{
  color: black;
}

#kanwas{
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.clr{
    height: 20px;
    width: 20px;
    background-color: blue;
    border-radius: 50%;
    border: 3px solid rgb(214, 214, 214);
    transition: transform .5s;
    color:red;
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

#typy{
  list-style: circle;
  width: 20%;
  margin-left: auto;
  margin-right: auto;
  margin-top: 5px;
}

#typy li{
  margin-top: 10px;
  color: black;
}

#typy li span{
  color: black;
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
  border-right: solid 2px;
  border-bottom: solid 2px;
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
  border-left: solid 2px;
  border-bottom: solid 2px;
}

.p-sidebar-right .p-sidebar-close:before{
  content: "▶";
}

.p-sidebar-left .p-sidebar-close:before{
  content: "◀";
}

p{
  color: white;
}

a{
  color: white;
}

#moreL {
  height: 7%;
  width: 10%;
  position: fixed;
  bottom: 5px;
  left: 4.7%;
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
  height: 7%;
  width: 10%;
  position: fixed;
  bottom: 5px;
  right: 4.7%;
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