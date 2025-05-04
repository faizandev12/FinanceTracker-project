<template>
    <v-app-bar app color="primary" dark>
      <v-container class="d-flex justify-space-between align-center">
        <!-- App Name -->
        <span class="text-h6 font-weight-bold">Finance Tracker</span>
  
        <!-- Authentication Buttons -->
        <div class="d-flex gap-3">
          <v-btn text @click="$router.push('/login')">Login</v-btn>
          <v-btn outlined color="white" @click="$router.push('/signup')">Register</v-btn>
        </div>
      </v-container>
    </v-app-bar>
  </template>
  
  <script>
  export default {
    name: "NavBar",
  };
  </script>
  
  <style scoped>
  /* Navbar Styling */
  .v-app-bar {
    background-color: #3b82f6 !important; /* Matches homepage primary color */
    padding: 10px 20px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .v-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  /* Navbar title */
  .text-h6 {
    font-weight: bold;
    color: white;
    font-size: 20px;
  }
  
  /* Navbar buttons */
  .v-btn {
    font-weight: 600;
    text-transform: none;
  }
  
  .v-btn--text {
    color: white !important;
  }
  
  .v-btn--outlined {
    border: 2px solid white !important;
    color: white !important;
  }
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .v-container {
      flex-direction: row;
      justify-content: space-between;
    }
  
    .text-h6 {
      font-size: 18px;
    }
  
    .v-btn {
      font-size: 14px;
      padding: 6px 12px;
    }
  }
  </style>
  