<template>
  <div class="register-container">
    <form @submit.prevent="handleRegister" class="register-form">
      <h1>Register</h1>
      <div class="form-group">
        <label for="username"></label>
        <input
          type="text"
          id="username"
          v-model="username"
          placeholder="Enter username"
        />
      </div>
      <div class="form-group">
        <label for="email"></label>
        <input
          type="text"
          id="email"
          v-model="email"
          placeholder="Enter email"
        />
      </div>
      <div class="form-group">
        <label for="password"></label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="Enter password"
        />
      </div>
      <div class="form-group">
        <label for="confirmPassword"></label>
        <input
          type="password"
          id="confirmPassword"
          v-model="confirmPassword"
          placeholder="Confirm password"
        />
      </div>
      <button type="submit" class="submit-btn">Register</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { useToast } from "vue-toastification";

export default {
  name: "RegisterView",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
      toast: null,
    };
  },
  created() {
    this.toast = useToast();
  },
  methods: {
    handleRegister() {
      if (
        !this.username.trim() ||
        !this.email.trim() ||
        !this.password.trim() ||
        !this.confirmPassword.trim()
      ) {
        this.toast.error("All fields are required", {
          timeout: 1500,
        });
        return;
      }
      if (this.username.length < 3 || this.username.length > 20) {
        this.toast.error("Username must be between 3 and 20 characters!", {
          timeout: 1500,
        });
        return;
      }
      if (!/^[a-zA-Z0-9_]+$/.test(this.username)) {
        this.toast.error(
          "Username can only contain letters, numbers, and underscores!",
          {
            timeout: 1500,
          }
        );
        return;
      }
      if (
        !/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(this.email)
      ) {
        this.toast.error("Invalid email format!", {
          timeout: 1500,
        });
        return;
      }
      if (this.password.length < 6) {
        this.toast.error("Password must be at least 6 characters long!", {
          timeout: 1500,
        });
        return;
      }
      if (this.password !== this.confirmPassword) {
        this.toast.error("Password do not match!", {
          timeout: 1500,
        });
        return;
      }

      const userData = {
        username: this.username,
        email: this.email,
        password: this.password,
      };
      axios
        .post("http://localhost:5000/register", userData)
        .then((response) => {
          console.log(response.data);
          this.toast.success(response.data.message, {
            timeout: 1500,
          });
          this.$router.push("/login");
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
  margin: 0;
  padding: 0;
}

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #121212;
}

.register-form {
  background: #1e1e1e;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.05);
  width: 100%;
  max-width: 500px;
}

h1 {
  font-size: 30px;
  margin-bottom: 20px;
  text-align: center;
  font-weight: bold;
  color: #ffffff;
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
  margin-top: 15px;
  width: 100%;
  padding: 12px;
  background-color: #050571;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #020244;
}
</style>
