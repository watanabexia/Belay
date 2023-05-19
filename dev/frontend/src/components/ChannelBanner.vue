<template>
    <div class="channel-banner pb-3">
        <button class="btn btn-secondary" v-if="!isSelect">{{ ChannelName }}</button>
        <button class="btn btn-primary" v-else>{{ ChannelName }}</button>
    </div>
</template>

<script>
export default {
    name: "ChannelBanner",
    props: {
        ChannelName: {
            type: String,
            required: true,
        },
        isSelect: {
            type: Boolean,
            default: false,
        },
    },
};
</script>