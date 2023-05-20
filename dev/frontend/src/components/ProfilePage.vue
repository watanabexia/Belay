<template>
  <div class="p-3 m-5 col-lg">
    <form>
    <div class="form-outline mb-4">
      <input type="username" id="username" class="form-control" :value="username"/>
      <label class="form-label" for="username">Username</label>
    </div>
    <button type="button" class="btn btn-primary btn-block mb-4 me-2" @click="updateUsername">Update Username</button>
    <div class="form-outline mb-4">
      <small id="usernameUpdateSuccess" class="form-text text-primary"></small>
    </div>
    </form>
    <form>
      <div class="form-outline mb-4">
        <input type="password" id="password" class="form-control"/>
        <label class="form-label" for="password">Password</label>
      </div>
      <button type="button" class="btn btn-danger btn-block mb-4" @click="updatePassword">Update Password</button>
      <div class="form-outline mb-4">
        <small id="passwordUpdateSuccess" class="form-text text-danger"></small>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "Profile",
  data() {
    return {
      username: "test",
    };
  },
  methods: {
    updateUsername() {
      const username = document.getElementById('username').value;
      const path = 'users/username/update';
      this.$axios.put(path, {
        username,
      })
        .then((res) => {
          document.getElementById('usernameUpdateSuccess').innerHTML = 'Username updated successfully';
        })
        .catch((error) => {
          console.error(error);
        });
    },
    updatePassword() {
      const password = document.getElementById('password').value;
      const path = 'users/password/update';
      this.$axios.put(path, {
        password,
      })
        .then((res) => {
          document.getElementById('passwordUpdateSuccess').innerHTML = 'Password updated successfully';
        })
        .catch((error) => {
          console.error(error);
        });
    }
  },
  created() {
    if (!this.$isApiKeyExistsInCookie()) {
      this.$router.push({path: "/login", query: { redirect: this.$route.path }});
    } else {
      this.$emit('update:current_title', 'Profile');

      this.$getUsername()
      .then((username) => {
        this.username = username;
      })
    }
  },
};
</script>
