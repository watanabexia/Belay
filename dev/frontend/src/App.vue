<template>
  <Banner :title="current_title" @click="home"/>
  <RouterView @update:current_title="(new_title) => current_title = new_title " />
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<script>
import Banner from './components/Banner.vue'

export default {
  data() {
    return {
      current_title: 'Belay',
    }
  },
  methods: {
    home() {
      this.$router.push("/");
    },
  },
}
</script>