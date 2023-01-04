
<template>
  <div id="edit">
    <Button label="Edytuj nieadnotowane zdjęcie" @click="visibleLeft = true" />
    <Button label="Edytuj adnotowane zdjęcie" @click="visibleRight = true" />
    <Sidebar v-model:visible="visibleLeft" position="left" class="sidebar_left" id="sidebar_left">
      <a href="#">About</a>
      <a href="#">Services</a>
      <a href="#">Clients</a>
      <a href="#">Contact</a>
      <img :src="img" v-if="img"/>
    </Sidebar>
    <Sidebar v-model:visible="visibleRight" position="right" class="sidebar_right" id="sidebar_right">
      <a href="#">About</a>
      <a href="#">Services</a>
      <a href="#">Clients</a>
      <a href="#">Contact</a>
      <img :src="img" v-if="img"/>
    </Sidebar>
  </div>
</template>

<script>
import Import_images from '../views/Import_images.vue'

export default {
  name: "Edit_images",
  components:
      {
        Import_images
      },
  img:"",
  data: function() {
    return {
      info: "",
      std:"",
      img:"",
      imn:0,
      visibleLeft:false,
      visibleRight:false,
    }
  },
  mounted:async function()
  {
        //Import_images.ims = 7;
        //this.imn = Import_images.data.ims;
        console.log(Import_images.ims);
        console.log(this.imn);
        Import_images.ims = 25;
        console.log(Import_images.ims)
        const files = Import_images.files;
        //console.log(files);
        const reader = new FileReader();
        reader.readAsDataURL(files);
        this.img = reader.result;
        reader.onload = () => (this.img = reader.result);
        //console.log("std");
        //const gResponse = await fetch("http://localhost:5000/name");
        //const gObject = await gResponse.json();
        //this.info = gObject.name;
  }

}
</script>

<style scoped>
#sidebar_left
{
  color:#111;
  border: 2px solid powderblue;
}
</style>