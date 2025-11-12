<template>
  <div class="admin-page d-flex flex-column min-vh-100">
    <NavBar />

    <div class="admin-content container py-5">
      <br></br>
      <h2 class="text-center fw-bold text-dark-glow mb-4">Admin Dashboard</h2>
      <h4 class="text-center text-accent mb-5">Manage Parking Places</h4>

      <div class="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
        <p class="text-light-50 mb-2 mb-sm-0">Total Available Places: {{ lots.length }}</p>
        <div class="d-flex gap-2">
          <button class="btn btn-add-parking" @click="showAddModal = true">
            <i class="bi bi-car-front me-1"></i> Add Parking Lot
          </button>
          <button class="btn btn-add-location" @click="showAddLocationModal = true">
            <i class="bi bi-geo-alt me-1"></i> Add Location
          </button>
        </div>
      </div>

      <!-- Parking Lot Cards -->
      <transition-group name="fade" tag="div" class="row g-4" appear>
        <div
          class="col-sm-12 col-md-6 col-lg-3"
          v-for="(lot, index) in displayLots"
          :key="lot.id"
        >
          <div class="lot-card glass-card h-100 d-flex flex-column animate__animated animate__fadeInUp">
            <div class="card-header border-0">
              <h5 class="fw-semibold text-accent mb-0">
                {{ lot.prime_location_name }}
              </h5>
              <p>📍 <span class="fw-semibold">Location:</span> {{ lot.location_name }} ({{ lot.city }})</p>

            </div>
            <div class="card-body text-light-50 flex-grow-1">
              <p>💰 <span class="fw-semibold">Price/hr:</span> ₹ {{ lot.price }}</p>
              <p>📍 <span class="fw-semibold">Address:</span> {{ lot.address }}</p>
              <p>📫 <span class="fw-semibold">Pin Code:</span> {{ lot.pin_code }}</p>
              <p>🅿️ <span class="fw-semibold">Spots:</span> {{ lot.number_of_spots }}</p>
              <p>🔒 <span class="fw-semibold">Reserved:</span> {{ lot.hasReservedSpots ? 'Yes' : 'No' }}</p>
            </div>

            <div class="card-footer border-0 d-flex justify-content-center gap-2 mb-3">
              <button class="btn btn-outline-primary btn-sm" @click="openViewModal(lot)">View</button>
              <button class="btn btn-outline-warning btn-sm" @click="openEditModal(lot)">Edit</button>
              <button
                class="btn btn-outline-danger btn-sm"
                :disabled="lot.hasReservedSpots"
                @click="deleteLot(lot.id)"
                data-bs-toggle="tooltip"
                :title="lot.hasReservedSpots ? 'Cannot delete: reserved spots exist' : ''"
               >
                Delete
              </button>
            </div>
          </div>
        </div>
      </transition-group>

      <div v-if="lots.length > 8 && !showAll" class="text-center mt-4">
        <button class="btn btn-outline-accent px-4" @click="showAll = true">
          Show All
        </button>
      </div>
    </div>

    <!-- Modals -->
    <AddLotModal v-if="showAddModal" @close="showAddModal = false" @lot-added="handleLotAdded" />
    <ViewLotModal
      v-if="showViewModal"
      :lot="selectedLot"
      :spots="spots"
      :reservedSpots="reservedSpots"
      @close="showViewModal = false"
    />
    <AddLocationModal 
      v-if="showAddLocationModal"
      @close="showAddLocationModal = false"
      @location-added="handleLocationAdded"
    />

    <EditLotModal
      v-if="showEditModal"
      :lot="selectedLot"
      @close="showEditModal = false"
      @lot-updated="handleLotUpdated"
    />
  </div>
</template>

<script>
import AddLocationModal from '@/components/AddLocationModal.vue';
import NavBar from '@/components/NavBar.vue';
import ViewLotModal from '@/components/ViewLotModal.vue';
import EditLotModal from '@/components/EditLotModal.vue';
import AddLotModal from '@/components/AddLotModal.vue';
import * as bootstrap from 'bootstrap';
import { toast } from 'vue3-toastify';

export default {
  name: 'AdminView',
  components: { NavBar, ViewLotModal, EditLotModal, AddLotModal, AddLocationModal },
  data() {
    return {
      lots: [],
      spots: [],
      reservedSpots: [],
      showAll: false,
      showViewModal: false,
      showEditModal: false,
      showAddModal: false,
      showAddLocationModal: false,
      selectedLot: null,
    };
  },
  computed: {
    displayLots() {
      return this.showAll ? this.lots : this.lots.slice(0, 8);
    },
  },
  async mounted() {
    try {
      const response = await fetch('http://127.0.0.1:5000/admin_dashboard', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      });

      if (!response.ok) {
        toast.error('Access Denied: You are logged in as a user.', { position: 'top-center' });
        this.$router.push('/user_dashboard');
      } else {
        await this.getLots();
        this.enableTooltips();
      }
    } catch (error) {
      toast.error('Server error.', { position: 'top-center' });
      console.error(error);
    }
  },
  methods: {
    async handleLocationAdded() {
      this.showAddLocationModal = false;
      // Refresh lots (so dropdown updates)
      await this.getLots();
    },

    async getLots() {
      try {
        // Fetch all lots, spots, and reservations
        const resLots = await fetch('http://127.0.0.1:5000/parking_lots', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        });
        const data = await resLots.json();

        // Fetch all locations separately
        const resLoc = await fetch('http://127.0.0.1:5000/get_locations', {
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        });
        const locData = await resLoc.json();

        // Build lookup: { location_id: location_name }
        const locationMap = {};
        if (locData.locations && locData.locations.length > 0) {
          for (const loc of locData.locations) {
            locationMap[loc.id] = { name: loc.name, city: loc.city };
          }
        }

        this.reservedSpots = data.reservedSpots;
        this.spots = data.spots.map((spot) => ({
          id: spot.id,
          lot_id: spot.lot_id,
          is_available: spot.is_available,
        }));

        // Build reserved lot lookup
        const spotIdToLotId = {};
        for (const spot of this.spots) spotIdToLotId[spot.id] = spot.lot_id;

        const reservedLotIds = new Set();
        for (const reservation of this.reservedSpots) {
          const spotId = reservation.spot_id;
          const lotId = spotIdToLotId[spotId];
          if (lotId) reservedLotIds.add(lotId);
        }

        // Attach location info to each lot
        this.lots = data.lots.map((lot) => {
          const locationInfo = locationMap[lot.location_id] || {};
          return {
            id: lot.id,
            prime_location_name: lot.prime_location_name,
            price: lot.price,
            address: lot.address,
            pin_code: lot.pin_code,
            number_of_spots: lot.number_of_spots,
            hasReservedSpots: reservedLotIds.has(lot.id),
            location_name: locationInfo.name || 'Unknown',
            city: locationInfo.city || '',
          };
        });
      } catch (error) {
        toast.error('Error fetching parking lots or locations.', { position: 'top-center' });
        console.error(error);
      }
    },
    enableTooltips() {
      const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
      );
      tooltipTriggerList.forEach((tooltipTriggerEl) => {
        new bootstrap.Tooltip(tooltipTriggerEl);
      });
    },
    openViewModal(lot) {
      this.selectedLot = lot;
      this.showViewModal = true;
    },
    openEditModal(lot) {
      this.selectedLot = lot;
      this.showEditModal = true;
    },
    handleLotAdded() {
      this.showAddModal = false;
      this.getLots();
    },
    handleLotUpdated(updatedLot) {
      this.showEditModal = false;
      const index = this.lots.findIndex((lot) => lot.id === updatedLot.id);
      if (index !== -1) {
        this.lots.splice(index, 1, { ...updatedLot });
      }
    },
    async deleteLot(lotId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/delete_parking_lot/${lotId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
          credentials: 'include',
        });

        if (response.ok) {
          toast.success('Lot deleted successfully.', { position: 'top-center' });
          this.getLots();
        } else {
          toast.error('Failed to delete lot.', { position: 'top-center' });
        }
      } catch (error) {
        toast.error('Server error.', { position: 'top-center' });
        console.error(error);
      }
    },
  },
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
.admin-page {
  background: linear-gradient(135deg, var(--dark-bg) 0%, #001533 70%, var(--primary) 100%);
  min-height: 100vh;
  color: rgb(0, 0, 0);
}

/* 💎 Content */
.admin-content {
  flex: 1;
  padding-bottom: 100px;
}

/* 🧊 Glass Card */
.lot-card {
  background: rgba(13, 255, 0, 0.08);
  border: 4px solid rgba(32, 179, 22, 0.15);
  border-radius: 30px;
  backdrop-filter: blur(20px);
  transition: all 0.3s ease;
}
.lot-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 25px rgba(0, 224, 255, 0.3);
}

/* ✨ Buttons */
.btn-glow {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: #810174;
  border: none;
  border-radius: 50px;
  font-weight: 600;
  padding: 0.5rem 1.5rem;
  transition: 0.3s;
}
.btn-glow:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 15px rgba(0, 242, 254, 0.6);
}

.btn-outline-accent {
  border: 1px solid rgba(169, 0, 0, 0.7);
  color: rgba(0, 0, 0, 0.7);
}
.btn-outline-accent:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #000;
}

/* 🩵 Text helpers */
.text-accent {
  color: rgba(0, 63, 254, 0.399);
}
.text-light-50 {
  color: rgba(0, 0, 0, 0.7);
}

/* 🔄 Fade Animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
