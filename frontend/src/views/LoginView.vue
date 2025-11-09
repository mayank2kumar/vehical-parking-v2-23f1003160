<template>
  <div class="login-page d-flex flex-column min-vh-100">
    <NavBar />

    <div class="login-content flex-grow-1 d-flex justify-content-center align-items-center">
      <div class="login-card animate__animated animate__fadeInUp">
        <h2 class="text-center mb-3 fw-bold text-black">Welcome Back 👋</h2>
        <p class="text-center text-light-50 mb-4">
          Login to continue to <span class="text-accent">Parking Karo</span>
        </p>

        <form @submit.prevent="login">
          <div class="form-group mb-3">
            <label for="username" class="form-label text-black">Username</label>
            <input
              type="text"
              v-model="username"
              class="form-control custom-input"
              id="username"
              placeholder="Enter your username"
              required
            />
          </div>

          <div class="form-group mb-4">
            <label for="password" class="form-label text-black">Password</label>
            <input
              type="password"
              v-model="password"
              class="form-control custom-input"
              id="password"
              placeholder="Enter your password"
              required
            />
          </div>

            <button 
            type="submit" 
            class="btn btn-glow-dark w-100 py-2 fw-semibold" 
            style="background-color: #6c757d; color: white; border: none; border-radius: 5px;">
            Login
            </button>
        </form>

        <div class="mt-4 text-center">
          <p class="text-dark-50 mb-0">
            Don’t have an account?
            <router-link to="/register" class="register-link fw-semibold">
              Register here
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import { toast } from 'vue3-toastify';

export default {
  name: 'LoginView',
  components: { NavBar },
  data() {
    return {
      username: '',
      password: '',
    };
  },
  async mounted() {
    const token = localStorage.getItem('access_token');
    if (token) {
      const userInfoResponse = await fetch('http://127.0.0.1:5000/get_user_info', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
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
    async login() {
      try {
        const response = await fetch('http://127.0.0.1:5000/login', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });
        const data = await response.json();
        if (!response.ok) {
          toast.error(data.message || 'Login failed', { position: 'top-center' });
          return;
        }

        localStorage.setItem('access_token', data.access_token);
        toast.success(data.message || 'Login successful', {
          position: 'top-center',
          onClose: async () => {
            const token = localStorage.getItem('access_token');
            if (!token) return;

            const userInfoResponse = await fetch('http://127.0.0.1:5000/get_user_info', {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
              },
            });
            const userInfo = await userInfoResponse.json();
            if (userInfo.user && userInfo.user.admin === true) {
              this.$router.push('/admin_dashboard');
            } else {
              this.$router.push('/user_dashboard');
            }
          },
        });
      } catch (error) {
        toast.error('Server error. Try again later.', { position: 'top-center' });
        console.error(error);
      }
    },
  },
};
</script>

<style scoped>
@import 'animate.css';
@import 'bootstrap-icons/font/bootstrap-icons.css';

/* 🌌 THEME COLORS */
:root {
  --primary: #4facfe;
  --secondary: #00f2fe;
  --dark-bg: #0a0f1f;
  --accent: #00d4ff;
}

/* 🩵 Background fills entire page */
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--dark-bg) 0%, #001533 60%, var(--primary) 100%);
  display: flex;
  flex-direction: column;
}

/* 👇 Centers the form */
.login-content {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem 1rem;
}

/* 🧊 Glass card */
.login-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  padding: 2.5rem;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
  transition: all 0.3s ease;
}
.login-card:hover {
  box-shadow: 0 10px 40px rgba(0, 224, 255, 0.4);
}

/* ✏️ Inputs */
.custom-input {
  background: rgba(0, 0, 0, 0.1);
  color: #fafafa;
  border: 1px solid rgba(7, 0, 0, 0.2);
  border-radius: 10px;
  padding: 10px 14px;
  transition: all 0.3s ease;
}
.custom-input::placeholder {
  color: rgba(0, 0, 0, 0.6);
}
.custom-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 12px rgba(0, 212, 255, 0.5);
}

/* 💡 Buttons */
.btn-glow {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: #fff;
  border: none;
  border-radius: 50px;
  transition: all 0.3s ease;
}
.btn-glow:hover {
  transform: translateY(-3px);
  box-shadow: 0 0 25px rgba(79, 172, 254, 0.7);
}

/* 🔤 Text styling */
.text-light-50 {
  color: rgba(0, 0, 0, 0.6);
}
.text-accent {
  color: rgba(122, 0, 0, 0.4);
  text-shadow: 0 0 5px rgba(122, 0, 0, 0.4);

  transition: 0.2s;
}
.text-accent:hover {
  text-decoration: underline;
}
</style>
