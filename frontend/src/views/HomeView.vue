<template>
  <div class="home">
    <NavBar />

    <!-- HERO SECTION -->
    <!-- HERO SECTION -->
    <section class="hero d-flex flex-column justify-content-center align-items-center text-center position-relative">
      <div class="hero-overlay"></div>
      <div class="hero-content animate__animated animate__fadeInUp">
        <h1 class="display-3 fw-bold text-white mb-3">
          🚗 Smart <span class="text-primary">Parking Finder</span>
        </h1>
        <p class="lead text-light mb-4">
          Find, Book, and Park — Simplifying your parking experience.
        </p>
        <router-link to="/login" class="btn btn-primary btn-lg px-5 shadow-lg">
          Get Started
        </router-link>
      </div>
    </section>


    <!-- LOCATIONS GRID -->
    <section class="locations py-5">
      <div class="container text-center">
        <h2 class="fw-bold mb-4 text-primary">Available Parking Locations</h2>

        <div v-if="isLoadingLocations" class="text-center mt-4">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="text-muted mt-2">Loading locations...</p>
        </div>

        <div v-else-if="!locations.length" class="text-center mt-4 text-muted">
          No locations available at the moment.
        </div>

        <div v-else class="row g-4 justify-content-center">
          <div
            v-for="location in locations"
            :key="location.id"
            class="col-10 col-sm-6 col-md-4 col-lg-3"
          >
            <div class="location-card glass-card animate__animated animate__fadeInUp">
              <i class="bi bi-geo-alt-fill location-icon mb-3"></i>
              <h5 class="fw-semibold mb-1">{{ location.name }}</h5>
              <p class="text-muted mb-0">{{ location.city }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURES SECTION -->
    <section class="features py-5 text-center bg-dark text-light">
      <div class="container">
        <h2 class="fw-bold mb-5">Why Choose <span class="text-primary">Parking Karo?</span></h2>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="feature-card p-4 rounded-4">
              <i class="bi bi-map-fill feature-icon mb-3"></i>
              <h4>Smart Navigation</h4>
              <p>Real-time location tracking and intelligent route suggestions.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card p-4 rounded-4">
              <i class="bi bi-calendar-check-fill feature-icon mb-3"></i>
              <h4>Instant Booking</h4>
              <p>Reserve parking instantly with live spot availability updates.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card p-4 rounded-4">
              <i class="bi bi-shield-check feature-icon mb-3"></i>
              <h4>Safe & Secure</h4>
              <p>Trusted payment, verified lots, and secure reservations guaranteed.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import userMixin from '@/mixins/userMixin';
import { toast } from 'vue3-toastify';

export default {
  name: 'HomeView',
  mixins: [userMixin],
  components: { NavBar },
  data() {
    return {
      locations: [],
      isLoadingLocations: false,
    };
  },
  async mounted() {
    await this.fetchLocations();
  },
  methods: {
    async fetchLocations() {
      this.isLoadingLocations = true;
      try {
        const response = await fetch('http://127.0.0.1:5000/get_locations');
        if (response.ok) {
          const data = await response.json();
          this.locations = data.locations;
        } else {
          const errorData = await response.json();
          toast.error(errorData.message || 'Failed to fetch locations.', { position: 'top-center' });
        }
      } catch (error) {
        console.error('Error fetching locations:', error);
        toast.error('Server error while fetching locations.', { position: 'top-center' });
      } finally {
        this.isLoadingLocations = false;
      }
    },
  },
};
</script>

<style scoped>
@import 'animate.css';
@import 'bootstrap-icons/font/bootstrap-icons.css';

/* GLOBAL COLORS */
:root {
  --primary: #4facfe;
  --secondary: #00f2fe;
  --dark-bg: #0a0f1f;
}

/* Hero Section Styling */
.hero {
  height: 100vh;
  width: 100%;
  background: linear-gradient(
      rgba(0, 0, 0, 0.5),
      rgba(0, 0, 0, 0.6)
    ),
    url("@/assets/background.jpg") center center / cover no-repeat;
  position: relative;
  overflow: hidden;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: linear-gradient(to bottom right, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.6));
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  color: #ffffff;
  text-shadow: 1px 2px 4px rgba(0, 0, 0, 0.7);
}

/* Animation Enhancements */
.hero-content h1 {
  font-size: 3rem;
  letter-spacing: 1px;
}

.hero-content p {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.9);
}

/* Button Styling */
.btn-primary {
  background: linear-gradient(135deg, #007bff, #00a6ff);
  border: none;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #00a6ff, #007bff);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 123, 255, 0.3);
}

/* LOCATIONS SECTION */
.locations {
  background: #f7faff;
}
.location-card {
  background: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 1rem;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.location-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 6px 20px rgba(79, 172, 254, 0.3);
}
.location-icon {
  font-size: 2.5rem;
  color: var(--primary);
}

/* FEATURES SECTION */
.features {
  background: var(--dark-bg);
}
.feature-card {
  background: rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.feature-card:hover {
  transform: translateY(-6px);
  border-color: var(--secondary);
  box-shadow: 0 0 25px rgba(0, 242, 254, 0.3);
}
.feature-icon {
  font-size: 3rem;
  color: var(--secondary);
}
</style>
