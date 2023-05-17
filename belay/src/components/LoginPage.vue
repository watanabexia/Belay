<template>
    <div class="login-page">
        <h1>Login</h1>
        <form @submit.prevent="submitForm">
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="email" required>
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" required>
        </div>
        <button type="submit">Login</button>
        </form>
    </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    submitForm() {
      // Perform login logic, e.g., make API call or check credentials
      if (this.email === 'user@example.com' && this.password === 'password') {
        // Login successful
        console.log('Login successful');
        // Redirect to the home page or perform any other action
        this.$router.push('/home');
      } else {
        // Login failed
        console.log('Login failed');
        // Display an error message or perform any other action
      }
    },
  },
};
</script>