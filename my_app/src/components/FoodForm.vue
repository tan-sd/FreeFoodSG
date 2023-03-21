<template>
    <button class="btn btn-main" data-bs-toggle="modal" data-bs-target="#new-foodpost"><font-awesome-icon icon="fa-solid fa-utensils" /> Create Post</button>
    
    <div class="modal fade" id="new-foodpost" tabindex="-1" aria-labelledby="modal-title-foodform" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content bg-light text-dark">
          <div class="modal-header bg-dark text-extra-light">
            <h5 class="modal-title" id="modal-title-foodform"><font-awesome-icon icon="fa-solid fa-utensils" /> Create Food Post</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>

          <div class="modal-body justify-content-center">
            <form>
              <div class="form-floating mb-3">
                  <input type="text" class="form-control" id="floatingInput" placeholder="Title">
                  <label for="floatingInput">Title</label>
              </div>
              
              <div class="form-floating mb-3">
                  <textarea class="form-control" id="floatingInput"   placeholder="Description" style="height: 80px; resize: none;"></textarea>
                  <label for="floatingInput">Description</label>
              </div>
  
              <div class="form-floating mb-3">
                  <GMapAutocomplete
                      class="form-control"
                      placeholder=" "
                      @place_changed="setPlace"
                      id="googlemap_autocomplete_foodform"
                      type="text"
                      :options="autoCompleteOptions"
                  >
                  </GMapAutocomplete>
                  <label for="googlemap_autocomplete_foodform"><font-awesome-icon icon="fa-solid fa-location-dot" />&nbsp;Location</label>
              </div>
  
              <!-- Dietary Restrictions START -->
              <div class="d-flex justify-content-center mt-3">
                <div class="form-check mx-2">
                    <input class="form-check-input" type="checkbox" value="halal" id="foodform-halal-checkbox">
                    <label class="form-check-label" for="foodform-halal-checkbox">
                      <font-awesome-icon icon="fa-solid fa-star-and-crescent" />&nbsp;Halal
                    </label>
                </div>
    
                <div class="form-check mx-2">
                    <input class="form-check-input" type="checkbox" value="vegetarian" id="foodform-vege-checkbox">
                    <label class="form-check-label" for="foodform-vege-checkbox">
                      <font-awesome-icon icon="fa-solid fa-leaf" />&nbsp;Vegetarian
                    </label>
                </div>
    
                <div class="form-check mx-2">
                    <input class="form-check-input" type="checkbox" value="" id="foodform-nobeef-checkbox">
                    <label class="form-check-label" for="foodform-nobeef-checkbox">
                      <font-awesome-icon icon="fa-solid fa-cow" />&nbsp;No Beef
                    </label>
                </div>
              </div>  
              <!-- Dietary Restrictions END -->
  
              <div class="input-group custom-file-button my-4">
                  <label class="input-group-text bg-dark text-extra-light" for="foodform-upload-img-btn">
                    <font-awesome-icon icon="fa-solid fa-image" />&nbsp;Upload Image
                  </label>
                  
                  <input class="form-control" type="file" id="foodform-upload-img-btn">
              </div>
  
              <div class="d-flex justify-content-center mt-3">
                  <button class="btn btn-main"><font-awesome-icon icon="fa-solid fa-paper-plane" />&nbsp;&nbsp;Post</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
  export default{
    data() {
      return{
        autoCompleteOptions: {
            componentRestrictions: {
                country: ["sg"],
            }
        },
      }
    }
  }
</script>

<style scoped>
  .custom-file-button input[type="file"]{
      margin-left: -2px !important;
  }

  .custom-file-button input[type="file"]:hover label{
        background-color: #dde0e3;
        cursor: pointer;
  }

  .custom-file-button input[type="file"]::-webkit-file-upload-button {
      display: none;
  }

  .custom-file-button input[type="file"]::file-selector-button {
      display: none;
  }
</style>

<style>
  .pac-container {
        z-index: 10000 !important;
    }
</style>