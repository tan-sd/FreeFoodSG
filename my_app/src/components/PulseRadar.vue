<template>
    <div class="marker-container">
      <div class="pulse-marker"></div>
      <div class="current-location-marker"></div>
    </div>
  </template>
  
  <script>
  export default {
    name: "CustomMarker",
    props: {
      position: Object,
    },
  };
  </script>
  
  <style scoped>
  .marker-container {
    z-index: 101;
    position: relative;
    width: 40px;
    height: 40px;
  }
  
  .pulse-marker {
    position: absolute;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: rgba(38, 139, 210, 0.3);
    animation: pulse 2s infinite;
  }
  
  .current-location-marker {
    position: absolute;
    top: 10px;
    left: 10px;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: #268bd2;
    border: 2px solid #fff;
  }
  
  @keyframes pulse {
  0% {
    transform: scale(0.1);
    opacity: 0.7;
  }
  70% {
    transform: scale(1);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 0;
  }
}
  </style>