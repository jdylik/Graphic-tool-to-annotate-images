<template>
<div id="input">
    <p>{{"Kliknij, jeżeli chcesz dodać folder zdjęć"}}</p>
    <input type="file" id="input_folder" webkitdirectory directory multiple />
    <p>{{"Kliknij, jeżeli chcesz dodać zdjęcie"}}</p>
    <input type="file" id="input_folder" />
</div>
</template>

<script>
export default {
  name: "Import_images",
    data: function(){
        return {
            files: 0
        }
    },
  methods:
      {
        get_files: function()
        {
          let files = document.getElementById("input_folder").files;
          this.files = files.length;
          alert("std")
        }

      }
}
</script>