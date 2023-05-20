<template>
    <div class="p-3 m-5 col-lg">
        <form>
          <div class="form-outline mb-4">
            <input type="username" id="username" class="form-control" required/>
            <label class="form-label" for="username">Username</label>
          </div>
          <div class="form-outline mb-4">
            <input type="password" id="password" class="form-control" required/>
            <label class="form-label" for="password">Password</label>
          </div>
          <div class="form-outline mb-4">
            <small id="passwordError" class="form-text text-danger"></small>
          </div>
          <button type="button" class="btn btn-success btn-block mb-4" @click="signup">Sign up</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    signup() {
      // get the username and password
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      // call the login API
      const path = 'auth/signup';
      this.$axios.post(path, {
        username,
        password,
      })
        .then((res) => {
          document.getElementById('username').value = '';
          document.getElementById('password').value = '';
          this.$router.push('/');
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    if (this.$isApiKeyExistsInCookie()) {
      this.$router.push('/');
    } else {
      this.$emit('update:current_title', 'Registration');
    }
  },
};
</script>