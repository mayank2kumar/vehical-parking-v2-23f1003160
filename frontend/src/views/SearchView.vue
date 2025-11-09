<template>
  <div class="search-page min-vh-100 d-flex flex-column">
    <NavBar />

    <div class="container py-5 text-center">
      <br>    </br>
      <h2 class="fw-bold text-dark-glow mb-3">Admin Search</h2>
      <p class="text-dark-100 mb-4">Search across Users, Parking Lots, and Reservations</p>

      <!-- Search Box -->
      <div class="search-box mx-auto mb-3">
        <input
          v-model="query"
          @keyup.enter="performSearch"
          type="text"
          class="form-control form-control-lg custom-input"
          placeholder="🔍 Search users, lots, or reservations..."
        />
      </div>

      <button class="btn btn-glow px-4 border-5" @click="performSearch">
        <i class="bi bi-search"></i> Search
      </button>

      <!-- Results Section -->
      <div class="results-section mt-5 text-start">
        <!-- USERS -->
        <div v-if="results.users && results.users.length" class="glass-table-wrapper mb-5 animate__animated animate__fadeInUp">
          <h4 class="text-accent text-center mb-3">👤 Users ({{ results.users.length }})</h4>
          <div class="table-responsive">
            <table class="table table-borderless align-middle">
              <thead class="table-header">
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in results.users" :key="user.ID" class="table-row">
                  <td>{{ user.ID }}</td>
                  <td>{{ user.Name }}</td>
                  <td>{{ user.Username }}</td>
                  <td>{{ user.Email }}</td>
                  <td>
                    <button class="btn btn-danger-glow btn-sm" @click="deleteUser(user.ID)">
                      <i class="bi bi-trash"></i> Delete
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- PARKING LOTS -->
        <div v-if="results.lots && results.lots.length" class="glass-table-wrapper mb-5 animate__animated animate__fadeInUp">
          <h4 class="text-accent text-center mb-3">🅿️ Parking Lots ({{ results.lots.length }})</h4>
          <div class="table-responsive">
            <table class="table table-borderless align-middle">
              <thead class="table-header">
                <tr>
                  <th>ID</th>
                  <th>Location</th>
                  <th>Address</th>
                  <th>Pin</th>
                  <th>Price</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="lot in results.lots" :key="lot.ID" class="table-row">
                  <td>{{ lot.ID }}</td>
                  <td>{{ lot.Location }}</td>
                  <td>{{ lot.Address }}</td>
                  <td>{{ lot.Pin }}</td>
                  <td>₹ {{ lot.Price?.toFixed(2) || 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- RESERVATIONS -->
        <div v-if="results.reservations && results.reservations.length" class="glass-table-wrapper animate__animated animate__fadeInUp">
          <h4 class="text-accent text-center mb-3">🕒 Reservations ({{ results.reservations.length }})</h4>
          <div class="table-responsive">
            <table class="table table-borderless align-middle">
              <thead class="table-header">
                <tr>
                  <th>ID</th>
                  <th>User ID</th>
                  <th>Spot ID</th>
                  <th>Park Time</th>
                  <th>Exit Time</th>
                  <th>Total Cost</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="res in results.reservations" :key="res.ID" class="table-row">
                  <td>{{ res.ID }}</td>
                  <td>{{ res["User ID"] }}</td>
                  <td>{{ res["Spot ID"] }}</td>
                  <td>{{ res["Park Time"] }}</td>
                  <td>{{ res["Exit Time"] }}</td>
                  <td>₹ {{ res["Total Cost"] != null ? res["Total Cost"] : 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- NO RESULTS -->
        <div v-if="!totalResults && searched" class="text-light-50 text-center mt-4">
          <i class="bi bi-x-circle"></i> No matching results found.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import { toast } from 'vue3-toastify';

export default {
  name: 'SearchView',
  components: { NavBar },
  data() {
    return {
      query: '',
      results: {
        users: [],
        lots: [],
        reservations: []
      },
      searched: false
    };
  },
  computed: {
    totalResults() {
      return (
        this.results.users.length +
        this.results.lots.length +
        this.results.reservations.length
      );
    }
  },
  async mounted() {
    try {
      const res = await fetch('http://127.0.0.1:5000/admin_dashboard', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
      });
      if (!res.ok) {
        toast.error('Unauthorized or server error.', {
          position: 'top-center',
          onClose: () => this.$router.push('/login')
        });
      }
    } catch (err) {
      console.error(err);
      toast.error('Failed to fetch initial data.', { position: 'top-center' });
    }
  },
  methods: {
    async deleteUser(id) {
      try {
        const res = await fetch(`http://127.0.0.1:5000/delete_user/${id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
          }
        });

        if (!res.ok) {
          toast.error('Unauthorized or server error.', { position: 'top-center' });
          return;
        }

        toast.success('User deleted successfully.', { position: 'top-center' });
        this.results.users = this.results.users.filter(user => user.ID !== id);
      } catch (err) {
        console.error(err);
        toast.error('Delete failed.', { position: 'top-center' });
      }
    },

    async performSearch() {
      this.searched = true;
      this.results = { users: [], lots: [], reservations: [] };

      if (!this.query.trim()) {
        toast.warning('Enter a search query.', { position: 'top-center' });
        return;
      }

      try {
        const res = await fetch(`http://127.0.0.1:5000/search?q=${encodeURIComponent(this.query)}`, {
          method: 'GET',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
          }
        });

        if (!res.ok) {
          toast.error('Unauthorized or server error.', { position: 'top-center' });
          return;
        }

        const data = await res.json();
        this.results = {
          users: data.users || [],
          lots: data.lots || [],
          reservations: data.reservations || []
        };
      } catch (err) {
        console.error(err);
        toast.error('Search failed.', { position: 'top-center' });
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

/* 🌌 Page background */
.search-page {
  background: linear-gradient(135deg, var(--dark-bg) 0%, #001533 70%, var(--primary) 100%);
  color: rgb(0, 0, 0);
}

/* 🔍 Search Box */
.search-box {
  max-width: 600px;
  border: 1px solid #ccc; /* visible border */
  background-color: #f0f0f0; /* light grey fill */
  padding: 8px 12px; /* optional: inner spacing */
  border-radius: 4px; /* optional: rounded corners */
}

.custom-input {
  background: rgba(255, 255, 255, 0.08);
  color: rgb(0, 0, 0);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  transition: all 0.3s ease;
}
.custom-input::placeholder {
  color: rgba(125, 198, 237, 0.721);
}
.custom-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 12px rgba(0, 224, 255, 0.5);
}

/* 🧊 Table Container */
.glass-table-wrapper {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  padding: 1.5rem;
  backdrop-filter: blur(15px);
}

/* 🩵 Table Header */
.table-header {
  color: rgba(0, 0, 0, 0.9);
  font-weight: 600;
  border-bottom: 2px solid rgba(0, 224, 255, 0.2);
}

/* 🧾 Table Rows */
.table-row {
  color: rgba(0, 0, 0, 0.9);
  transition: all 0.3s ease;
}
.table-row:hover {
  background: rgba(0, 224, 255, 0.1);
  transform: translateY(-2px);
}

/* 💡 Buttons */
.btn-glow {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: rgb(0, 0, 0);
  border: none;
  border-radius: 50px;
  transition: all 0.3s ease;
}
.btn-glow:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(0, 242, 254, 0.6);
}

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
}

/* 🩶 Text helpers */
.text-accent {
  color: rgba(0, 0, 0, 0);
}
.text-light-50 {
  color: rgba(0, 0, 0, 0);
}

/* 📱 Responsive */
@media (max-width: 768px) {
  .custom-input {
    font-size: 1rem;
  }
  .glass-table-wrapper {
    padding: 1rem;
  }
}
</style>
