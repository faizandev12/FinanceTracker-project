<template>
  <div class="portfolio-box" v-if="portfolio.length > 0">
    <div class="header-bar">
      <h2>Your Finance Entries</h2>
      <button class="add-entry-btn" @click="showAddModal = true">
        <i class="fa-solid fa-plus"></i> Add Entry
      </button>
    </div>

    <!-- Desktop View -->
    <div v-if="!isMobile" class="desktop-view">
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Category</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in portfolio" :key="item.entry_ID">
            <td>{{ item.Title }}</td>
            <td>{{ item.category_name }}</td>
            <td>${{ item.Amount }}</td>
            <td>{{ formatDate(item.date) }}</td>
            <td class="action-buttons">
              <button class="edit-btn" @click="editFinanceEntry(item)">
                <i class="fa-regular fa-pen-to-square"></i>
              </button>
              <button class="delete-btn" @click="deleteFinanceEntry(item.entry_ID)">
                <i class="fa-solid fa-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Mobile View -->
    <div v-if="isMobile" class="mobile-view">
      <div v-for="(item, index) in portfolio" :key="item.entry_ID" class="finance-card">
        <div class="finance-header" @click="toggleExpand(index)">
          <h3>{{ item.Title }}</h3>
          <i :class="expandedIndex === index ? 'fa-solid fa-angle-up' : 'fa-solid fa-angle-down'"></i>
        </div>
        <transition name="expand">
          <div v-if="expandedIndex === index" class="finance-details">
            <p><strong>Category:</strong> {{ item.category_name }}</p>
            <p><strong>Amount:</strong> ${{ item.Amount }}</p>
            <p><strong>Date:</strong> {{ formatDate(item.date) }}</p>
            <div class="button-group">
              <button class="edit-btn" @click="editFinanceEntry(item)">
                <i class="fa-regular fa-pen-to-square"></i>
              </button>
              <button class="delete-btn" @click="deleteFinanceEntry(item.entry_ID)">
                <i class="fa-solid fa-trash"></i>
              </button>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>

  <!-- Add Entry Modal -->
  <div v-if="showAddModal" class="modal-overlay">
    <div class="modal-content">
      <h3>Add New Finance Entry</h3>
      <form @submit.prevent="submitNewEntry">
        <input v-model="newEntry.Title" placeholder="Title" required />
        <input v-model="newEntry.category_name" placeholder="Category" required />
        <input v-model="newEntry.Amount" type="number" step="0.01" placeholder="Amount" required />
        <input v-model="newEntry.date" type="date" required />
        <div class="modal-actions">
          <button type="submit" class="save-btn">Save</button>
          <button type="button" class="cancel-btn" @click="showAddModal = false">Cancel</button>
        </div>
      </form>
    </div>
  </div>

  <EditComponent 
    :show="isModalVisible" 
    :entry="selectedEntry"
    @close="isModalVisible = false"
  />
</template>

<script>
import axios from "axios";
import EditComponent from './EditComponent.vue';

export default {
  components: { EditComponent },
  props: {
    portfolio: Array,
    isMobile: Boolean
  },
  data() {
    return {
      expandedIndex: null,
      isModalVisible: false,
      selectedEntry: null,
      showAddModal: false,
      newEntry: {
        Title: '',
        category_name: '',
        Amount: '',
        date: ''
      }
    };
  },
  methods: {
    toggleExpand(index) {
      this.expandedIndex = this.expandedIndex === index ? null : index;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric"
      }).format(date);
    },
    editFinanceEntry(entry) {
      this.selectedEntry = { ...entry };
      this.isModalVisible = true;
      console.log("portfolot", this.selectedEntry);
    },
    async deleteFinanceEntry(entryId) {
      if (!confirm("Are you sure you want to delete this finance entry?")) return;
      try {
        const token = localStorage.getItem("token");
        await axios.delete(`${process.env.VUE_APP_URL}/api/portfolio/${entryId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        window.location.reload();
      } catch (error) {
        console.error("Error deleting finance entry:", error);
      }
    },
    async submitNewEntry() {
  try {
    const token = localStorage.getItem("token");
    const response = await axios.post(`${process.env.VUE_APP_URL}/api/addentry`, {
      title: this.newEntry.Title,
      category_name: this.newEntry.category_name,
      amount: parseFloat(this.newEntry.Amount), 
      date: this.newEntry.date
    }, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      withCredentials: true
    });

    console.log('Server response:', response.data); // 🆕 Add this line if you want to see what's returned

    this.showAddModal = false;
    this.newEntry = { 
      Title: '',
      category_name: '',
      Amount: '',
      date: ''
    };
    this.$emit('entry-added', {
  Title: this.newEntry.Title,
  category_name: this.newEntry.category_name,
  Amount: parseFloat(this.newEntry.Amount),
  date: this.newEntry.date,
  entry_ID: response.data.entry_id // from your backend response
});
    alert('Entry added successfully!');
  } catch (error) {
    console.error('Error adding entry:', error);
    const errorMessage = error.response?.data?.error || 'Failed to add entry. Please try again.';
    alert(errorMessage);
  }
}


  }
};
</script>

<style scoped>
.portfolio-box {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(8px);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  margin: 2rem auto;
  max-width: 960px;
  width: 95%;
  animation: fadeIn 0.5s ease-in-out;
}

.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.header-bar h2 {
  font-size: 2rem;
  font-weight: 600;
  color: #1e293b;
}

.add-entry-btn {
  background-color: #3b82f6;
  color: white;
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.3s;
}

.add-entry-btn:hover {
  background-color: #2563eb;
}

/* Table */
table {
  width: 100%;
  border-collapse: collapse;
  overflow: hidden;
  border-radius: 12px;
}

th, td {
  padding: 1rem;
  text-align: left;
}

th {
  background-color: #3b82f6;
  color: white;
  font-weight: 600;
  text-transform: uppercase;
}

td {
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

tr:hover td {
  background: #f3f4f6;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

/* Buttons */
button {
  padding: 8px 10px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: 0.2s ease-in-out;
}

.edit-btn {
  background-color: #10b981;
  color: white;
}

.edit-btn:hover {
  background-color: #059669;
}

.delete-btn {
  background-color: #ef4444;
  color: white;
}

.delete-btn:hover {
  background-color: #b91c1c;
}

/* Mobile Cards */
.mobile-view {
  display: none;
}

.finance-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  margin: 1rem 0;
  overflow: hidden;
  transition: 0.3s;
}

.finance-header {
  background: #3b82f6;
  color: white;
  padding: 1rem;
  font-weight: 600;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.finance-details {
  padding: 1rem;
  background: #f8fafc;
}

.button-group {
  margin-top: 1rem;
  display: flex;
  gap: 10px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 20px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.3s ease;
}

.modal-content h3 {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  text-align: center;
}

.modal-content input {
  width: 100%;
  margin-bottom: 1rem;
  padding: 0.75rem 1rem; /* Added right padding */
  border-radius: 8px;
  border: 1px solid #d1d5db;
  font-size: 1rem;
  box-sizing: border-box; /* Ensures padding doesn't mess up width */
}

.modal-actions {
  display: flex;
  justify-content: space-between;
}

.save-btn {
  background-color: #10b981;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
}

.cancel-btn {
  background-color: #ef4444;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
}

/* Responsive */
@media (max-width: 768px) {
  .desktop-view {
    display: none;
  }

  .mobile-view {
    display: block;
  }

  .header-bar {
    flex-direction: column;
    gap: 1rem;
  }

  .add-entry-btn {
    width: 100%;
    justify-content: center;
  }
}

/* Animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
