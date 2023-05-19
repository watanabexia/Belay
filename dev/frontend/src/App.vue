<template>
  <!-- Wide Screen Layout -->
  <div class="container-fluid d-none d-lg-block" v-if="isWideScreen">
    <div class="row">
      <div class="col-lg-3">
        <Banner @click="home"/>
        <h2 class="p-3">{{ current_title }}</h2>
        <RouterView name="LeftSidebar" @update:current_title="(new_title) => current_title = new_title " />
      </div>
      <RouterView name="MainContent" @update:current_title="(new_title) => current_title = new_title " />
    </div>
  </div>

  <!-- Narrow Screen Layout -->
  <div class="container-fluid d-lg-none" v-else>
    <div class="row">
      <div class="col">
        <Banner @click="home"/>
        <h2 class="p-3">{{ current_title }}</h2>
        <div class="p-3 menu-bar">
          <button class="btn btn-primary" @click="toggleChannelList" v-if="!showChannelList">Channel List</button>
          <button class="btn btn-primary" @click="toggleChannelList" v-else>Close Channel List</button>
        </div>
        <RouterView name="LeftSidebar" v-if="showChannelList" @update:current_title="(new_title) => current_title = new_title " @toggleChannelList="toggleChannelList"/>
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
      isWideScreen: window.innerWidth > 992,
    }
  },
  methods: {
    home() {
      this.$router.push("/");
    },
    toggleChannelList() {
      this.showChannelList = !this.showChannelList;
    },
    handleResize() {
      this.isWideScreen = window.innerWidth > 992;
    }
  },
  created() {
    window.addEventListener('resize', this.handleResize);
  },
}
</script>