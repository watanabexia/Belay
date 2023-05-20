<template>
    <div class="col">
        <Popper placement="top">
        <button class="btn btn-secondary">➕</button>
        <template #content>
            <EmojiPicker :show_arrow="false" @emoji_click="handleEmojiClick" />
        </template>
        </Popper>
    </div>
</template>
  
<script>
import { defineComponent } from "vue";
import Popper from "vue3-popper";
import EmojiPicker from "./EmojiPicker - Vue.js/EmojiPicker.vue";
export default {
    components: {
        Popper,
        EmojiPicker
    },
};
</script>