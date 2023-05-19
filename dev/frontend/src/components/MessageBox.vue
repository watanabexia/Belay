<template>
    <div class="row">
        <h4> {{ message.username }}</h4>
        <p> {{ message.message }}</p>
    </div>
</template>

<script>
export default {
    name: "MessageBox",
    props: {
        message: {
            type: Object,
            required: true,
        },
    },
    methods: {
        showThread() {
            this.$emit('showThread');
        },
    },
};
</script>