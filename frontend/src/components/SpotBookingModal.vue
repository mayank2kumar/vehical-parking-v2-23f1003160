<template>
    <div class="modal-backdrop">
        <div class="modal-container">
            <div class="modal-header">
                <h5 class="modal-title">Select a Spot in {{ lot.prime_location_name }}</h5>
                <button type="button" class="btn-close" @click="$emit('close')"></button>
            </div>

            <div class="modal-body">
                <div class="spot-grid">
                    <div v-for="spot in allSpots" :key="spot.id" class="spot-item">
                        <div v-if="!spot.is_available" class="border border-1 border-dark solid rounded">
                            <img src="@/assets/images/occupied.png" alt="Occupied" class="spot-img" />
                        </div>
                        <button v-else class="btn btn-outline-success" :class="{ selected: selectedSpot === spot.id }"
                            @click="selectSpot(spot.id)" style="width: 100px; height: 100px;">
                            Spot {{ spot.id }}
                        </button>
                    </div>
                </div>
            </div>

            <div class="modal-footer">
                <button class="btn btn-primary" :disabled="!selectedSpot" @click="bookSpot">
                    Book
                </button>
                <button class="btn btn-secondary" @click="$emit('close')">Cancel</button>
            </div>
        </div>
    </div>
</template>

<script>
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default {
    name: 'SpotBookingModal',
    props: {
        lot: Object,
        spots: Array, // only available spots passed
    },
    data() {
        return {
            selectedSpot: null,
            allSpots: [], // includes both available and occupied
        };
    },
    async created() {
        await this.fetchAllSpots();
    },
    methods: {
        async fetchAllSpots() {
            try {
                const res = await fetch(`http://127.0.0.1:5000/get_spots_in_lot/${this.lot.id}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                    },
                });
                const data = await res.json();
                this.allSpots = data.spots;
            } catch (err) {
                toast.error("Failed to fetch spots.");
            }
        },
        selectSpot(id) {
            this.selectedSpot = this.selectedSpot === id ? null : id;
        },
        async bookSpot() {
            if (!this.selectedSpot) return;
            try {
                const res = await fetch(`http://127.0.0.1:5000/reserve_spot/${this.selectedSpot}`, {
                    method: 'POST',
                    headers: {
                        'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                        'Content-Type': 'application/json',
                    },
                });
                const data = await res.json();
                toast.success(data.message || "Booking confirmed");
                this.$emit('reserve', this.selectedSpot);
                this.$emit('close');
            } catch (err) {
                toast.error("Failed to reserve spot.");
            }
        },
    },
};
</script>

<style scoped>
:root {
  --primary: #00bfff;
  --secondary: #0077ff;
  --accent: #00eaff;
  --dark-bg: #050510;
  --green: #00ff8c;
  --red: #ff5b5b;
  --text-light: #e5e5e5;
}

/* 🌌 Backdrop */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  backdrop-filter: blur(8px);
  background: rgba(184, 211, 238, 0.75);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
  animation: fadeIn 0.4s ease-in-out;
}

/* 🧊 Modal Container */
.modal-container {
  background: rgba(152, 191, 203, 0.77);
  border: 1px solid rgba(0, 238, 255, 0.2);
  box-shadow: 0 0 25px rgba(0, 238, 255, 0.25);
  border-radius: 16px;
  padding: 1.5rem;
  width: 90%;
  max-width: 600px;
  color: var(--text-light);
  backdrop-filter: blur(16px);
  animation: popUp 0.4s ease-out;
}

/* 🎯 Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(204, 233, 235, 0.2);
  margin-bottom: 1rem;
}
.modal-title {
  color: var(--accent);
  font-weight: 600;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.352);
}
.btn-close {
  background: none;
  border: none;
  color: var(--text-light);
  font-size: 1.5rem;
  opacity: 0.7;
  transition: all 0.3s ease;
}
.btn-close:hover {
  opacity: 1;
  color: var(--accent);
}

/* 🧱 Body */
.modal-body {
  margin: 1.2rem 0;
  text-align: center;
}

/* 🟩 Spot Grid */
.spot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 1rem;
  justify-items: center;
}
.spot-item {
  text-align: center;
}
.spot-img {
  width: 95px;
  height: 95px;
  border-radius: 8px;
  background: rgba(255, 0, 0, 0.15);
  border: 1px solid rgba(255, 0, 0, 0.3);
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.2);
}

/* 🟢 Available Spots */
.btn-outline-success {
  border: 2px solid var(--green);
  color: var(--green);
  font-weight: 500;
  border-radius: 10px;
  transition: all 0.3s ease;
  background: rgba(7, 62, 155, 0.05);
}
.btn-outline-success:hover {
  background: var(--green);
  color: black;
  box-shadow: 0 0 15px rgba(218, 221, 220, 0.5);
}
.selected {
  background: var(--green) !important;
  color: black !important;
  box-shadow: 0 0 18px rgba(0, 255, 140, 0.7);
}

/* 🦶 Footer */
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
  border-top: 1px solid rgba(0, 238, 255, 0.2);
  padding-top: 1rem;
}
.btn-primary {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border: none;
  color: white;
  border-radius: 25px;
  padding: 0.4rem 1rem;
  transition: all 0.3s ease;
}
.btn-primary:hover {
  box-shadow: 0 0 15px rgba(0, 238, 255, 0.5);
  transform: translateY(-2px);
}
.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--text-light);
  border-radius: 25px;
  padding: 0.4rem 1rem;
  transition: all 0.3s ease;
}
.btn-secondary:hover {
  background: rgba(0, 238, 255, 0.2);
  box-shadow: 0 0 10px rgba(0, 238, 255, 0.3);
}

/* 🎞️ Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes popUp {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* 📱 Responsive */
@media (max-width: 600px) {
  .modal-container {
    width: 95%;
    padding: 1rem;
  }
  .spot-grid {
    grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  }
  .btn-outline-success {
    font-size: 0.85rem;
  }
}
</style>