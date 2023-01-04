<template>
<div id="import">
    <p>{{"Kliknij, jeżeli chcesz dodać folder zdjęć"}}</p>
    <input type="file" id="input_folder" @change="onFolder" webkitdirectory directory multiple/>
    <p>{{"Kliknij, jeżeli chcesz dodać zdjęcie"}}</p>
    <input type="file" id="input_folder" @change="onFile"/>
    <img :src="imgSrc" v-if="imgSrc"/>
</div>
</template>

<script>
import Edit_images from "@/views/Edit_images.vue";
export default {
  name: "Import_images",
  files:'',
  components:
      {
        Edit_images
      },
    data: function(){
        return {
          imgSrc:'',
          imgsSrc:[],
          ims:0,
        }
    },
  mounted:async function()
  {
    this.ims = 500;
  },
  methods:
      {
        onFile(e)
        {
          //Edit_images.imn = 20;
          console.log(Edit_images.imn);
          console.log(this.ims);
          this.ims = 6;
          console.log(this.ims);
          this.files = e.target.files[0];
          console.log(this.files);
          const reader = new FileReader();
          reader.readAsDataURL(this.files);
          this.imgSrc = reader.result;
          reader.onload = () => (this.imgSrc = reader.result);
        },
        onFolder(e)
        {
          const files = e.target.files;
          const reader = new FileReader();
          for (let i = 0; i < files.length;i++)
          {
            reader.readAsDataURL(files[i]);
            this.imgsSrc[i] = reader.result;
          }
        },
        get_files: function()
        {
          let files = document.getElementById("input_folder").files;
          this.files = files.length;
          alert("std")
        }

      }
}
</script>
<style>
p{
  padding: 15px;
  font-size: large;
}
input{
  font-size: medium;
}
</style>