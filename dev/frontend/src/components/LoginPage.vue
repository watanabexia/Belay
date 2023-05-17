<template>
    <div class="login-page">
        <h1>Login</h1>
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
          <button type="button" class="btn btn-primary btn-block mb-4 me-2" @click="login">Login</button>
          <button type="button" class="btn btn-success btn-block mb-4" @click="signup">Sign up</button>
        </form>
    </div>
</template>

<script>
  export default {
    methods: {
      login() {
        // get the username and password
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        // call the login API
        const path = 'auth/login';
        this.$axios.post(path, {
          username,
          password,
        })
          .then((res) => {
            this.$router.push('/');
          })
          .catch((error) => {
            if (error.response.status === 401) {
              document.getElementById('passwordError').innerHTML = 'Invalid username or password';
            } else {
              console.error(error);
            }
          });
      },
      signup() {
        this.$router.push('/signup');
      }
    },
    created() {
      if (this.$isApiKeyExistsInCookie()) {
        this.$router.push('/');
      }
    },
  };
</script>