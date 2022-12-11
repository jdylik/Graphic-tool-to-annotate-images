<template>
<div id="app">
    <input type="file" id="input_folder" style="display:none;" onblur="this.get_files()" webkitdirectory directory multiple />
    <label for="input_folder" style="cursor: pointer; border: 1px solid red;">Import folders</label>
  <p>{{this.files}}</p>
</div>
</template>

<script>
export default {
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