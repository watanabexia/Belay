<template>
  <div class="home-page">
    <p>Welcome back,</p>
  </div>
  <div class="btn-group login">
    <button class="btn btn-primary" @click="profile">profile</button>
    <button class="btn btn-danger" @click="logout">Logout</button>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  methods: {
    profile() {
      this.$router.push("/profile");
    },
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
    } else {
      this.$emit('update:current_title', 'Dashboard');
    }
  },
};
</script>
