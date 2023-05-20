<template>
    <div class="col-lg">
        <div class="input-group pt-5 pe-5">
          <input type="text" class="form-control" id="message" placeholder="Message">
          <button type="button" class="btn btn-primary" @click="sendMessage">Send</button>
        </div>
        <div class="pt-3">
          <button type="button" class="btn btn-danger" @click="deleteChannel">Delete Channel</button>
        </div>
        <div class="row pt-3 messages-column">
          <template v-for="message in messages" >
            <template v-if="message.reply_to==null" >
                <MessageBox :message="message" />
                <div class="mb-3">
                    <button v-if="message.reply_count == 0" type="button" class="btn btn-secondary" @click="showThread(message)">Reply</button>
                    <button v-else type="button" class="btn btn-secondary" @click="showThread(message)">{{message.reply_count}} replies</button>
                </div>
            </template>
          </template>
        </div>
    </div>
    <div class="col-lg-3" :class="{'d-none':!IsShowThread}">
    <div class="pt-5 pb-3">
        <button type="button" class="btn btn-secondary" @click="hideThread">Close Thread</button>
    </div>
      <MessageBox v-if="threadMessage != null" :message="threadMessage" />
        <div class="input-group pe-3">
            <input type="text" class="form-control" id="reply" placeholder="Reply">
            <button type="button" class="btn btn-primary" @click="sendReply">Send</button>
        </div>
      <div class="row pt-3 thread-column">
        <template v-for="replyMessage in replyMessages" >
            <MessageBox :message="replyMessage" />
        </template>
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
          replyMessages: [],
          messageInterval: null,
          threadMessage: null,
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
        showThread(message) {
            this.threadMessage = message;
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
        sendReply() {
            const path = '/messages/' + this.threadMessage.id + '/reply';
            const message = document.getElementById('reply').value;
            this.$axios.post(path, {
                message,
            })
                .then((res) => {
                    document.getElementById('reply').value = '';
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        getReplies() {
            if (this.threadMessage == null) {
                return;
            }
            const path = '/messages/' + this.threadMessage.id + '/replies';
            this.$axios.get(path)
                .then((res) => {
                    this.replyMessages = res.data;
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
                this.getReplies();
            }, 200);
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