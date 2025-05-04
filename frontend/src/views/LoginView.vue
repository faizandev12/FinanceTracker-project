<template>
  <!-- Navbar -->
  <NavBar />

  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="email">Email:</label>
        <input
          type="email"
          id="email"
          v-model="email"
          placeholder="Enter your email"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="Enter your password"
          required
        />
      </div>
      <button type="submit">Login</button>
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      <div class="create-account">
        <h6>
          Don't have an account? Click <router-link to="/signup">here</router-link> to create an account.
        </h6>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import NavBar from "@/components/RegNavbar.vue"; // Import the Navbar component

export default {
  name: "LoginPage",
  components: {
    NavBar, // Register Navbar component
  },
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
  async handleLogin() {
    //make sure taht email and password aren't null
    if (this.email && this.password) {
      try {
        // send email and password to the API to authenticate
        const response = await axios.post(`${process.env.VUE_APP_URL}/api/login`, {
          email: this.email,
          password: this.password,
        });
        
        //get token and store it for local session
        const token = response.data.token;
        localStorage.setItem("token", token);
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

        //go to the dashboard route
        this.$router.push("/dashboard");

      } catch (error) {
        if (error.response) {
          this.errorMessage = error.response.data.message || "Login failed.";
        } else {
          this.errorMessage = "An error occurred. Please try again later.";
        }
      }
    } else {
      this.errorMessage = "Please fill in all fields.";
    }
  },
},

};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
}

.create-account {
  text-align: center;
  margin-top: 20px;
}

.create-account h6 {
  font-size: 14px;
  color: #555;
}

.create-account a {
  color: #007bff;
  text-decoration: none;
}

.create-account a:hover {
  text-decoration: underline;
}
</style>
