<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <h1>Log in</h1>
      <div class="form-group">
        <label for="username"></label>
        <input
          type="text"
          id="username"
          placeholder="Enter username"
          v-model="username"
        />
        <p v-if="usernameError" class="error-message">{{ usernameError }}</p>
      </div>
      <div class="form-group">
        <label for="password"></label>
        <input
          type="password"
          id="password"
          placeholder="Enter password"
          v-model="password"
        />
        <p v-if="passwordError" class="error-message">{{ passwordError }}</p>
      </div>
      <button type="submit" class="submit-btn">Log in</button>
    </form>
  </div>
</template>
<script>
import axios from "axios";
import { useToast } from "vue-toastification";
export default {
  data() {
    return {
      username: "",
      password: "",
      usernameError: "",
      passwordError: "",
      toast: null,
    };
  },
  created() {
    this.toast = useToast();
  },
  methods: {
    handleLogin() {
      this.usernameError = "";
      this.passwordError = "";

      if (!this.username.trim()) {
        this.usernameError = "Username is required";
      }
      if (!this.password.trim()) {
        this.passwordError = "Password is required";
      }

      if (this.usernameError || this.passwordError) {
        return;
      }

      const userData = {
        username: this.username,
        password: this.password,
      };
      axios
        .post("http://localhost:5000/login", userData)
        .then((response) => {
          console.log(response.data);
          localStorage.setItem("token", response.data.access_token);
          console.log("Token", response.data.access_token);
          this.toast.success(response.data.message, {
            timeout: 1500,
            pauseOnHover: false,
          });
          this.$router.push("/");
        })
        .catch((error) => {
          if (error.response) {
            this.toast.error(error.response.data.message, {
              timeout: 1500,
            });
          } else {
            alert("Something went wrong");
          }
        });
    },
  },
};
</script>
<style scoped>
* {
  box-sizing: border-box;
}
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #121212;
}
.login-form {
  background-color: #1e1e1e;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.05);
  width: 100%;
  max-width: 500px;
}
h1 {
  font-size: 30px;
  margin-bottom: 20px;
  color: #ffffff;
  text-align: center;
  font-weight: bold;
}
.form-group {
  margin-top: 15px;
}
.form-group input {
  width: 100%;
  padding: 10px;
  background-color: #121212;
  color: #ffffff;
  border: 1px solid #333;
  border-radius: 8px;
  transition: border-color 0.3s ease, background-color 0.3s ease;
}
.form-group input:focus {
  border-color: #050571;
  background-color: #1e1e1e;
  outline: none;
}
.submit-btn {
  width: 100%;
  margin-top: 15px;
  padding: 12px;
  background-color: #050571;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.submit-btn:hover {
  background-color: #020244;
}
.error-message {
  color: #930b0b;
  font-size: 14px;
  margin-top: 5px;
  text-align: center;
  font-weight: bold;
}
</style>
