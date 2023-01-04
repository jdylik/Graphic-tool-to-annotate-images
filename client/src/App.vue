<template xmlns="http://www.w3.org/1999/html">
  <div id="container">
    <div id="title">
      <h1>Narzędzie do adnotacji zdjęć na potrzeby algorytmu detekcji</h1>
    </div>
    <nav>
      <button>
        <router-link to="/login">Zaloguj się</router-link>
      </button>
      <button>
        <router-link to="/import">Importuj</router-link>
      </button>
      <button>
        <router-link to="/edit">Edytuj</router-link>
      </button>

    </nav>
    <router-view/>
    <footer>
      <div id="footer">&copy Katarzyna Prokop, Jan Dylik, Adrian Matlok, Michał Pluszczewski</div>
    </footer>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

#container {
	width: 100%;
	height: 100%;
	margin-left: auto;
	margin-right: auto;
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

#footer {
	position:absolute;
	bottom:0px;
  color: aliceblue;
	width:100%;
	clear:both;
	text-align: center;
	font-family: 'Autowide', cursive;
	padding: 10px;
	background-color: black
}

button {
  border: 3px solid black;
  background-color: steelblue;
  height: 50px;
  width: 150px;
  margin-left: 5px;
  margin-right: 5px;
  font-size: large;
}

body {
	overflow-x:hidden;
}
</style>
