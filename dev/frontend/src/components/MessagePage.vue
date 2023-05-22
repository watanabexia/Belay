<template>
    <div class="col-lg" :class="{'d-none':IsShowThread&&!isWideScreen}">
        <div class="input-group pt-5 pe-5">
          <input type="text" class="form-control" id="message" placeholder="Message">
          <button type="button" class="btn btn-primary" @click="sendMessage">Send</button>
        </div>
        <div class="row pt-3 messages-column overflow-auto">
          <template v-for="message in messages" >
            <template v-if="message.reply_to==null" >
                <MessageBox :message="message" />
                <div class="row mb-3">
                    <div class="col-2">
                        <button v-if="message.reply_count == 0" type="button" class="btn btn-secondary" @click="() => {goToThread(message.id); showThread(message)}">Reply</button>
                    <button v-else type="button" class="btn btn-secondary" @click="() => {goToThread(message.id); showThread(message)}">{{message.reply_count}} replies</button>
                    </div>
                    <ReactionPane :message="message" />
                </div>
            </template>
          </template>
        </div>
        <div class="row pt-3">
            <div class="col"></div>
            <div class="col-3"> <button type="button" class="btn btn-danger" @click="deleteChannel">Delete Channel</button> </div>
        </div>
    </div>
    <div class="col-lg-3" :class="{'d-none':!IsShowThread}">
    <div class="pt-5 pb-3">
        <button type="button" class="btn btn-secondary" @click="hideThread">Close Thread</button>
    </div>
        <div class="replyto-column pb-3">
            <MessageBox v-if="threadMessage != null" :message="threadMessage" style="overflow-y: auto; max-height: 200px;"/>
        </div>
        <div class="input-group pe-3">
            <input type="text" class="form-control" id="reply" placeholder="Reply">
            <button type="button" class="btn btn-primary" @click="sendReply">Send</button>
        </div>
      <div class="row pt-3 thread-column overflow-auto">
        <template v-for="replyMessage in replyMessages" >
            <MessageBox :message="replyMessage" />
            <div class="row mb-3">
                <ReactionPane :message="replyMessage" />
            </div>
        </template>
      </div>
    </div>
</template>

<script>
import MessageBox from "./MessageBox.vue";
import ReactionPane from "./ReactionPane.vue";
export default {
    name: "MessagePage",
    data() {
        return {
          messages: [],
          replyMessages: [],
          messageInterval: null,
          threadMessage: null,
          IsShowThread: false,
          isWideScreen: window.innerWidth > 992,
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
        goToThread(message_id) {
            this.$router.push('/channel/' + this.$route.params.channelId + '/thread/' + message_id);
        },
        showThread(message) {
            this.threadMessage = message;
            this.IsShowThread = true;
        },
        hideThread() {
            this.IsShowThread = false;
            this.$router.push('/channel/' + this.$route.params.channelId);
        },
        updateTitle() {
            let path = 'channels/' + this.$route.params.channelId;
            this.$axios.get(path)
                .then((res) => {
                    this.$emit('update:current_title', res.data.name);
                })
                .catch((error) => {
                    if (error.response.status == 404) {
                        this.$router.push('/dashboard');
                    }
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
        handleResize() {
            this.isWideScreen = window.innerWidth > 992;
        },
    },
    components: {
    MessageBox,
    ReactionPane
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
            window.addEventListener('resize', this.handleResize);

            if (this.$route.params.messageId != null) {
                let path = '/messages/' + this.$route.params.messageId;
                this.$axios.get(path)
                    .then((res) => {
                        if (res.data.reply_to != null) {
                            this.$router.push('/channel/' + this.$route.params.channelId);
                        } else {
                            this.showThread(res.data);
                        }
                    })
                    .catch((error) => {
                        console.error(error);
                    });
            }
        }
    },
};
</script>