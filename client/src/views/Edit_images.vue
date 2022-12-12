<template>
<div id="information">
  <p>{{info}}</p>
</div>
</template>

<script>
export default {
  name: "Edit_images",
  data: function() {
    return {
      info: ""
    }
  },
  created:async function()
  {
        console.log("std");
        const gResponse = await fetch("http://localhost:5000/name");
        const gObject = await gResponse.json();
        this.info = gObject.name;
  }

}
</script>

<style scoped>

</style>