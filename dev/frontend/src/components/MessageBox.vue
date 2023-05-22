<template>
    <div class="row message-box">
        <h4> {{ message.username }}</h4>
        <p> {{ parsedMessage }}</p>
        <div v-if="imageUrls.length > 0">
            <div class="pb-3" v-for="imageUrl in imageUrls">
                <img class="chatImage" :src="imageUrl" alt="image">
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "MessageBox",
    data() {
        return {
            imageUrls: [],
        };
    },
    props: {
        message: {
            type: Object,
            required: true,
        },
    },
    computed: {
        parsedMessage() {
            const imageUrls = this.extractImageUrls(this.message.message);
            this.imageUrls = imageUrls;
            let parsedMessage = this.message.message;
            for (let i = 0; i < imageUrls.length; i++) {
                parsedMessage = parsedMessage.replace(
                    imageUrls[i],
                    ""
                );
            }
            return parsedMessage
        },
    },
    methods: {
        showThread() {
            this.$emit('showThread');
        },
        extractImageUrls(message) {
            const urlRegex = /(https?:\/\/[^\s]+(?=\.(jpg|jpeg|png|gif))\.\S+)/gi;
            return message.match(urlRegex) || [];
        },
    },
};
</script>