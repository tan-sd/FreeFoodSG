<template>
    <div>
      <button class="btn btn-main" @click="showModal = true"><font-awesome-icon icon="fa-solid fa-utensils" /> Create Post</button>
      <div class="modal-box" v-if="showModal">
        <div class="modal-content">
          <span class="close-btn" @click="showModal = false">
            <font-awesome-icon icon="fa-solid fa-xmark" />
            </span>
          <h2>Create Post</h2>
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
                <input type="text" class="form-control" id="floatingPassword" placeholder="Location">
                <label for="floatingInput">Location</label>
            </div>

            <div class="mb-3">
                Allergens
            </div>

            <div class="form-check form-check-inline">
                <input class="form-check-input" type="checkbox" value="" id="reverseCheck1">
                <label class="form-check-label" for="reverseCheck1">
                    Halal
                </label>
            </div>

            <div class="form-check form-check-inline">
                <input class="form-check-input" type="checkbox" value="" id="reverseCheck1">
                <label class="form-check-label" for="reverseCheck1">
                    Vegan
                </label>
            </div>

            <div class="form-check form-check-inline">
                <input class="form-check-input" type="checkbox" value="" id="reverseCheck1">
                <label class="form-check-label" for="reverseCheck1">
                    ??
                </label>
            </div>

            <div class="mb-3">
                <label for="formFile" class="form-label">Image</label>
                <input class="form-control" type="file" id="formFile">
            </div>

            <button type="submit">Submit</button>
          </form>
        </div>
      </div>
    </div>
  </template>

<script>
export default {
  data() {
    return {
      showModal: false,
    };
  },
  methods: {
    onSubmit() {
      // Handle form submission
      this.showModal = false; // Close the modal after form submission
    },
  },
};
</script>

<style scoped>
.modal-box {
  position: fixed;
  z-index: 9999;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: auto;
}

.modal-content {
  position: relative;
  background-color: white;
  padding: 20px;
  width: 60%;
  max-width: 500px;
  border-radius: 5px;
  animation: fadeIn 0.5s ease-in-out;
  transform-origin: center center;
  animation-fill-mode: forwards;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: scale(0.7);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 20px;
  font-size: 1.5rem;
  cursor: pointer;
}
</style>