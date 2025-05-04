import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/LoginView.vue';
import SignupView from '@/views/SignupView.vue';
import DashboardView from '@/views/DashboardView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }, // Mark this route as protected
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// Global navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token'); // Check for token in localStorage

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!token) {
      // Redirect to login if no token is found
      next({ name: 'login' });
    } else {
      // Allow access if token exists
      next();
    }
  } else {
    // Allow access to routes that don't require authentication
    next();
  }
});

export default router;
