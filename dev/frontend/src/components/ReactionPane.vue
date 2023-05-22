<template>
    <div class="col-auto">
        <Popper placement="right">
        <button class="btn btn-secondary"><i class="bi bi-plus-circle-fill"></i></button>
        <template #content>
            <EmojiPicker :show_arrow="false" @emoji_click="(emoji) => handleEmojiClick(emoji)" />
        </template>
        </Popper>
    </div>
    <div class="col-auto" v-for=" emoji in Object.keys(reactionCount)">
        <Popper placement="right">
            <button class="btn" :class="{ 'btn-secondary': !isCurrentUser[emoji], 'btn-primary': isCurrentUser[emoji] }" :title="this.reactionUsers[emoji].join(', ')" @click="handleEmojiClick(emoji)">
            {{ reactionCount[emoji] }} {{ emoji }}
            </button>
        <template #content>
            <p> {{  }} </p>
        </template>
        </Popper>
    </div>
</template>
  
<script>
import Popper from "vue3-popper";
import EmojiPicker from "./EmojiPicker - Vue.js/EmojiPicker.vue";
export default {
    data() {
        return {
            reactions: [],
            reactionCount: {},
            reactionUsers: {},
            isCurrentUser: {},
            interval: null,
        };
    },
    props: {
        message: {
            type: Object,
            required: true,
        },
    },
    components: {
        Popper,
        EmojiPicker
    },
    methods: {
        handleEmojiClick(emoji) {
        let path = 'messages/' + this.message.id + '/reactions/create';
        this.$axios.post(path, {
            emoji,
        })
            .then((res) => {
            })
            .catch((error) => {
                console.error(error);
            });
        },
        getReactions() {
            let path = 'users/me';
            this.$axios.get(path)
                .then((res) => {
                    this.username = res.data.username;

                    let path = 'messages/' + this.message.id + '/reactions';
                    this.$axios.get(path)
                        .then((res) => {
                            if (this.reactions.length != res.data.length) {
                                this.reactions = res.data;
                            }
                            let reactionCount_raw = {};
                            let reactionUsers_raw = {};
                            for (let i = 0; i < this.reactions.length; i++) {
                                let reaction = this.reactions[i];
                                if (reaction.emoji in reactionCount_raw) {
                                    reactionCount_raw[reaction.emoji] += 1;
                                    reactionUsers_raw[reaction.emoji].push(reaction.username);
                                } else {
                                    reactionCount_raw[reaction.emoji] = 1;
                                    reactionUsers_raw[reaction.emoji] = [reaction.username];
                                }
                            }

                            if (Object.keys(this.reactionCount).length != Object.keys(reactionCount_raw).length) {
                                this.reactionCount = reactionCount_raw;
                                this.reactionUsers = reactionUsers_raw;
                                this.isCurrentUser = {};
                            }

                            for (let emoji in this.reactionCount) {
                                if (reactionCount_raw[emoji] != this.reactionCount[emoji]) {
                                    this.reactionCount[emoji] = reactionCount_raw[emoji];
                                    this.reactionUsers[emoji] = reactionUsers_raw[emoji];
                                }
                                this.isCurrentUser[emoji] = this.reactionUsers[emoji].includes(this.username);
                            }
                        })
                        .catch((error) => {
                            console.error(error);
                        });
                })
                .catch((error) => {
                    console.error(error);
                });
        },
    },
    mounted() {
        this.getReactions();
        this.interval = setInterval(() => {
            this.getReactions();
        }, 200);
    },
    unmounted() {
        clearInterval(this.interval);
    },
};
</script>