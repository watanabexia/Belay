<template>
    <div class="col-lg">
        <div class="input-group p-5">
          <input type="text" class="form-control" id="message" placeholder="Message" aria-label="Message" aria-describedby="basic-addon1">
          <button type="button" class="btn btn-primary" @click="sendMessage">Send</button>
        </div>
        <div class="p-3">
          <button type="button" class="btn btn-danger" @click="deleteChannel">Delete Channel</button>
        </div>
        <div class="row p-3 messages-column">
          <template v-for="message in messages" >
            <MessageBox v-if="message.reply_to==null" :message="message" />
            <div class="mb-3">
                <button type="button" class="btn btn-secondary" @click="showThread">Reply</button>
            </div>
          </template>
        </div>
    </div>
    <div class="col-lg-3" :class="{'d-none':!IsShowThread}">
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
          IsShowThread: false,
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
        deleteChannel() {
            const path = 'channels/' + this.$route.params.channelId + '/delete';
            this.$axios.post(path)
                .then((res) => {
                    this.$router.push('/dashboard');
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        showThread() {
            this.IsShowThread = true;
        },
        hideThread() {
            this.IsShowThread = false;
        },
        updateTitle() {
            let path = 'channels/' + this.$route.params.channelId;
            this.$axios.get(path)
                .then((res) => {
                    this.$emit('update:current_title', res.data.name);
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    components: {
        MessageBox,
    },
    watch: {
        '$route.params.channelId': function() {
            this.updateTitle();
        },
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
    created() {
        if (!this.$isApiKeyExistsInCookie()) {
        } else {
            this.updateTitle();
        }
    },
};
</script>