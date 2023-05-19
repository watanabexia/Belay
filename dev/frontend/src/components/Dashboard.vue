<template>
  <!-- Wide Screen Layout -->
  <div class="p-3">
    <p>Welcome back!</p>
    <div class="btn-group login">
      <button class="btn btn-primary" @click="profile">profile</button>
      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>
  </div>
  <div class="p-3">
    <button class="btn btn-success" @click="createChannel">Create Channel</button>
  </div>
  <!-- Channel List -->
  <div class="p-3 channel-list">
    <ChannelBanner @click="$event => navigateToChannel(channel)" v-for="channel in channels" :ChannelName="channel.name" :isSelect="channel.id == $route.params.channelId" />
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
    }
  },
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
    createChannel() {
      const path = "channels/create";
      this.$axios.post(path)
        .then((res) => {
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getChannels() {
      const path = "channels/all";
      this.$axios.get(path)
        .then((res) => {
          this.channels = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    navigateToChannel(channel) {
      this.$emit('update:current_title', channel.name);
      this.$emit('toggleChannelList');
      this.$router.push(`/channel/${channel.id}`);
    },
  },
  components: {
    ChannelBanner,
  },
  mounted() {
    if (!this.$isApiKeyExistsInCookie()) {
    } else {
      this.$emit('update:current_title', 'Dashboard');
      this.interval = setInterval(() => {
        this.getChannels();
      }, 500);
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
