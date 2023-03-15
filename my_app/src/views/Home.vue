<template>
  <div class="container-fluid p-0 fill-space position-relative flex-wrapper">
    <div class="child-map">
      <Map class="map-main"/>
    </div>

    <FoodList class="child-foodlist"/>
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

  .flex-wrapper{
    display: flex;
    flex-direction: column;
  }

  .child-map{
    flex: 1 1 auto;
    position: relative;
  }

  .child-foodlist{
    flex: 0 1 auto;
  }

  /* .map-main{
    position: absolute;
    height: 105%;
    top: 0;
  } */
</style>