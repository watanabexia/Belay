<template>
  <!-- Wide Screen Layout -->
  <div class="col-lg-3 p-5">
    <p>Welcome back!</p>
    <div class="btn-group login">
      <button class="btn btn-primary" @click="profile">profile</button>
      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
import ChannelBanner from "./ChannelBanner.vue";
export default {
  name: "Dashboard",
  data() {
    return {
      channels: [],
      interval: null,
      channel_ids: [],
    }
  },
  methods: {
    profile() {
      this.$emit('toggleChannelList');
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
  components: {
    ChannelBanner,
  },
  mounted() {
    if (!this.$isApiKeyExistsInCookie()) {
    } else {
      this.$emit('update:current_title', 'Dashboard');
    }
  },
  unmounted() {
    clearInterval(this.interval);
  },
  created() {
    if (!this.$isApiKeyExistsInCookie()) {
      this.$router.push("/login");
    }
  },
};
</script>
