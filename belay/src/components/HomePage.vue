<template>
    <div class="home-page">
      <h1>Belay</h1>
      <p>This is the content of the home page.</p>
      <button class="btn btn-primary"> Login </button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomePage',
    methods: {
      login() {
        this.$router.push('/login');
      },
    },
    created() {
      console.log('Home page created');
    },
  };
  </script>