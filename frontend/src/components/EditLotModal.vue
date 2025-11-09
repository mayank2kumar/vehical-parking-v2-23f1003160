<template>
  <div class="modal fade show d-block" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content glass-modal animate__animated animate__fadeInUp">
        <div class="modal-header border-0">
          <h5 class="modal-title text-accent fw-bold">
            ✏️ Edit Parking Place (ID: {{ editedLot.id }})
          </h5>
          <button type="button" class="btn-close btn-close-white" @click="$emit('close')" aria-label="Close"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="submitEdit">
            <div class="mb-3">
              <label for="primeLocationName" class="form-label text-light-50">Prime Location Name</label>
              <input
                type="text"
                class="form-control custom-input"
                id="primeLocationName"
                v-model="editedLot.prime_location_name"
                required
              />
            </div>

            <div class="mb-3">
              <label for="price" class="form-label text-light-50">Price (per hour)</label>
              <input
                type="number"
                class="form-control custom-input"
                id="price"
                v-model.number="editedLot.price"
                min="0"
                required
              />
            </div>

            <div class="mb-3">
              <label for="address" class="form-label text-light-50">Address</label>
              <input
                type="text"
                class="form-control custom-input"
                id="address"
                v-model="editedLot.address"
                required
              />
            </div>

            <div class="mb-3">
              <label for="pinCode" class="form-label text-light-50">Pin Code</label>
              <input
                type="text"
                class="form-control custom-input"
                id="pinCode"
                v-model="editedLot.pin_code"
                required
                pattern="[0-9]{6}"
                title="Pin code must be 6 digits"
              />
            </div>

            <div class="mb-3">
              <label for="numberOfSpots" class="form-label text-light-50">Number of Spots</label>
              <input
                type="number"
                class="form-control custom-input"
                id="numberOfSpots"
                v-model.number="editedLot.number_of_spots"
                min="1"
                required
              />
            </div>

            <div class="modal-footer border-0 d-flex justify-content-end">
              <button type="button" class="btn btn-secondary px-4" @click="$emit('close')">Cancel</button>
              <button type="submit" class="btn btn-glow px-4">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { toast } from 'vue3-toastify';

export default {
  name: 'EditLotModal',
  props: {
    lot: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      editedLot: { ...this.lot },
    };
  },
  methods: {
    async submitEdit() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/update_parking_lot/${this.editedLot.id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
          body: JSON.stringify({
            prime_location_name: this.editedLot.prime_location_name,
            price: this.editedLot.price,
            address: this.editedLot.address,
            pin_code: this.editedLot.pin_code,
            number_of_spots: this.editedLot.number_of_spots,
          }),
        });

        if (response.ok) {
          toast.success('Parking lot updated successfully!', { position: 'top-center' });
          this.$emit('lot-updated', this.editedLot);
        } else {
          const errorData = await response.json();
          toast.error(errorData.message || 'Failed to update parking lot.', { position: 'top-center' });
        }
      } catch (error) {
        toast.error('Server error during update.', { position: 'top-center' });
        console.error('Error updating parking lot:', error);
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

/* Overlay */
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

/* Inputs */
.custom-input {
  background: rgba(255, 255, 255, 0.08);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  transition: all 0.3s ease;
}
.custom-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}
.custom-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 12px rgba(0, 224, 255, 0.4);
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
.btn-secondary {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  transition: 0.3s;
}
.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.25);
}

/* Text helpers */
.text-accent {
  color: var(--accent);
}
.text-light-50 {
  color: rgba(255, 255, 255, 0.7);
}
</style>
