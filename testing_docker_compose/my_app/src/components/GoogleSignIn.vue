<script setup>
import { GoogleSignInButton } from 'vue3-google-signin';

// handle success event
const handleLoginSuccess = response => {
  const { credential } = response 
  console.log("Access Token", credential)
};

const handleLoginError = () => {
  console.error("Login failed");
};
</script>

<template>
  <div>
    <GoogleSignInButton
    @success="handleLoginSuccess"
    @error="handleLoginError"
    ></GoogleSignInButton>
  </div>
</template>