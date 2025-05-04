<template>
  <NavBar />
  <v-container>
    <!-- Header -->
    <v-container class="text-center mt-5">
      <h1>Finance Tracker</h1>
      <p class="subtitle">Manage your expenses and stay on top of your budget</p>
    </v-container>

    <!-- Overview Cards -->
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card outlined class="pa-5 text-center">
            <h3>Monthly Budget</h3>
            <p>${{ budget }}</p>
          </v-card>
        </v-col>
        <v-col cols="12">
          <v-card outlined class="pa-5 text-center">
            <h3>Total Expenses</h3>
            <p>${{ totalExpenses }}</p>
          </v-card>
        </v-col>
        <v-col cols="12">
          <v-card outlined class="pa-5 text-center">
            <h3>Savings Goal</h3>
            <p>${{ savingsGoal }}</p>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script>

import NavBar from "@/components/RegNavbar.vue"; // Import the Navbar component


export default {
  components: {
    NavBar, // Register Navbar component
  },
  data() {
    return {
      budget: 0,
      totalExpenses: 0,
      savingsGoal: 0
    };
  },
  mounted() {
    this.fetchFinancialData();
  },
  methods: {
    async fetchFinancialData() {
      try {
        const response = await fetch(`${process.env.VUE_APP_URL}/api/finance`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) throw new Error('Failed to fetch data');

        const data = await response.json();
        this.budget = data.budget;
        this.totalExpenses = data.totalExpenses;
        this.savingsGoal = data.savingsGoal;
      } catch (error) {
        console.error('Error:', error);
        this.budget = 2000;
        this.totalExpenses = 1200;
        this.savingsGoal = 500;
      }
    }
  }
};
</script>

<style scoped>
.subtitle {
  color: #555;
  font-size: 1.1rem;
}
</style>
