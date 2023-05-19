<template>
    <div class="channel-banner pb-3">
        <button class="btn btn-secondary" v-if="!isSelect">{{ ChannelName }} <span class="unread-count" v-if="unreadCount > 0">{{ unreadCount }}</span> </button>
        <button class="btn btn-primary" v-else>{{ ChannelName }} <span class="unread-count" v-if="unreadCount > 0">{{ unreadCount }}</span> </button>
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
        unreadCount: {
            type: Number,
            default: 0,
        },
    },
};
</script>