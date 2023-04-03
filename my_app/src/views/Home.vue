<template>
  <div class="container-fluid p-0 fill-space position-relative flex-wrapper">
    <div class="child-map">
      <Map class="map-main"/>
    </div>

    <div class="child-foodlist">
      <FoodList/>
    </div>
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
    created() {
      //IF LOGGED IN

      //IF NOT LOGGED IN
    }
  };

// if is existing users
// food_url is'http://localhost:5100/available_food'
// use axios post food_url
// with params lat: lng:

// if cnot find username in caache -> guest
// guest_URL = 'http://localhost:5100/guest/available_food'
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