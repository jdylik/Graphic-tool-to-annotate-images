<template xmlns="http://www.w3.org/1999/html">
  <div id="container">
    <div id="title">
      <h1>Narzędzie do adnotacji zdjęć na potrzeby algorytmów detekcji</h1>
    </div>
    <nav>
      <button class="button">
        <router-link style="text-decoration: none; color: inherit;" to="/login">Zaloguj się</router-link>
      </button>
      <button class="button">
        <router-link style="text-decoration: none; color: inherit;" to="/import">Importuj</router-link>
      </button>
      <button class="button">
        <router-link style="text-decoration: none; color: inherit;" to="/edit">Edytuj</router-link>
      </button>
      <button class="button">
        <router-link style="text-decoration: none; color: inherit;" to="/logout">Wyloguj się</router-link>
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
  background: no-repeat center/140% url("background.jpg");
  overflow-x: hidden;
  height: 100%;

}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #e0e1dd;
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
	background-color:#0d1b2a;
	text-align: center;
	text-shadow: 1px 1px #ff0000;
  margin: auto;
	vertical-align: middle;
	color: #e0e1dd;
	padding: 15px;
	font-size: xx-large;
  font-family: Bahnschrift;
	/*font-family: 'Audiowide', sans-serif;*/
}

#footer {
	position:fixed;
	bottom:0px;
  color: #e0e1dd;
	width:100%;
	clear:both;
	text-align: center;
	font-family: 'Courier New', monospace;
	padding: .5em;
	background-color: #0d1b2a;
}

.button {
  height: 50px;
  width: 150px;
  padding: 5px;
  font-size: 15px;
  text-align: center;
  cursor: pointer;
  outline: none;
  color: #e0e1dd;
  background-color: #1b263b;
  /*border-radius: 15px;*/
  /*margin-left: 5px;*/
  /*margin-right: 5px;*/
}

.button:hover {background-color: #2c3e50}

.button:active {
  background-color: #2c3e50;
  transform: translateY(4px);
}
body {
	overflow-x:hidden;
}

footer{
    margin-top:5%;
}
</style>
