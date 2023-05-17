<template>
<div class="banner">
    <h1 class="display-1">Belay</h1>
    <h1>{{ title }}</h1>
</div>
</template>

<script>
export default {
    name: "Banner",
    props: {
        title: {
            type: String,
            default: "Belay",
        },
    },
    methods: {
    },
};
</script>