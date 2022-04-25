<template>
  <nav class="navbar navbar-expand-md navbar-light bg-dark sticky-top border-bottom shadow-sm">
    <router-link to="/" class="navbar-brand" href="#" style="margin-left: 30px">
      <img src="/img/triang.png" alt="Logo" style="width:50px;">
    </router-link>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02"
            aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
      <ul class="navbar-nav ml-auto" style="padding-right: 15%">
        <li class="nav-item active" style="padding-right: 30px">
          <router-link to="/"  class="nav-link text-white"><h5>Главная</h5></router-link>
        </li>
        <li class="nav-item active" style="padding-right: 30px">
          <router-link to="/events"  class="nav-link text-white"><h5>Ивенты</h5></router-link>
        </li>
        <li class="nav-item active" style="padding-right: 30px">
          <router-link to="/errors" class="nav-link text-white"><h5>Ошибки</h5></router-link>
        </li>
      </ul>
    </div>
  </nav>

  <router-view/>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  //background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSyIREk300U8K__Nw4Z47M7U62udw9AXZe5Sg&usqp=CAU");
  /* Full height */
  height: 100%;

  /* Center and scale the image nicely */
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}


</style>
