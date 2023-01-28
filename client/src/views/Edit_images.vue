
<template>
  <div id="pageWrap">
    <p>{{work_option}}</p>
    <div id="kanwas">
          <div id="add_data">
      <p>{{"Wybierz nazwę pliku"}}</p>
        <input type="text" id="file_name"/>
      <p>{{"Wybierz rodzaj kamery"}}</p>
        <input type="text" id="camera_type"/>
      <p>{{"Wpisz lokalizację wykonania zdjęcia"}}</p>
        <input type="text" id="location"/>
    </div>
      <canvas id="myCanvas" width="666" height="500" style="border:5px solid black;"/>
      <!--ta lista oraz pole input poniżej ma się znaleźć obok canvasa-->
      <div id="lista">
        <p>{{"Określ typ adnotowanego obiektu"}}</p>
        <input type="text" id="object_type" v-on:keyup.enter="onEnter"/>
        <ul id="typy">
          <li v-for="(value, index) in unique_labels"  id="kolko">
            <span>{{ value }} - {{nr_labels[index]}}</span>
          </li>
        </ul>
      </div>

    </div>
    <div id="row1">
      <Button label="Rysuj" @click="drawRectangle();" id="draw" class="tools"/>
      <Button label="Usuń" @click="deleteRectangle();" class="tools"/>
      <Button label="Zapisz" @click="saveAnnotations()" class="tools"/>
      <Button label="Eksportuj" @click="exportData()" class="tools"/>
    </div>

    <div id="row2">
      <Button label="Edytuj nieadnotowane zdjęcie" @click="visibleLeft = true; visibleRight = false; loadImportedImages();" id="editimp" class="tools"/>
      <Button label="Edytuj adnotowane zdjęcie" @click="visibleRight = true;visibleLeft = false; loadAnnotatedImages();" id="editann" class="tools"/>
    </div>

    <Sidebar v-model:visible="visibleLeft" position="left" class="sidebar_left" id="sidebar_left">
      <p class="sidebar-message">Wybierz zdjęcie do edycji</p>
      <ul>
      <li v-for="(image, index_l) in displayed_imported_images" id="import_list">
        <img v-bind:id="index_l" :src="image" v-if="image" width="200" height="150" @click="selected(index_l,1)" class="img_bars"/>
      </li>
      </ul>
      <Button label="Załaduj więcej" @click="loadMoreImported()" id="moreL"/>
    </Sidebar>

    <Sidebar v-model:visible="visibleRight" position="right" class="sidebar_right" id="sidebar_right">
      <p class="sidebar-message">Wybierz zdjęcie do edycji</p>
      <ul>
      <li v-for="(image, index_r) in displayed_annotated_images" id="annotated_list">
        <img v-bind:id="index_r" :src="image" v-if="image" width="200" height="150" @click="selected(index_r,2)" class="img_bars"/>
      </li>
      </ul>
      <Button label="Załaduj więcej" @click="loadMoreAnnotated()" id="moreR"/>
    </Sidebar>


  </div>
</template>

<script>
import {app} from "@/main";
import axios from "axios";
import router from "@/router";

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
      unique_colors:[],
      fill_colors:[],
      stroke_colors:[],
      //fill_colors_for_labels:[],
      //stroke_colors_for_labels:[],
      strokeColor:[],
      fillColor:[],
      if_deleted:false,
      work_option:"Tryb: ",
      common_fill_colors_for_labels:null,
      common_stroke_colors_for_labels:null,
      source:'',
      file_name:'',
      camera_type:'',
      location:'',
    }
  },
  methods:
      {
        onEnter:function() {
          this.ifButtonDrawClicked = false;
          if (document.getElementById("object_type").value !== '') {
            if (this.rec_beg_x.length !== 0 && !this.if_deleted) {
              if (this.is_rect_finished) {
                if (document.getElementById("object_type").value.length / this.rec_w[this.rec_counter - 1] > 0.15) {
                  alert("Podpis zdjęcia jest za długi! Zaleca się zmianę podpisu w celu braku utraty danych.")
                  this.current_label = '...';
                } else
                  this.current_label = document.getElementById("object_type").value;
                document.getElementById("object_type").value = '';
                if (this.edition_count !== 0) {
                  this.labels.splice(this.labels.length - 1, 1);
                }
                this.labels.push(this.current_label);
                if (Object.keys(this.common_fill_colors_for_labels).includes(this.current_label)) {
                  this.stroke_colors.splice(this.stroke_colors.length - 1, 1);
                  this.fill_colors.splice(this.fill_colors.length - 1, 1);
                  this.stroke_colors.push(this.common_stroke_colors_for_labels[this.current_label]);
                  this.fill_colors.push(this.common_fill_colors_for_labels[this.current_label]);
                }
                if (!(Object.keys(this.common_fill_colors_for_labels).includes(this.current_label))) {
                  this.labels_counter[this.current_label] = 1;
                  this.common_fill_colors_for_labels[this.current_label] = this.fill_colors[this.fill_colors.length-1];
                  this.common_stroke_colors_for_labels[this.current_label] = this.stroke_colors[this.stroke_colors.length-1];
                }
                else if (!(Object.keys(this.labels_counter).includes(this.current_label))) {
                  this.labels_counter[this.current_label] = 1;
                }else
                {
                  this.labels_counter[this.current_label] += 1;
                }
                if (this.previous_label !== this.current_label && this.labels_counter[this.previous_label] > 1 && this.edition_count !== 0)
                  this.labels_counter[this.previous_label] -= 1;
                else if (this.previous_label !== this.current_label && this.labels_counter[this.previous_label] <= 1 && this.edition_count !== 0) {
                  delete this.labels_counter[this.previous_label];
                }
                this.previous_label = this.current_label;
                this.edition_count += 1;
                this.unique_labels = [];
                this.nr_labels = [];
                for (let key in this.labels_counter) {
                  if (this.labels_counter.hasOwnProperty(key)) {
                    this.unique_labels.push(key);
                    this.nr_labels.push(this.labels_counter[key]);
                  }
                }
                this.drawAllRects();
                this.work_option = "Tryb: ";
              } else
                document.getElementById("object_type").value = '';
            } else
              document.getElementById("object_type").value = '';
          }
        },
        async exportData() {
          await router.push({path: '/export'});
        },

        async saveAnnotations() {
          if (document.getElementById("file_name").value !== '') {
            let image = '';
            if (this.source === 'importowane')
              image = this.imported[this.indexOfCurrentImage].split("data:image/jpeg;base64,")[1];
            else
              image = this.annotated[this.indexOfCurrentImage].split("data:image/jpeg;base64,")[1];
            let element, previous;
            let fatal_indexes = [];
            console.log(this.rec_beg_x)
            for (let i = 0; i < this.labels.length; i++) {
              element = this.rec_beg_x[i];
              if (element === previous && this.rec_beg_y[i] === this.rec_beg_y[i - 1] && this.rec_w[i] === this.rec_w[i - 1] && this.rec_h[i] === this.rec_h[i - 1])
                fatal_indexes.push(i);
              previous = element;
            }
            for (let i = 0; i < fatal_indexes.length; i++) {
              this.labels.splice(fatal_indexes[i], 1);
              this.rec_beg_x.splice(fatal_indexes[i], 1);
              this.rec_beg_y.splice(fatal_indexes[i], 1);
              this.rec_w.splice(fatal_indexes[i], 1);
              this.rec_h.splice(fatal_indexes[i], 1);
              this.stroke_colors.splice(fatal_indexes[i], 1);
              this.fill_colors.splice(fatal_indexes[i], 1);
            }
            console.log(this.rec_beg_x);
            const inf_dict = {
              "login": app.config.globalProperties.$login.value,
              "password": app.config.globalProperties.$password.value,
              "image": image,
              "name": this.file_name,
              "camera": this.camera_type,
              "location": this.location,
            }
            if (this.camera_type !== '')
              inf_dict["camera"] = this.camera_type;
            if (this.location !== '')
              inf_dict["location"] = this.location;
            await axios.post("http://localhost:5000/save_image_info", {params: JSON.stringify(inf_dict)})
            const dict = {
              "login": app.config.globalProperties.$login.value,
              "password": app.config.globalProperties.$password.value,
              "labels": this.labels,
              "image": image,
              "rec_beg_x": this.rec_beg_x,
              "rec_beg_y": this.rec_beg_y,
              "rec_w": this.rec_w,
              "rec_h": this.rec_h,
              "fill_colors": this.fill_colors,
              "stroke_colors": this.stroke_colors,
            };
            await axios.post("http://localhost:5000/save_annotations", {params: JSON.stringify(dict)})
            this.context.reset();
            this.current_img = null;
            this.labels_counter = [];
            this.unique_labels = [];
            this.nr_labels = [];
            this.camera_type = '';
            this.location = '';
            document.getElementById("file_name").value = '';
            document.getElementById("camera_type").value = '';
            document.getElementById("location").value = '';
          }
          else {
            alert("Aby zapisać zmiany, musisz sprecyzować nazwę pliku wynikowego.")
          }
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
            "password": app.config.globalProperties.$password.value,
          };
          const annotated = [];
          const annotated_ind = [];                                                                                                                                                                                                                                                                                                                                                                                                                                                                             0
          await axios.post("http://localhost:5000/get_annotated_images_no_rects", {params: JSON.stringify(dict)}).then(function (response) {
            let data = response.data["images"];
            for(let i = 0; i < data.length; i++)
            {
              //let canvas = document.createElement('canvas');
              //canvas.width = 200;
              //canvas.height = 150;
              //let ctx = canvas.getContext('2d');
              //ctx.globalAlpha = 1;
              //let image = document.createElement('image');
              //ctx.fillStyle = '#fff';
              //ctx.fillRect(0, 0, canvas.width, canvas.height);
              //image.onload = function() {
               // ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
              //};
              //image.src = "data:image/jpeg;base64," + data[i][1];
              //let start_x = data[i][2];
              //let start_y = data[i][3];
              //let width = data[i][4];
              //let height = data[i][5];
              //let label = data[i][6];
              //ctx.fillStyle = `rgb(${data[i][8].toString().split(",")[0].split("[")[1]}, ${data[i][8].toString().split(",")[1]}, ${data[i][8].toString().split(",")[2].split("]")[0]})`;
              //ctx.fillRect(start_x / 3.33, start_y / 3.33, width / 3.33, height / 3.33);
              //ctx.strokeRect(start_x, start_y, width, height);
              //let stroke_color = "rgb(" + data[i][7].toString().split(",")[0].split("[")[7] + ", " + data[i][7].toString().split(",")[1] + ", " + data[i][7].toString().split(",")[2].split("]")[0] + ")";
              //let url = canvas.toDataURL('image/jpeg');
              //ctx.strokeRect(start_x, start_y, width, height);
              annotated.push("data:image/jpeg;base64," + data[i]);
              annotated_ind.push(response.data["indexes"][i][0]);
            }
            return annotated;
          });
          this.annotated = annotated;
          this.annotated_ind=annotated_ind;
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
        async selected(index,num) {
          document.getElementById("file_name").value = '';
          document.getElementById("camera_type").value = '';
          document.getElementById("location").value = '';
          document.getElementById("object_type").value = '';
          this.source = 'importowane';
          this.work_option="Tryb: ";
          this.indexOfCurrentImage = index;
          this.current_real_id=this.imported_ind[index];
          this.rec_counter = 0;
          this.rec_beg_x = [];
          this.rec_beg_y = [];
          this.rec_w = [];
          this.rec_h = [];
          this.stroke_colors = [];
          this.fill_colors = [];
          this.fillColor = [];
          this.strokeColor = [];
          this.unique_colors = [];
          this.fill_colors_for_labels = [];
          this.stroke_colors_for_labels = [];
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
          this.context.globalAlpha = 1;
          if (num===2)
          {
            this.source = 'adnotowane';
            const dict = {
            "login": app.config.globalProperties.$login.value,
            "password": app.config.globalProperties.$password.value,
            "image": this.annotated[this.indexOfCurrentImage].split("data:image/jpeg;base64,")[1],
            };
            let response_ad = await axios.post("http://localhost:5000/get_image_info", {params: JSON.stringify(dict)})
            let data = response_ad.data["description"]
            console.log(data)
            document.getElementById("file_name").value = data[2];
            document.getElementById("camera_type").value = data[0];
            document.getElementById("location").value = data[1];
            this.file_name = data[2];
            this.camera_type = data[0];
            this.location = data[1];
            const rec_beg_x=[];
            const rec_beg_y=[];
            const rec_w=[];
            const rec_h=[];
            const labels=[];
            const stroke_colors=[];
            const fill_colors=[];
            let response = await axios.post("http://localhost:5000/get_annotations", {params: JSON.stringify(dict)})//.then(function (response) {
            for (let i = 0; i < response.data["stroke_cols"].length; i++) {
              rec_beg_x.push(response.data["rec_beg_x"][i]);
              rec_beg_y.push(response.data["rec_beg_y"][i]);
              rec_w.push(response.data["rec_w"][i]);
              rec_h.push(response.data["rec_h"][i]);
              labels.push(response.data["labels"][i]);
              console.log(response.data["stroke_cols"][i])
              let strokes = response.data["stroke_cols"][i].split(", ");
              let stroke = [];
              stroke.push(parseFloat(strokes[0].split("[")[1]));
              stroke.push(parseFloat(strokes[1]));
              stroke.push(parseFloat(strokes[2].split("]")[0]));
              stroke_colors.push(stroke);
              let fills = response.data["fill_cols"][i].split(", ");
              let fill = [];
              fill.push(parseFloat(fills[0].split("[")[1]));
              fill.push(parseFloat(fills[1]));
              fill.push(parseFloat(fills[2].split("]")[0]));
              fill_colors.push(fill);
            }
            this.rec_beg_x=rec_beg_x;
            this.rec_beg_y=rec_beg_y
            this.rec_w=rec_w;
            this.rec_h=rec_h;
            this.labels=labels;
            this.stroke_colors=stroke_colors;
            this.fill_colors=fill_colors;
            this.rec_counter=this.rec_beg_x.length;
            for (let i = 0; i < this.labels.length; i++)
            {
              if (Object.hasOwn(this.labels_counter, this.labels[i])) {
                this.labels_counter[this.labels[i]] += 1;
                console.log(this.labels_counter)
              }
              else
                this.labels_counter[this.labels[i]] = 1;
            }
            this.unique_labels = Object.keys(this.labels_counter);
            this.nr_labels = Object.values(this.labels_counter);
            this.drawAllRects();
          }


        },
        drawAllRects()
        {
          console.log(this.stroke_colors)
          this.context.beginPath();
          this.context.drawImage(this.current_img, 0, 0, this.current_img.width * 3.33, this.current_img.height * 3.33);
          for(let i = 0; i < this.rec_counter; i++)
          {
            this.context.strokeStyle = `rgb(${this.stroke_colors[i][0]}, ${this.stroke_colors[i][1]}, ${this.stroke_colors[i][2]})`;
            this.context.fillStyle = `rgb(${this.fill_colors[i][0]}, ${this.fill_colors[i][1]}, ${this.fill_colors[i][2]}, 0.2)`;
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
            this.context.fillStyle = "rgb(0, 0, 0)";
            this.context.font = "bold 15px Serif";
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
            this.context.fillStyle = `rgb(${this.fill_colors[i][0]}, ${this.fill_colors[i][1]}, ${this.fill_colors[i][2]}, 0.2)`;
            }
        },
        drawRectangle() {
            this.work_option="Tryb: rysowanie";
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
                if (e.target.localName === 'canvas' && this.ifButtonDrawClicked) {
                  this.if_deleted = false;
                  this.visibleLeft = false;
                  this.visibleRight = false;
                }
                if (e.target.localName === 'canvas') {
                  if(this.ifButtonDrawClicked === true)
                  if (this.ifButtonRemoveClicked !== true && this.ifButtonDrawClicked === true) {
                    if (this.rec_beg_x.length !== this.labels.length) {
                      this.rec_beg_x.pop();
                      this.rec_beg_y.pop();
                      this.rec_w.pop();
                      this.rec_h.pop();
                      this.stroke_colors.pop();
                      this.fill_colors.pop();
                      this.rec_counter -= 1;
                      if (this.rec_counter < 0)
                        this.rec_counter = 0;
                      this.drawAllRects();
                      this.context.stroke();
                      this.context.closePath();
                    }
                    if (this.rec_counter === this.stroke_colors.length) {
                      console.log(this.common_stroke_colors_for_labels);
                      this.strokeColor = this.getRandomRGB();
                      console.log(this.strokeColor);
                      this.fillColor = this.strokeColor.map(function (x) {
                        return x * 1.5;
                      });
                      this.stroke_colors.push(this.strokeColor);
                      this.fill_colors.push(this.fillColor);
                    }
                    if (this.ifButtonDrawClicked === true && this.labels[this.rec_counter - 1] !== '') {
                      this.edition_count = 0;
                      this.new_rect = true;
                      this.is_rect_finished = false;
                      draw = true;
                    }
                  }
                }
              });
              window.addEventListener("mouseup", (e) => {
                if (e.target.localName === 'canvas') {
                  this.new_rect = false;
                  if (this.ifButtonDrawClicked === true && this.ifButtonRemoveClicked === false) {
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
                    // else {
                    //   this.stroke_colors.pop();
                    //   this.fill_colors.pop();
                    // }
                    //while (this.stroke_colors.length !== this.rec_counter)
                    //{
                    //  this.stroke_colors.pop();
                    //  this.fill_colors.pop();
                    //}
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
                if (this.ifButtonRemoveClicked !== true && this.ifButtonDrawClicked === true) {
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
                  this.context.strokeStyle = `rgb(${this.strokeColor[0]}, ${this.strokeColor[1]}, ${this.strokeColor[2]})`;
                  this.context.fillStyle = `rgb(${this.fillColor[0]}, ${this.fillColor[1]}, ${this.fillColor[2]}, 0.2)`;
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
          this.work_option="Tryb: usuwanie";
          this.if_deleted = true;
          this.ifButtonRemoveClicked = true;
          this.ifButtonDrawClicked = false;
          window.addEventListener("click", (e) => {
              if (e.target.localName === 'canvas' && this.ifButtonRemoveClicked === true && this.labels.length === this.rec_beg_x.length) {
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
                      delete this.fill_colors_for_labels[this.labels[i]];
                      delete this.stroke_colors_for_labels[this.labels[i]];
                    }
                    this.labels.splice(i, 1);
                    this.fill_colors.splice(i, 1);
                    this.stroke_colors.splice(i, 1);
                    this.unique_labels = [];
                    this.nr_labels = [];
                    for (let key in this.labels_counter) {
                      if (this.labels_counter.hasOwnProperty(key)) {
                        this.unique_labels.push(key);
                        this.nr_labels.push(this.labels_counter[key]);
                      }
                    }
                    this.rec_counter -= 1;
                  }
                }
                this.drawAllRects();
                this.work_option="Tryb: ";
                this.context.stroke();
                this.context.closePath();
                this.ifButtonRemoveClicked = false;
                console.log("lab", this.common_fill_colors_for_labels);
                console.log("col", this.fill_colors)
              }
            });
        },
        getRandomRGB()
        {
          let r = Math.floor(Math.random() * 255);
          let g = Math.floor(Math.random() * 255);
          let b = Math.floor(Math.random() * 255);
          let rs = []
          let gs = []
          let bs = []
          for(let i = 0; i < this.fill_colors.length; i++)
          {
            rs.push(this.fill_colors[i][0])
            gs.push(this.fill_colors[i][1])
            bs.push(this.fill_colors[i][2])
          }
          while(true)
          {
            if ((r === 0 && g === 0 && b === 0) || ((r === 255 && g === 255 && b === 255)|| rs.includes(r) || gs.includes(g) || bs.includes(b)))
            {
              r = Math.floor(Math.random() * 255);
              g = Math.floor(Math.random() * 255);
              b = Math.floor(Math.random() * 255);
            }
            else
              break;
          }
          return [r, g, b]
        },
      },
      async mounted()
      {
        document.getElementById("file_name").addEventListener("input", (event) =>
        {
          if (this.current_img !== null) {
            let file_name = document.getElementById("file_name").value;
            if (file_name !== '' && !file_name.includes(" ") && !file_name.includes("\"")) {
              this.file_name = file_name;
            }
          }
          else
            document.getElementById("file_name").value = '';
        });
        document.getElementById("camera_type").addEventListener("input", (event) =>
        {
          if (this.current_img !== null) {
            let camera_type = document.getElementById("camera_type").value;
            if (camera_type !== '' && !camera_type.includes(" ") && !camera_type.includes("\"")) {
              this.camera_type = camera_type;
            }
          }
          else
            document.getElementById("camera_type").value = '';
        });
        document.getElementById("location").addEventListener("input", (event) =>
        {
          if (this.current_img !== null) {
            let location = document.getElementById("location").value;
            if (location !== '' && !location.includes(" ") && !location.includes("\"")) {
              this.location = location;
            }
          }
          else
            document.getElementById("location").value = '';
        });
        this.canvas = document.getElementById("myCanvas");
        this.context = this.canvas.getContext("2d");
        const req_dict = {
            "login": app.config.globalProperties.$login.value,
            "password": app.config.globalProperties.$password.value,
            };
          let com_fill = [];
          let com_str = [];
          await axios.post("http://localhost:5000/get_categories", {params: JSON.stringify(req_dict)}).then(function (response) {
            if (response.data === 1)
              {}
            else
              {
                for (let i = 0; i < response.data["names"].length; i++) {
                  com_fill[response.data["names"][i]] = response.data["fill_colors"][i];
                  com_str[response.data["names"][i]] = response.data["stroke_colors"][i];
                }

              }
          });
          this.common_fill_colors_for_labels = com_fill;
          this.common_stroke_colors_for_labels = com_str;
      }
}
</script>

<style>

canvas{
  background: #e0e1dd;
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
    border: 3px solid #e0e1dd;
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
  color: #0d1b2a;
  background-color: #e0e1dd;
  border-radius: 15px;
  margin-left: 5px;
  margin-right: 5px;
}

.tools:hover {background-color: #415a77}

.tools:active {
  background-color: #2c3e50;
  transform: translateY(4px);

}

ul
{
  list-style-tuple:none;
}


#edit{
  background-color: #778da9;
}
#edit:hover {background-color: #415a77}
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
  background-color: #0d1b2a;
  border: solid 2px #e0e1dd;
  color: #e0e1dd;
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
  color: #e0e1dd;
}

a{
  color: #e0e1dd;
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
  color: #0d1b2a;
  background-color: #778da9;
  border-radius: 15px;
  margin-left: 5px;
  margin-right: 5px;
}

#moreL:hover {background-color: #415a77}

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
  color: #0d1b2a;
  background-color: #778da9;
  border-radius: 15px;
  margin-left: 5px;
  margin-right: 5px;
}

#moreR:hover {background-color: #415a77}

#moreR:active {
  background-color: #2c3e50;
  transform: translateY(4px);
}

a{
  padding: 15px;
}
.sidebar-message{
  color:#e0e1dd;
}
.img_bars{
  box-shadow: 4px 4px 8px rgba(170, 170, 170, 0.6);
  margin-top: 10px;
}
.img_bars:hover{
  box-shadow: 6px 6px 9px rgba(170, 170, 170, 0.8);
  cursor: pointer;
}
</style>