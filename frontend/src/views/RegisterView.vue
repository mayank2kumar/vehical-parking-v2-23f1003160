<template>
  <div class="register-page min-vh-100 d-flex flex-column">
    <NavBar />

    <div class="container d-flex flex-column align-items-center justify-content-center py-5">
      <br />
      <h2 class="text-center fw-bold text-accent mb-4 animate__animated animate__fadeInDown">
        ✨ Create Your Account
      </h2>

      <div class="glass-form p-4 rounded-4 shadow-lg animate__animated animate__fadeInUp">
        <form @submit.prevent="register">
          <div class="form-group mb-3">
            <label for="name" class="form-label text-light-50">Full Name</label>
            <input
              type="text"
              v-model="name"
              class="form-control custom-input"
              id="name"
              placeholder="Enter name"
              required
            />
          </div>

          <div class="form-group mb-3">
            <label for="username" class="form-label text-light-50">Username</label>
            <input
              type="text"
              v-model="username"
              class="form-control custom-input"
              id="username"
              placeholder="Enter username"
              required
            />
          </div>

          <div class="form-group mb-3">
            <label for="email" class="form-label text-light-50">Email</label>
            <input
              type="email"
              v-model="email"
              class="form-control custom-input"
              id="email"
              placeholder="Enter email"
              required
            />
          </div>

          <div class="form-group mb-3">
            <label for="password" class="form-label text-light-50">Password</label>
            <input
              type="password"
              v-model="password"
              class="form-control custom-input"
              id="password"
              placeholder="Enter password"
              required
            />
          </div>

          <div class="form-group mb-4">
            <label for="confirmPassword" class="form-label text-light-50">Confirm Password</label>
            <input
              type="password"
              v-model="confirmPassword"
              class="form-control custom-input"
              id="confirmPassword"
              placeholder="Confirm password"
              required
            />
          </div>

          <button type="submit" class="btn btn-glow w-100 py-2 fw-semibold">
            Register
          </button>

          <p class="text-center text-light-50 mt-3 mb-0">
            Already have an account?
            <router-link to="/login" class="text-accent fw-semibold text-decoration-none">
              Login here
            </router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import { toast } from 'vue3-toastify';

export default {
  name: 'RegisterView',
  components: { NavBar },
  data() {
    return {
      name: '',
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    };
  },
  async mounted() {
    const token = localStorage.getItem('access_token');
    if (token) {
      const userInfoResponse = await fetch('http://127.0.0.1:5000/get_user_info', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });
      const userInfo = await userInfoResponse.json();
      if (userInfo.user && userInfo.user.admin === true) {
        this.$router.push('/admin_dashboard');
      } else {
        this.$router.push('/user_dashboard');
      }
    }
  },
  methods: {
    checkPasswordsMatch() {
      return this.password === this.confirmPassword;
    },
    async register() {
      if (!this.checkPasswordsMatch()) {
        toast.error('Passwords do not match');
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:5000/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: this.name,
            username: this.username,
            email: this.email,
            password: this.password,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          if (data.message === 'User already exists') {
            toast.warning(data.message, {
              onClose: () => this.$router.push('/login'),
            });
          } else {
            toast.error(data.message || 'Registration failed');
          }
        } else {
          toast.success(data.message || 'Registration successful', {
            onClose: () => this.$router.push('/login'),
          });
        }
      } catch (error) {
        toast.error('Server error. Try again later.');
      }
    },
  },
};
</script>

<style scoped>
@import 'animate.css';

:root {
  --primary: #00bfff;        /* Neon cyan-blue */
  --secondary: #0077ff;      /* Bright blue */
  --accent: #00eaff;         /* Light glow cyan */
  --dark-bg: #050510;        /* Deep dark navy background */
  --text-light: #e5e5e5;     /* Soft white text */
  --text-muted: #9aa0a6;     /* Muted gray text */
}

/* 🌌 Page Background */
.register-page {
  background: linear-gradient(160deg, var(--dark-bg) 0%, #001122 80%);
  color: var(--text-light);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* 🧊 Glass Form */
.glass-form {
  background: rgba(105, 100, 100, 0.6);
  border: 1px solid rgba(187, 211, 35, 0.2);
  border-radius: 16px;
  backdrop-filter: blur(18px);
  width: 100%;
  max-width: 420px;
  transition: all 0.3s ease;
  box-shadow: 0 0 20px rgba(0, 200, 255, 0.15);
}
.glass-form:hover {
  transform: translateY(-3px);
  box-shadow: 0 0 30px rgba(0, 238, 255, 0.25);
}

/* 🩵 Input Styling */
.custom-input {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-light);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  transition: all 0.3s ease;
}
.custom-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 12px rgba(0, 238, 255, 0.6);
  outline: none;
  background: rgba(255, 255, 255, 0.08);
}
.custom-input::placeholder {
  color: var(--text-muted);
}

/* ✨ Button Glow */
.btn-glow {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: #fff;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
}
.btn-glow:hover {
  transform: translateY(-3px);
  box-shadow: 0 0 20px rgba(0, 238, 255, 0.6);
  background: linear-gradient(135deg, var(--secondary), var(--primary));
}

/* 💡 Text Styles */
.text-accent {
  color: var(--accent);
}
.text-light-50 {
  color: var(--text-muted);
}

/* 🧱 Form Label */
.form-label {
  color: var(--text-light);
  font-weight: 500;
}

/* 🎯 Page Title */
h2 {
  color: var(--accent);
  font-size: 1.8rem;
  text-shadow: 0 0 10px rgba(0, 238, 255, 0.3);
}

/* 📱 Responsive */
@media (max-width: 768px) {
  .glass-form {
    max-width: 90%;
    padding: 1.5rem;
  }
  h2 {
    font-size: 1.5rem;
  }
}
</style>

