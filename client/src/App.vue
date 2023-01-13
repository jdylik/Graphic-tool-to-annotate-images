<template xmlns="http://www.w3.org/1999/html">
  <div id="container">
    <div id="title">
      <h1>Narzędzie do adnotacji zdjęć na potrzeby algorytmów detekcji</h1>
    </div>
    <nav>
      <button class="button">
        <router-link to="/login">Zaloguj się</router-link>
      </button>
      <button class="button">
        <router-link to="/import">Importuj</router-link>
      </button>
      <button class="button">
        <router-link to="/edit">Edytuj</router-link>
      </button>
      <button class="button">
        <router-link to="/logout">Wyloguj się</router-link>
      </button>

    </nav>
    <router-view/>
    </div>
  <footer>
      <div id="footer">&copy Katarzyna Prokop, Jan Dylik, Adrian Matlok, Michał Pluszczewski</div>
  </footer>

</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

body{
  background-image: url("background.jpg");
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: white;
}

nav a.router-link-exact-active {
  color: #6ce8ac;
}

#container {
	width: 100%;
  min-height:100vh;
	margin-left: auto;
	margin-right: auto;
  position:relative
}

#title {
	background-color:#3366CC;
	text-align: center;
	text-shadow: 1px 1px #ff0000;
  margin: auto;
	vertical-align: middle;
	color: #FFFFF0;
	padding: 15px;
	font-size: xx-large;
	font-family: 'Audiowide', sans-serif;
}

footer {
    clear: both;
    position: sticky;
    height: 100px;
}

#footer {
	position:absolute;
	bottom:0px;
  color: aliceblue;
	width:100%;
	clear:both;
	text-align: center;
	font-family: 'Autowide', cursive;
	padding: 10px;
	background-color: black;
  margin-bottom:-200px;
}

.button {
  height: 50px;
  width: 150px;
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

.button:hover {background-color: #2c3e50}

.button:active {
  background-color: #2c3e50;
  transform: translateY(4px);
}
body {
	overflow-x:hidden;
}
</style>
