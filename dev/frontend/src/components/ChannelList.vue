<template>
  <div class="input-group pt-5 pe-5">
    <input type="text" class="form-control" id="NewChannelName" placeholder="Channel Name">
    <button class="btn btn-success" @click="createChannel">Create Channel</button>
  </div>
  <!-- Channel List -->
  <div class="pt-3 channel-list">
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
          for (let i = 0; i < this.channels.length; i++) {
            let channel = this.channels[i];
            channel.name = res.data[i].name
            let path = "channels/" + channel.id + "/unread";
              this.$axios.get(path)
              .then ((res) => {
                channel['unreadCount'] = res.data['unread_count']
              })
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    navigateToChannel(channel) {
      this.$emit('toggleChannelList');
      this.$emit('update:current_title', channel.name);
      this.$router.push(`/channel/${channel.id}`);
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
      this.$router.push("/login");
    }
  },
};
</script>
