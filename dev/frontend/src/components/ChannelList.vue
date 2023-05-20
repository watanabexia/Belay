<template>
  <div class="input-group pt-5 pe-5">
    <input type="text" class="form-control" id="NewChannelName" placeholder="Channel Name">
    <button class="btn btn-success" @click="createChannel">Create Channel</button>
  </div>
  <!-- Channel List -->
  <div class="pt-3 channel-list overflow-auto">
    <ChannelBanner @click="$event => navigateToChannel(channel)" v-for="channel in channels" :ChannelName="channel.name" :isSelect="channel.id == $route.params.channelId" :unreadCount="channel.unreadCount" />
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
    createChannel() {
      const path = "channels/create";
      this.$axios.post(path, {
        channel_name: document.getElementById('NewChannelName').value,
      })
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
          if (this.channels.length != res.data.length) {
            this.channels = res.data;
          }

          let path = "channels/unread";
          this.$axios.get(path)
          .then ((res) => {
            for (let i = 0; i < this.channels.length; i++) {
              let channel = this.channels[i];
              channel['unreadCount'] = res.data[channel.id]
            }
          })
        })
        .catch((error) => {
          console.error(error);
        });
    },
    navigateToChannel(channel) {
      this.$emit('toggleChannelList');
      this.$emit('update:current_title', channel.name);
      if (this.$route.params.messageId != null) {
        this.$router.push(`/channel/${channel.id}/thread/${this.$route.params.messageId}`);
      } else {
        this.$router.push(`/channel/${channel.id}`);
      }
    },
  },
  components: {
    ChannelBanner,
  },
  mounted() {
    if (!this.$isApiKeyExistsInCookie()) {
    } else {
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
      console.log("redirecting to login");
      this.$router.push({path: "/login", query: { redirect: this.$route.path }});
    }
  },
};
</script>
