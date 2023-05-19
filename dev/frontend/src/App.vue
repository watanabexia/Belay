<template>
  <!-- Wide Screen Layout -->
  <div class="container-fluid d-none d-lg-block">
    <div class="row">
      <div class="col-lg-3">
        <Banner :title="current_title" @click="home"/>
        <RouterView name="LeftSidebar" @update:current_title="(new_title) => current_title = new_title " />
      </div>
      <RouterView name="MainContent" />
    </div>
  </div>

  <!-- Narrow Screen Layout -->
  <div class="container-fluid d-lg-none">
    <div class="row">
      <div class="col">
        <Banner :title="current_title" @click="home"/>
        <div class="p-3 menu-bar">
          <button class="btn btn-primary" @click="toggleChannelList" v-if="!showChannelList">Channel List</button>
          <button class="btn btn-primary" @click="toggleChannelList" v-else>Close Channel List</button>
        </div>
        <RouterView name="LeftSidebar" v-if="showChannelList" @update:current_title="(new_title) => current_title = new_title " />
        <RouterView name="MainContent" v-else/>
      </div>
    </div>
  </div>
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
      showChannelList: false,
    }
  },
  methods: {
    home() {
      this.$router.push("/");
    },
    toggleChannelList() {
      this.showChannelList = !this.showChannelList;
    },
  },
}
</script>