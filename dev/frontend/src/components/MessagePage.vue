<template>
    <div class="col-lg">
        <div class="input-group p-5">
          <input type="text" class="form-control" id="message" placeholder="Message" aria-label="Message" aria-describedby="basic-addon1">
          <button type="button" class="btn btn-primary" @click="sendMessage">Send</button>
        </div>
        <div class="row p-3 messages-column">
          <template v-for="message in messages" >
            <MessageBox v-if="message.reply_to==null" :message="message" @showThread="showThread" />
          </template>
        </div>
    </div>
    <div class="col-lg-3" :class="{'d-none':!showThread}">
      <div class="p-3 thread-column">
        <!-- Thread Column content goes here -->
      </div>
    </div>
</template>

<script>
import MessageBox from "./MessageBox.vue";
export default {
    name: "MessagePage",
    data() {
        return {
          messages: [],
          messageInterval: null,
          showThread: false,
        };
    },
    methods: {
        getMessages() {
            const path = 'channels/' + this.$route.params.channelId + '/messages';
            this.$axios.get(path)
                .then((res) => {
                    this.messages = res.data;
                    if (this.messages.length > 0) {
                        let message_id = this.messages[0].id;
                        let path = 'channels/' + this.$route.params.channelId + '/last';
                        this.$axios.post(path, {
                            message_id,
                        })
                        .then((res) => {
                        })
                        .catch((error) => {
                            console.error(error);
                        });
                    }
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        sendMessage() {
            const path = 'channels/' + this.$route.params.channelId + '/messages/create';
            const message = document.getElementById('message').value;
            this.$axios.post(path, {
                message,
            })
                .then((res) => {
                    document.getElementById('message').value = '';
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        showThread() {
            this.showThread = true;
        },
        hideThread() {
            this.showThread = false;
        },
    },
    components: {
        MessageBox,
    },
    mounted() {
        if (!this.$isApiKeyExistsInCookie()) {
        } else {
            this.messageInterval = setInterval(() => {
                this.getMessages();
            }, 500);
        }
    },
    unmounted() {
        clearInterval(this.messageInterval);
    },
};
</script>