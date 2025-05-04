<template>
  <div class="app-container">
    <AppNavbar />

    <div class="dashboard-content">
      <h1 v-if="firstName">Hello, {{ firstName }}! Welcome to your Dashboard</h1>
      <h1 v-else class="error">ERROR: Cannot connect to account</h1>

      <div class="portfolio-wrapper" v-if="portfolio.length">
        <PortfolioBox 
  :portfolio="portfolio" 
  :isMobile="isMobile" 
  @entry-added="handleEntryAdded" 
/>
      </div>
    </div>
  </div>

  <AddStockComponent
    :show="showAddStockModal"
    @close="showAddStockModal = false"
    @stock-added="refreshStocks"
  />
</template>

<script>
import axios from "axios";
import AppNavbar from "@/components/AppNavbar.vue";
import PortfolioBox from "@/components/PortfolioBox.vue";
// import AddStockComponent from "@/components/AddStockComponent.vue";

export default {
  name: "DashboardView",
  components: {
    AppNavbar,
    PortfolioBox,
    // AddStockComponent
  },
  data() {
    return {
      firstName: "",
      portfolio: [],
      isMobile: window.innerWidth <= 790,
      showModal: false,
      industries: [],
      entry: { 
        Title: "",
        Category: null,
        Amount: null,
        Date: "",
      },
      showAddStockModal: false,
      errors: {}
    };
  },
  async created() {
    window.addEventListener("resize", this.updateScreenSize);
    this.updateScreenSize();

    const token = localStorage.getItem("token");
    if (!token) {
      this.$router.push("/login");
      return;
    }

    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

    try {
      const response = await axios.get(`${process.env.VUE_APP_URL}/api/dashboard`, {
        withCredentials: true
      });
      this.firstName = response.data.first_name;
      this.getPortfolio();
    } catch (error) {
      this.$router.push("/login");
    }
  },
  methods: {
    toggleAddStockModal() {
      this.showAddStockModal = !this.showAddStockModal;
    },
    async refreshStocks() {
      await this.fetchStocks(); // Refresh the stock list
    },
    async getPortfolio() {
      try {
        const path = `${process.env.VUE_APP_URL}/api/portfolio`;
        const res = await axios.get(path, { withCredentials: true });
        if (Array.isArray(res.data.entries)) {
          this.portfolio = res.data.entries;
        } else {
          console.error("Expected entries to be an array but got:", res.data.entries);
          this.portfolio = [];
        }
        console.log("Portfolio response:", res.data);
      } catch (err) {
        console.error("Error fetching portfolio:", err);
      }
    },
    updateScreenSize() {
      this.isMobile = window.innerWidth <= 790;
    },
    documentStock() {
      // Add document stock logic
    },
    generateSuggestions() {
      this.$router.push('/suggestions');
    }
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.updateScreenSize);
  }
};
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.dashboard-content {
  max-width: 1200px;
  margin: 80px auto 0;
  padding: 20px;
  text-align: center;
}

h1 {
  color: #2c3e50;
  margin-bottom: 30px;
  text-align: center;
}

.error {
  color: #dc3545;
  text-align: center;
}

/* 🟩 Centered and Responsive Portfolio Box */
.portfolio-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  padding: 0 15px;
}

/* PortfolioBox styles (optional) */
.portfolio-box {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
  text-align: center;
}

/* Table Styling */
table {
  width: 100%;
  border-collapse: separate;
  margin-top: 10px;
  border: 2px solid black;
  border-radius: 10px;
  border-spacing: 0;
}

th:first-child {
  border-top-left-radius: 8px;
}

th:last-child {
  border-top-right-radius: 8px;
}

tbody tr:last-child td:first-child {
  border-bottom-left-radius: 10px;
}

th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background: #007bff;
  color: white;
}

/* 🔵 Mobile Styling */
@media (max-width: 790px) {
  .dashboard-content {
    padding: 15px;
    margin-top: 70px;
  }

  .portfolio-wrapper {
    padding: 0 10px;
  }

  .portfolio-box {
    padding: 15px;
  }
}
</style>
