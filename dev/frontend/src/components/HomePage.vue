<template>
  <div class="home-page">
    <h1>Belay</h1>
    <p>Welcome to Belay! Your next Slack is not slack, but belay ;)</p>
    <div class="btn-group login">
      <button class="btn btn-primary" @click="login">Login</button>
      <button class="btn btn-success" @click="signup">Sign Up</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  methods: {
    login() {
      this.$router.push("/login");
    },
    signup() {
      this.$router.push("/signup");
    },
  },
  created() {
    if (this.$isApiKeyExistsInCookie()) {
      this.$router.push("/dashboard");
    }
  },
};
</script>
