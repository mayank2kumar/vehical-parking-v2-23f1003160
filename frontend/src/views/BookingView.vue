<template>
    <NavBar />
    <div class="container py-5">
        <br>    </br>
        <div class="text-center mb-5">
            <h2 class="fw-bold">Parking Lots</h2>
        </div>

        <!-- Animated Card Group -->
        <transition-group name="fade" tag="div" class="row" appear>
            <div v-for="lot in visibleLots" :key="lot.id" class="col-12 col-md-6 col-lg-4 mb-4">
                <div class="card shadow border-0 h-100">
                    <div class="card-header bg-dark text-white text-center">
                        <h5 class="mb-0">{{ lot.prime_location_name }}</h5>
                    </div>
                    <div class="card-body">
                        <p><strong>Address:</strong> {{ lot.address }}</p>
                        <p><strong>Price:</strong> ₹{{ lot.price }} / hr</p>
                        <p>
                            <strong>Available Spots:</strong>
                            {{
                                spots.filter(
                                    (spot) => spot.lot_id === lot.id && spot.is_available
                                ).length
                            }}
                        </p>
                    </div>
                    <div class="card-footer text-center">
                        <button class="btn btn-outline-primary" @click="openModal(lot)">
                            View / Book
                        </button>
                    </div>
                </div>
            </div>
        </transition-group>

        <!-- Show More Button -->
        <div v-if="lots.length > 6 && !showAll" class="text-center mt-3">
            <button class="btn btn-dark" @click="showAll = true">
                Show More
            </button>
        </div>

        <!-- Modal -->
        <SpotBookingModal v-if="selectedLot" :lot="selectedLot"
            :spots="spots.filter((s) => s.lot_id === selectedLot.id && s.is_available)" @close="selectedLot = null"
            @reserve="handleSpotReserved" /> <!-- Changed @reserve to call handleSpotReserved -->
    </div>
</template>

<script>
import SpotBookingModal from '@/components/SpotBookingModal.vue';
import NavBar from '@/components/NavBar.vue';
import { toast } from 'vue3-toastify';

export default {
    name: 'BookingView',
    components: {
        NavBar,
        SpotBookingModal,
    },
    data() {
        return {
            lots: [],
            spots: [],
            locations: [],
            selectedLot: null,
            showAll: false,
        };
    },
    computed: {
        visibleLots() {
            return this.showAll ? this.lots : this.lots.slice(0, 6);
        },
    },
    async mounted() {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                this.$router.push('/login');
                return;
            }

            const response = await fetch('http://127.0.0.1:5000/user_dashboard', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });
            if (!response.ok) {
                this.$router.push('/login');
                return;
            }
        } catch (error) {
            toast.error('Server error.', { position: 'top-center' });
            console.error(error);
            this.$router.push('/login');
            return;
        }
        await this.getLots();
        await this.getLocations();
    },
    methods: {
        async getLots() {
            try {
                const res = await fetch('http://127.0.0.1:5000/get_lots', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                    },
                });
                const data = await res.json();
                this.lots = data.lots;
                this.spots = data.spots;
            } catch (err) {
                toast.error('Failed to fetch lots.');
            }
        },
        async getLocations() {
            try {
                const res = await fetch('http://127.0.0.1:5000/get_locations', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                    },
                });
                const data = await res.json();
                this.locations = data.locations;
            } catch (err) {
                toast.error('Failed to fetch locations.');
            }
        },
        // This method is now responsible for refreshing data after the modal books a spot
        async handleSpotReserved() {
            // Close the modal
            this.selectedLot = null;
            // Refresh the lots and spots data to reflect the change in availability
            await this.getLots();
        },
        openModal(lot) {
            this.selectedLot = lot;
        },
    },
};
</script>

<style scoped>
@import 'animate.css';

:root {
  --primary: #00bfff;
  --secondary: #0077ff;
  --accent: #00eaff;
  --dark-bg: #050510;
  --text-light: #e5e5e5;
  --text-muted: #9aa0a6;
}

/* 🌌 Page Background */
.container {
  background: linear-gradient(160deg, var(--dark-bg) 0%, #001122 80%);
  min-height: 100vh;
  color: var(--text-light);
  border-radius: 12px;
  padding: 2rem;
  animation: fadeIn 0.8s ease-in-out;
}

/* 🎯 Heading */
h2.fw-bold {
  color: var(--accent);
  text-shadow: 0 0 15px rgba(0, 238, 255, 0.4);
  letter-spacing: 1px;
  margin-bottom: 1.5rem;
}

/* 🧊 Glass Card */
.card {
  background: rgba(152, 191, 203, 0.77);
  border: 1px solid rgba(57, 67, 68, 0.2);
  border-radius: 16px;
  backdrop-filter: blur(16px);
  transition: all 0.3s ease;
  overflow: hidden;
  color: var(--text-light);
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 25px rgba(0, 238, 255, 0.25);
}

/* 💡 Card Header */
.card-header {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border: none;
  color: white;
  border-radius: 16px 16px 0 0;
  box-shadow: 0 0 12px rgba(0, 238, 255, 0.3);
}
.card-header h5 {
  margin: 0;
  font-weight: 600;
}

/* 📄 Card Body */
.card-body {
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.03);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}
.card-body p {
  margin-bottom: 0.6rem;
  color: var(--text-light);
  font-size: 0.95rem;
}

/* 🦶 Card Footer */
.card-footer {
  background: rgba(0, 0, 0, 0.4);
  border-top: 1px solid rgba(0, 238, 255, 0.15);
  text-align: center;
  padding: 1rem;
}

/* 🩵 Buttons */
.btn {
  border-radius: 25px;
  transition: all 0.3s ease;
  font-weight: 500;
}
.btn-outline-primary {
  border-color: var(--accent);
  color: var(--accent);
  background: transparent;
}
.btn-outline-primary:hover {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 0 15px rgba(0, 238, 255, 0.5);
}
.btn-secondary {
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-light);
  border: 1px solid rgba(255, 255, 255, 0.15);
}
.btn-secondary:hover {
  background: rgba(0, 238, 255, 0.15);
  color: white;
  box-shadow: 0 0 15px rgba(0, 238, 255, 0.3);
}

/* ✨ Fade Animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.6s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.fade-move {
  transition: transform 0.5s ease;
}

/* 🧭 Layout */
.row {
  margin-top: 1rem;
}
.col-lg-4 {
  display: flex;
}

/* 🎞️ Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 📱 Responsive */
@media (max-width: 768px) {
  .card-body p {
    font-size: 0.9rem;
  }
  h2.fw-bold {
    font-size: 1.6rem;
  }
}
</style>