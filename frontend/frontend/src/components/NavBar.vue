<template>
  <nav>
    <ul>
      <li><router-link to="/">Home</router-link></li>
      <li><router-link to="/search">SearchPage</router-link></li>
      <li v-if="!isLoggedIn"><router-link to="/login">Login</router-link></li>
      <li v-if="isLoggedIn">
        <button @click="logout" class="logout">Logout</button>
      </li>
    </ul>
  </nav>
</template>
<script>
export default {
  name: "NavBar",
  data() {
    return {
      isLoggedIn: false,
    };
  },
  created() {
    this.checkLoginStatus();
  },
  methods: {
    checkLoginStatus() {
      const token = localStorage.getItem("token");
      this.isLoggedIn = !!token;
    },
    logout() {
      localStorage.removeItem("token");
      this.isLoggedIn = false;
      this.$router.push("/login");
    },
  },
  watch: {
    $route() {
      this.checkLoginStatus();
    },
  },
};
</script>

<style scoped>
nav {
  background-color: #0b175f;
  padding: 20px 40px;
  width: 100%;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
  align-items: center;
}

ul {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
}
.logout {
  padding: 0;
  margin: 0;
}

li {
  margin: 0 15px;
}

a,
button {
  color: white;
  text-decoration: none;
  font-weight: 600;
  background: none;
  border: none;
  cursor: pointer;
  transition: 0.3s ease;
  padding: 4px 4px;
  font-size: 16px;
  line-height: 1.5;
}

a:hover,
button:hover {
  text-decoration: underline;
}
</style>
