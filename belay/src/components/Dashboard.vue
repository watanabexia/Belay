<template>
  <div class="home-page">
    <h1>Belay Dashboard</h1>
    <p>Welcome back,</p>
  </div>
  <div class="btn-group login">
    <button class="btn btn-danger" @click="logout">Logout</button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Dashboard",
  methods: {
    logout() {
      const path = "auth/logout";
      this.$axios.post(path)
        .then(() => {
          this.$router.push("/");
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    if (!this.$isApiKeyExistsInCookie()) {
      this.$router.push("/login");
    }
  },
};
</script>
