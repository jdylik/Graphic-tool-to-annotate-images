<template>
<div id="import">
    <p>{{"Kliknij, jeżeli chcesz dodać folder zdjęć"}}</p>
    <input type="file" id="input_folder" @change="onFolder" webkitdirectory directory multiple/>
    <p>{{"Kliknij, jeżeli chcesz dodać zdjęcie"}}</p>
    <input type="file" id="input_file" @change="onFile"/>
</div>
</template>

<script>
import Edit_images from "@/views/Edit_images.vue";
import axios from "axios";
export default {
  name: "Import_images",
    data: function(){
        return {
          imgSrc:'',
          imgsSrc:[],
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
            this.imgSrc = this.imgSrc.split(",")[1];
            let blob_img = this.convert_to_blob(this.imgSrc);
            //axios.post("http://localhost:5000/insert_new_image", {'blob_img':blob_img});
            //this.blob_img_d = window.URL.createObjectURL(blob_img);loading from
          };
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
        convert_to_blob: function(imgSrc)
        {
          const byteCharacters = atob(imgSrc);
          const byteArrays = [];

          for (let offset = 0; offset < byteCharacters.length; offset += 512)
          {
            const slice = byteCharacters.slice(offset, offset + 512);

            const byteNumbers = new Array(slice.length);
            for (let i = 0; i < slice.length; i++)
            {
              byteNumbers[i] = slice.charCodeAt(i);
            }

            const byteArray = new Uint8Array(byteNumbers);
            byteArrays.push(byteArray);
          }

          const blob = new Blob(byteArrays, {type:'image/jpeg'});
          return blob;
        }

      },

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