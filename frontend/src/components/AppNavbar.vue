<template>
  <nav class="navbar">
    <div class="brand">
      <i class="fas fa-chart-line"></i>
      <span>Finance Tracker</span>
    </div>
    <div class="nav-links">
      <button @click="logout" class="logout-btn">
        <i class="fas fa-sign-out-alt"></i>
        Logout
      </button>
    </div>
  </nav>
</template>

<script>
import axios from "axios";

export default {
  name: "AppNavbar",
  methods: {
    async logout() {
      try {
        await axios.post(`${process.env.VUE_APP_URL}/logout`, {}, {
          withCredentials: true
        });
      } catch (error) {
        console.log("Logout error:", error);
      }
      localStorage.removeItem("token");
      window.location.href = "/#/login";
    }
  }
};
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  z-index: 1000;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a237e;
}

.brand i {
  font-size: 1.8rem;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.logout-btn:hover {
  background: #bb2d3b;
}

@media (max-width: 790px) {
  .navbar {
    padding: 1rem;
  }
  
  .brand {
    font-size: 1.2rem;
  }
  
  .brand i {
    font-size: 1.5rem;
  }
}
</style>