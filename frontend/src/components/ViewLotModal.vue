<template>
  <div class="modal fade show d-block" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content glass-modal">
        <!-- Header -->
        <div class="modal-header border-0">
          <h5 class="modal-title text-accent fw-bold">🅿️ View Parking Place</h5>
          <button type="button" class="btn-close btn-close-white" @click="$emit('close')"></button>
        </div>

        <!-- Body -->
        <div class="modal-body text-light-50">
          <p class="fs-5 mb-3">
            <strong class="text-accent">Name:</strong> {{ lot.prime_location_name }}
          </p>
          <hr class="text-accent opacity-25" />

          <p class="mb-3 fw-semibold text-accent">Spots Status:</p>
          <div class="d-flex flex-wrap gap-2 justify-content-center">
            <div
              v-for="spot in spots.filter(s => s.lot_id === lot.id)"
              :key="spot.id"
              class="free-box rounded d-flex align-items-center justify-content-center"
              :class="spot.is_available ? 'available' : 'occupied'"
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              :title="getTooltipContent(spot)"
            >
              <img
                v-if="!spot.is_available"
                src="@/assets/images/occupied.png"
                alt="Occupied"
                class="occupied-icon"
              />
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="modal-footer border-0">
          <button type="button" class="btn btn-glow px-4" @click="$emit('close')">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as bootstrap from 'bootstrap';

export default {
  name: 'ViewLotModal',
  props: {
    lot: Object,
    spots: Array,
    reservedSpots: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    getTooltipContent(spot) {
      if (spot.is_available) {
        return `Spot ID: ${spot.id}\nStatus: Available`;
      } else {
        const reservation = this.reservedSpots.find(res => res.spot_id === spot.id);
        if (reservation) {
          const formattedTime = new Date(reservation.park_time).toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          });
          const price = typeof this.lot.price === 'number' ? this.lot.price.toFixed(2) : this.lot.price;
          return `Spot ID: ${spot.id}\nStatus: Occupied\nUser ID: ${reservation.user_id}\nParked Since: ${formattedTime}\nLot Price: ₹${price}`;
        }
        return `Spot ID: ${spot.id}\nStatus: Occupied (No details)`;
      }
    },
    initializeTooltips() {
      document.querySelectorAll('.tooltip').forEach(t => t.remove());
      const triggers = this.$el.querySelectorAll('[data-bs-toggle="tooltip"]');
      triggers.forEach(el => new bootstrap.Tooltip(el));
    }
  },
  mounted() {
    this.$nextTick(() => this.initializeTooltips());
  },
  updated() {
    this.$nextTick(() => this.initializeTooltips());
  },
  beforeUnmount() {
    const triggers = this.$el.querySelectorAll('[data-bs-toggle="tooltip"]');
    triggers.forEach(el => {
      const tooltip = bootstrap.Tooltip.getInstance(el);
      if (tooltip) tooltip.dispose();
    });
  }
};
</script>

<style scoped>
@import 'bootstrap-icons/font/bootstrap-icons.css';
@import 'animate.css';

:root {
  --primary: #4facfe;
  --secondary: #00f2fe;
  --dark-bg: #0a0f1f;
  --accent: #00d4ff;
}

/* Overlay background */
.modal {
  background-color: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
}

/* Glass modal */
.glass-modal {
  background: rgba(20, 25, 40, 0.9);
  border: 1px solid rgba(0, 224, 255, 0.2);
  border-radius: 16px;
  color: white;
  box-shadow: 0 0 30px rgba(0, 242, 254, 0.2);
  animation: fadeIn 0.4s ease;
}
@keyframes fadeIn {
  from {
    transform: translateY(15px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Modal header & footer */
.modal-header {
  background: transparent;
  border-bottom: none;
}
.modal-footer {
  border-top: none;
  justify-content: center;
}

/* Buttons */
.btn-glow {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: #fff;
  border: none;
  border-radius: 50px;
  transition: all 0.3s ease;
}
.btn-glow:hover {
  transform: translateY(-3px);
  box-shadow: 0 0 20px rgba(79, 172, 254, 0.7);
}

/* Free spot / occupied boxes */
.free-box {
  width: 45px;
  height: 45px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  transition: all 0.3s ease;
  cursor: pointer;
}

.free-box.available {
  background: rgba(0, 255, 128, 0.2);
  border-color: rgba(0, 255, 128, 0.5);
}
.free-box.available:hover {
  box-shadow: 0 0 12px rgba(0, 255, 128, 0.6);
}

.free-box.occupied {
  background: rgba(255, 0, 0, 0.2);
  border-color: rgba(255, 0, 0, 0.5);
}
.free-box.occupied:hover {
  box-shadow: 0 0 12px rgba(255, 77, 77, 0.6);
}

/* Occupied icon */
.occupied-icon {
  width: 32px;
  height: 32px;
  filter: drop-shadow(0 0 6px rgba(255, 0, 0, 0.4));
}

/* Tooltip styling */
.tooltip-inner {
  background: rgba(15, 20, 35, 0.9);
  border: 1px solid rgba(0, 224, 255, 0.2);
  white-space: pre-wrap;
  color: #fff;
  text-align: left;
  border-radius: 10px;
  box-shadow: 0 0 12px rgba(0, 242, 254, 0.3);
}
.bs-tooltip-top .tooltip-arrow::before {
  border-top-color: rgba(0, 242, 254, 0.4);
}

/* Text helpers */
.text-light-50 {
  color: rgba(255, 255, 255, 0.75);
}
.text-accent {
  color: var(--accent);
}
</style>
