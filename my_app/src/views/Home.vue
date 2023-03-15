<template>
  <div class="container-fluid p-0 fill-space position-relative">
    <Map/>

    <FoodList/>
  </div>
  </template>
  
  <script>
  import Map from "../components/Map.vue";
  import FoodList from "../components/FoodList.vue";
  
  export default {
    name: "App",
    components: {
      Map,
      FoodList
    },
  };
  </script>


<style scoped>
  .fill-space{
    height: 100%;
  }
</style>