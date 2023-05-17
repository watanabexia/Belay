<template>
  <div class="home-page">
    <p>Welcome back,</p>
  </div>
  <div class="btn-group login">
    <button class="btn btn-danger" @click="logout">Logout</button>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  methods: {
  },
  created() {
    if (!this.$isApiKeyExistsInCookie()) {
      this.$router.push("/login");
    } else {
      this.$emit('update:current_title', 'Profile');
    }
  },
};
</script>
