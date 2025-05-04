<template>
  <div v-if="show" class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <h2>Edit Finance Entry</h2>

      <div class="input-group">
        <label>Title:</label>
        <input v-model="editedEntry.Title" class="input-field" />
        <p v-if="errors.title" class="error-message">{{ errors.title }}</p>
      </div>

      <div class="input-group">
        <label>Category:</label>
        <select v-model="editedEntry.category_id" class="input-field">
          <option disabled value="">Select a category</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
        <p v-if="errors.category" class="error-message">{{ errors.category }}</p>
      </div>

      <div class="input-group">
        <label>Amount:</label>
        <input v-model.number="editedEntry.Amount" type="number" class="input-field" />
        <p v-if="errors.amount" class="error-message">{{ errors.amount }}</p>
      </div>

      <div class="input-group">
        <label>Date:</label>
        <input v-model="formattedDate" type="date" class="input-field" />
        <p v-if="errors.date" class="error-message">{{ errors.date }}</p>
      </div>

      <div class="button-group">
        <button class="save-btn" @click="updateFinanceEntry">Save</button>
        <button class="cancel-btn" @click="closeModal">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: { show: Boolean, entry: Object },
  data() {
    return {
      editedEntry: this.entry ? { ...this.entry } : {},
      categories: [],
      errors: {},
    };
  },
  computed: {
    formattedDate: {
      get() {
        if (!this.editedEntry.date) return "";
        const date = new Date(this.editedEntry.date);
        return date.toISOString().split("T")[0]; // Format to 'YYYY-MM-DD'
      },
      set(value) {
        this.editedEntry.date = value;
      }
    }
  },
  watch: {
    entry(newVal) {
      if (newVal) {
        // Create a copy to avoid modifying the original
        this.editedEntry = { ...newVal };
        
        // If we have a category_name but no category_id, try to find the ID
        if (this.categories.length > 0 && newVal.category_name && !newVal.category_id) {
          const selectedCategory = this.categories.find(cat => cat.name === newVal.category_name);
          if (selectedCategory) {
            this.editedEntry.category_id = selectedCategory.id;
          }
        }
      }
    }
  },
  async mounted() {
    await this.fetchCategories();
    
    // If we already have an entry, match with category
    if (this.entry && this.entry.category_name && this.categories.length > 0) {
      const selectedCategory = this.categories.find(cat => cat.name === this.entry.category_name);
      if (selectedCategory) {
        this.editedEntry.category_id = selectedCategory.id;
      }
    }
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_URL}/api/categories`);
        this.categories = response.data.categories.map(([id, name]) => ({
          id,
          name
        }));
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    },

    validateTitle() {
      if (!this.editedEntry.Title) {
        this.errors.title = "Title is required";
      } else {
        this.errors.title = "";
      }
    },

    validateCategory() {
      if (!this.editedEntry.category_id) {
        this.errors.category = "Category is required";
      } else {
        this.errors.category = "";
      }
    },

    validateAmount() {
      if (!this.editedEntry.Amount) {
        this.errors.amount = "Amount is required";
      } else if (isNaN(this.editedEntry.Amount)) {
        this.errors.amount = "Invalid amount format";
      } else {
        this.errors.amount = "";
      }
    },

    validateDate() {
      if (!this.editedEntry.date) {
        this.errors.date = "Date is required";
      } else {
        this.errors.date = "";
      }
    },

    async updateFinanceEntry() {
      this.validateTitle();
      this.validateCategory();
      this.validateAmount();
      this.validateDate();

      if (Object.values(this.errors).some((error) => error)) return;

      try {
        const token = localStorage.getItem("token");
        
        // Prepare the data for submission
        const submitData = {
          ...this.editedEntry,
          category: this.editedEntry.category_id // Make sure category field has the ID
        };
        
        const response = await axios.put(
          `${process.env.VUE_APP_URL}/api/portfolio/edit/${this.editedEntry.entry_ID}`,
          submitData,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        this.$emit("close", response); // Close the modal with response
        window.location.reload();

      } catch (error) {
        console.error("Error updating finance entry:", error);
      }
    },

    closeModal() {
      console.log(this.editedEntry);
      this.$emit("close");
    }
  }
};
</script>
<style scoped>
/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Modal Box */
.modal-content {
  background: white;
  padding: 25px;
  border-radius: 10px;
  width: 350px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
}

/* Input Fields */
.input-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
  text-align: left;
}

.input-group label {
  font-weight: bold;
  margin-bottom: 5px;
}

.input-field {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  width: 100%;
}

.error-message {
  color: #dc3545;
}

/* Button Group */
.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.save-btn {
  background: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.cancel-btn {
  background: #dc3545;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.save-btn:hover {
  background: #0056b3;
}

.cancel-btn:hover {
  background: #b02a37;
}
</style>
