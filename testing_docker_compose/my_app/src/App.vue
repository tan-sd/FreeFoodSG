<template>
  <div class="box">
    <div class="child-top">
      <NavBar/>
    </div>

    <div class="child-bottom">
      <router-view></router-view>
    </div>
  </div>

</template>

<script>
import NavBar from "./components/NavBar.vue";

export default {
  name: "App",
  components: {
    NavBar,
  },
};
</script>


<style>
.box{
  display: flex;
  flex-flow: column;
  height: 100vh;
}

.child-top{
  flex: 0 1 auto;
}

.child-bottom{
  flex: 1 1 auto;
}
</style>