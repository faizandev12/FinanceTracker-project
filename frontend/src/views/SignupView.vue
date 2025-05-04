<template>
  <div class="signup-container">
    <h1>Sign Up</h1>
    <form @submit.prevent="handleSubmit">
      <!-- First Name -->
      <div class="form-group">
        <label for="firstName">First Name:</label>
        <input
          type="text"
          id="firstName"
          v-model="formData.firstName"
          @blur="validateField('firstName')"
          placeholder="Enter your first name"
          required
        />
        <div v-if="errors.firstName" class="error-message">{{ errors.firstName }}</div>
      </div>

      <!-- Last Name -->
      <div class="form-group">
        <label for="lastName">Last Name:</label>
        <input
          type="text"
          id="lastName"
          v-model="formData.lastName"
          @blur="validateField('lastName')"
          placeholder="Enter your last name"
          required
        />
        <div v-if="errors.lastName" class="error-message">{{ errors.lastName }}</div>
      </div>

      <!-- Email -->
      <div class="form-group">
        <label for="email">Email:</label>
        <input
          type="email"
          id="email"
          v-model="formData.email"
          @blur="validateEmail"
          placeholder="Enter your email"
          required
        />
        <div v-if="errors.email" class="error-message">{{ errors.email }}</div>
      </div>

      <!-- Password -->
      <div class="form-group">
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          v-model="formData.password"
          @input="validatePassword"
          placeholder="Enter your password"
          required
        />
        <div class="password-requirements">
          <div v-for="(req, index) in passwordRequirements" 
               :key="index" 
               :class="{ met: req.condition }">
            <span class="requirement-icon">{{ req.condition ? '✓' : '✗' }}</span>
            {{ req.text }}
          </div>
        </div>
        <div v-if="errors.password" class="error-message">{{ errors.password }}</div>
      </div>

      <!-- Confirm Password -->
      <div class="form-group">
        <label for="confirmPassword">Confirm Password:</label>
        <input
          type="password"
          id="confirmPassword"
          v-model="formData.confirmPassword"
          @input="validatePasswordMatch"
          placeholder="Confirm your password"
          required
        />
        <div v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</div>
      </div>

      <button 
        type="submit" 
        :disabled="isSubmitting || !formIsValid" 
        class="submit-button"
      >
        {{ isSubmitting ? 'Creating Account...' : 'Sign Up' }}
      </button>

      <div v-if="serverError" class="server-error">{{ serverError }}</div>

      <div class="already-have-account">
        <h6>
          Already have an account? Click <router-link to="/login">here</router-link>
          to log in.
        </h6>
      </div>
    </form>
  </div>
</template>
<script>
import axios from 'axios';
import { validateEmail } from '@/utils/validators';

export default {
  name: 'SignupPage',
  data() {
    return {
      formData: {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      errors: {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      passwordRequirements: [
        { text: 'At least 8 characters', condition: false },
        { text: 'At least one uppercase letter', condition: false },
        { text: 'At least one lowercase letter', condition: false },
        { text: 'At least one number', condition: false },
        { text: 'At least one symbol (@$!%*?&)', condition: false }
      ],
      serverError: '',
      isSubmitting: false
    };
  },
  computed: {
    formIsValid() {
      return (
        Object.values(this.errors).every(error => !error) &&
        this.passwordRequirements.every(req => req.condition) &&
        this.formData.password === this.formData.confirmPassword
      );
    }
  },
  methods: {
    validateField(field) {
      this.errors[field] = this.formData[field].trim() ? '' : 'This field is required';
    },
    validateEmail() {
      if (!this.formData.email) {
        this.errors.email = 'Email is required';
      } else if (!validateEmail(this.formData.email)) {
        this.errors.email = 'Please enter a valid email address';
      } else {
        this.errors.email = '';
      }
    },
    validatePassword() {
      const password = this.formData.password;
      this.passwordRequirements = [
        { text: 'At least 8 characters', condition: password.length >= 8 },
        { text: 'At least one uppercase letter', condition: /[A-Z]/.test(password) },
        { text: 'At least one lowercase letter', condition: /[a-z]/.test(password) },
        { text: 'At least one number', condition: /\d/.test(password) },
        { text: 'At least one symbol (@$!%*?&)', condition: /[@$!%*?&]/.test(password) }
      ];
      this.errors.password = this.passwordRequirements.every(req => req.condition)
        ? '' 
        : 'Password does not meet requirements';
      this.validatePasswordMatch();
    },
    validatePasswordMatch() {
      this.errors.confirmPassword = 
        this.formData.password === this.formData.confirmPassword
          ? ''
          : 'Passwords do not match';
    },
    async handleSubmit() {
      if (!this.formIsValid || this.isSubmitting) return;

      this.isSubmitting = true;
      this.serverError = '';

      try {
        const response = await axios.post(
          `${process.env.VUE_APP_URL}/api/signup`,
          {
            firstName: this.formData.firstName.trim(),
            lastName: this.formData.lastName.trim(),
            email: this.formData.email.toLowerCase().trim(),
            password: this.formData.password
          }
        );

        if (response.status === 201) {
          this.$router.push({
            name: 'login',
            query: { newUser: true }
          });
        }
      } catch (error) {
        console.error('Signup error:', error);
        this.serverError = error.response?.data?.error || 
                         error.message || 
                         'Signup failed. Please try again.';
        
        if (error.response?.status === 409) {
          this.errors.email = 'This email is already registered';
        }
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
/* Global box-sizing reset */
* {
  box-sizing: border-box;
}

/* Container Styling */
.signup-container {
  max-width: 480px;
  width: 100%;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

/* Form Group */
.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
  color: #2d3748;
  font-weight: 600;
}

/* Input Styling */
input {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1.5px solid #cbd5e0;
  border-radius: 8px;
  transition: border-color 0.2s, box-shadow 0.2s;
  background-color: #f9fafb;
}

input:focus {
  border-color: #4299e1;
  outline: none;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.25);
}

/* Error Message Styling */
.error-message {
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #e53e3e;
  min-height: 1.25rem;
}

/* Server Error Styling */
.server-error {
  margin: 1rem 0;
  padding: 0.75rem;
  text-align: center;
  color: #e53e3e;
  background-color: #fff5f5;
  border: 1px solid #fed7d7;
  border-radius: 8px;
  font-size: 0.95rem;
}

/* Password Requirements Styling */
.password-requirements {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  background-color: #f7fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.875rem;
}

.password-requirements div {
  display: flex;
  align-items: center;
  margin-bottom: 0.4rem;
  color: #4a5568;
}

.requirement-icon {
  margin-right: 0.5rem;
  font-weight: bold;
  width: 1.2rem;
}

/* Correct Icon Colors */
.password-requirements div.met {
  color: #38a169; /* green for satisfied rule */
}

.password-requirements div.met .requirement-icon {
  color: #38a169; /* green check */
}

.password-requirements div:not(.met) .requirement-icon {
  color: #e53e3e; /* red cross */
}

/* Submit Button Styling */
.submit-button {
  width: 100%;
  padding: 0.85rem;
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  background-color: #4299e1;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.submit-button:disabled {
  background-color: #90cdf4;
  cursor: not-allowed;
}

.submit-button:not(:disabled):hover {
  background-color: #3182ce;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
}

/* Already Have Account Link */
.already-have-account {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #4a5568;
}

/* Responsive Tweaks */
@media (max-width: 480px) {
  .signup-container {
    margin: 1rem;
    padding: 1.25rem;
  }

  input {
    padding: 0.65rem;
  }

  .submit-button {
    padding: 0.75rem;
  }
}
</style>
