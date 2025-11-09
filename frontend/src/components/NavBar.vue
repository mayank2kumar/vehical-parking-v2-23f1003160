<template>
  <nav class="navbar navbar-expand-lg glass-navbar fixed-top">
    <div class="container-fluid">
      <!-- Logo + Brand -->
      <div class="d-flex align-items-center">
        <img src="../assets/logo.png" alt="Logo" class="navbar-logo me-2" />
        <router-link class="navbar-brand fw-bold text-light" to="/">
          Parking<span class="text-accent">Karo</span>
        </router-link>
      </div>

      <button
        class="navbar-toggler text-light border-0"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <i class="bi bi-list fs-2"></i>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <!-- USER NAV -->
        <ul v-if="loggedIn && user && !user.admin" class="navbar-nav me-auto px-2">
          <li class="nav-item px-2">
            <router-link class="btn nav-btn" to="/user_dashboard">Home</router-link>
          </li>
          <li class="nav-item px-2">
            <router-link class="btn nav-btn" to="/book_parking">Book</router-link>
          </li>
          <li class="nav-item px-2">
            <router-link class="btn nav-btn" to="/user_search">Search</router-link>
          </li>
          <li class="nav-item px-2">
            <router-link class="btn nav-btn" to="/user_summary">Summary</router-link>
          </li>
        </ul>

        <!-- ADMIN NAV -->
        <ul v-if="loggedIn && user && user.admin" class="navbar-nav me-auto px-2">
          <li class="nav-item px-2">
            <router-link class="btn nav-btn" to="/admin_dashboard">Home</router-link>
          </li>
          <li class="nav-item px-2">
            <router-link class="btn nav-btn" to="/user_management">Users</router-link>
          </li>
          <li class="nav-item px-2">
            <router-link class="btn nav-btn" to="/search">Search</router-link>
          </li>
          <li class="nav-item px-2">
            <router-link class="btn nav-btn" to="/admin_summary">Summary</router-link>
          </li>
        </ul>

        <!-- AUTH / PROFILE -->
        <ul class="navbar-nav ms-auto px-2">
          <li v-if="loggedIn && !user.admin" class="nav-item px-2">
            <router-link class="nav-link user-link" to="/user_profile">
              👤 {{ user.username }}
            </router-link>
          </li>

          <li v-if="loggedIn && user.admin" class="nav-item px-2 text-light fw-semibold align-self-center">
            {{ user.username }}
          </li>

          <li v-if="loggedIn" class="nav-item px-2">
            <button class="btn btn-logout px-3" @click="logout">
              Logout
            </button>
          </li>

          <template v-else>
            <li class="nav-item px-2">
              <router-link class="nav-link auth-link" to="/register">Register</router-link>
            </li>
            <li class="nav-item px-2">
              <router-link class="nav-link auth-link" to="/login">Login</router-link>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import userMixin from '@/mixins/userMixin';
export default {
  name: 'NavBar',
  mixins: [userMixin],
};
</script>

<style scoped>
@import 'bootstrap-icons/font/bootstrap-icons.css';

/* 🌌 Glass Navbar */
.glass-navbar {
  background: rgba(10, 15, 31, 0.75);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.4);
  transition: all 0.3s ease;
}

.navbar-logo {
  width: 45px;
  height: 45px;
  filter: drop-shadow(0 0 4px rgba(79, 172, 254, 0.6));
}

/* ✨ Brand */
.navbar-brand {
  font-size: 1.5rem;
  letter-spacing: 0.5px;
  transition: 0.3s;
}
.text-accent {
  color: #00e0ff;
}

/* 🧊 Nav Buttons */
.nav-btn {
  background: transparent;
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 20px;
  transition: all 0.3s ease;
  font-weight: 500;
  padding: 6px 16px;
}
.nav-btn:hover,
.router-link-active.nav-btn {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
  color: #fff !important;
  border-color: transparent;
  box-shadow: 0 0 10px rgba(0, 242, 254, 0.4);
}

/* 🔐 Auth links */
.auth-link {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
  transition: 0.3s;
}
.auth-link:hover {
  color: #00f2fe;
  text-shadow: 0 0 8px rgba(0, 242, 254, 0.6);
}

/* 👤 Username link */
.user-link {
  color: #00f2fe;
  font-weight: 600;
  text-shadow: 0 0 6px rgba(0, 242, 254, 0.6);
}

/* 🔴 Logout */
.btn-logout {
  background: transparent;
  color: #ff4d4d;
  border: 1px solid rgba(255, 77, 77, 0.3);
  border-radius: 20px;
  transition: 0.3s ease;
}
.btn-logout:hover {
  background: #ff4d4d;
  color: white;
  box-shadow: 0 0 10px rgba(255, 77, 77, 0.5);
}

/* 📱 Responsive adjustments */
@media (max-width: 992px) {
  .glass-navbar {
    backdrop-filter: blur(10px);
    background: rgba(10, 15, 31, 0.95);
  }
  .nav-btn {
    display: block;
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>
