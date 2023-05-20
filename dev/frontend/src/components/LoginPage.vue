<template>
<div class="LoginPage p-3 m-5 col-lg">
  <form>
    <div class="form-outline mb-4">
      <input type="username" id="username" class="form-control" required/>
      <label class="form-label" for="username">Username</label>
    </div>
    <div class="form-outline mb-4">
      <input type="password" id="password" class="form-control" required/>
      <label class="form-label" for="password">Password</label>
    </div>
    <button type="button" class="btn btn-primary btn-block mb-4 me-2" @click="login">Login</button>
    <button type="button" class="btn btn-success btn-block mb-4" @click="signup">Sign up</button>
    <div class="form-outline mb-4">
      <small id="passwordError" class="form-text text-danger"></small>
    </div>
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
            document.getElementById('passwordError').innerHTML = '';
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
            console.log(this.$route.query.redirect);
            this.$router.push(this.$route.query.redirect || '/');
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
      } else {
        this.$emit('update:current_title', 'Login');
      }
    },
  };
</script>