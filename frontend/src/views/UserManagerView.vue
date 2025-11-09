<template>
  <div class="user-manager-page d-flex flex-column min-vh-100">
    <NavBar />

    <div class="container py-5">
        <br></br>
      <h2 class="text-center fw-bold text-dark-glow mb-3">User Manager</h2>
      <p class="text-center text-light-50 mb-5">Manage all registered users and view their reservation activity</p>

      <div class="glass-table-wrapper p-4 rounded-4 shadow-lg">
        <table class="table table-borderless align-middle mb-0">
          <thead>
            <tr class="table-header">
              <th>User ID</th>
              <th>Name</th>
              <th>Username</th>
              <th>Email</th>
              <th>Reserved Spots</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="user in users"
              :key="user.id"
              class="table-row animate__animated animate__fadeInUp"
            >
              <td> {{ user.id }} </td>
              <td class="fw-semibold">{{ user.name }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>
                <span
                  class="badge"
                  :class="user.reserved_spots > 0 ? 'bg-dark' : 'bg-secondary'"
                >
                  {{ user.reserved_spots }}
                </span>
              </td>
              <td>
                <button
                  class="btn btn-danger-glow btn-sm"
                  @click="deleteUser(user.id)"
                >
                  <i class="bi bi-trash"></i> Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import { toast } from 'vue3-toastify';

export default {
  name: 'UserManagerView',
  components: { NavBar },
  data() {
    return {
      users: [],
      reservations: []
    };
  },
  async mounted() {
    try {
      const response = await fetch('http://127.0.0.1:5000/admin_dashboard', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
      });

      if (!response.ok) {
        toast.error('Access Denied: You are logged in as a user.', { position: 'top-center' });
        this.$router.push('/user_dashboard');
      } else {
        await this.getLots();
        await this.getUsers();
      }
    } catch (error) {
      toast.error('Server error.', { position: 'top-center' });
      console.error(error);
    }
  },
  methods: {
    async getLots() {
      try {
        const response = await fetch('http://127.0.0.1:5000/parking_lots', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        const data = await response.json();
        this.reservations = data.reservedSpots;
      } catch (error) {
        console.error(error);
        toast.error('Failed to fetch reservation data.', { position: 'top-center' });
      }
    },
    async getUsers() {
      try {
        const response = await fetch('http://127.0.0.1:5000/get_users', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        const data = await response.json();

        const reservationCounts = {};
        for (const reservation of this.reservations) {
          const userId = reservation.user_id;
          reservationCounts[userId] = (reservationCounts[userId] || 0) + 1;
        }

        this.users = data.users.map(user => ({
          ...user,
          reserved_spots: reservationCounts[user.id] || 0
        }));
      } catch (error) {
        console.error(error);
        toast.error('Failed to fetch user data.', { position: 'top-center' });
      }
    },
    async deleteUser(userId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/delete_user/${userId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        if (response.ok) {
          toast.success('User deleted successfully.', { position: 'top-center' });
          this.getUsers();
        } else {
          toast.error('Failed to delete user.', { position: 'top-center' });
        }
      } catch (error) {
        console.error(error);
        toast.error('Failed to delete user.', { position: 'top-center' });
      }
    }
  }
};
</script>

<style scoped>
@import 'animate.css';
@import 'bootstrap-icons/font/bootstrap-icons.css';

:root {
  --primary: #4facfe;
  --secondary: #00f2fe;
  --dark-bg: #0a0f1f;
  --accent: #00d4ff;
}

/* 🌌 Background */
.user-manager-page {
  background: linear-gradient(135deg, var(--dark-bg) 0%, #001533 70%, var(--primary) 100%);
  color: rgb(0, 0, 0);
  min-height: 100vh;
}

/* 🧊 Glass wrapper */
.glass-table-wrapper {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  backdrop-filter: blur(15px);
  overflow-x: auto;
}

/* 🩵 Table Header */
.table-header {
  color: var(--accent);
  font-weight: 600;
  border-bottom: 2px solid rgba(0, 224, 255, 0.2);
}

/* 🧾 Table Rows */
.table-row {
  color: rgba(0, 0, 0, 0.85);
  transition: all 0.3s ease;
}
.table-row:hover {
  background: rgba(0, 224, 255, 0.1);
  box-shadow: inset 0 0 15px rgba(0, 242, 254, 0.15);
  transform: translateY(-2px);
}

/* 🪩 Badges */
.bg-accent {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: #fff;
  border-radius: 10px;
  padding: 4px 10px;
}
.bg-secondary {
  background: rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  padding: 4px 10px;
}

/* 💀 Delete Button */
.btn-danger-glow {
  background: transparent;
  color: #ff4d4d;
  border: 1px solid rgba(255, 77, 77, 0.3);
  border-radius: 20px;
  transition: all 0.3s ease;
}
.btn-danger-glow:hover {
  background: #ff4d4d;
  color: #fff;
  box-shadow: 0 0 12px rgba(255, 77, 77, 0.6);
  transform: translateY(-2px);
}

/* 🩶 Text helpers */
.text-light-50 {
  color: rgb(0, 0, 0);
}

/* 📱 Responsive */
@media (max-width: 768px) {
  .table {
    font-size: 0.9rem;
  }
  .btn-danger-glow {
    padding: 4px 8px;
  }
}
</style>
