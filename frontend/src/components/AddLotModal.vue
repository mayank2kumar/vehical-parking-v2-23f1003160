<template>
  <div class="modal fade show d-block" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content glass-modal animate__animated animate__fadeInUp">
        <form @submit.prevent="submitLot">
          <div class="modal-header border-0">
            <h5 class="modal-title text-accent fw-bold">➕ Add Parking Lot</h5>
            <button type="button" class="btn-close btn-close-white" @click="$emit('close')"></button>
          </div>

          <div class="modal-body row g-3">
            <div class="col-md-6">
              <label class="form-label text-light-50">Prime Location Name</label>
              <input
                v-model="form.prime_location_name"
                type="text"
                class="form-control custom-input"
                placeholder="Enter lot name"
                required
              />
            </div>

            <div class="col-md-6 d-flex align-items-end">
              <div class="w-100 me-2">
                <label class="form-label text-light-50">Select Location</label>
                <select
                  v-model="form.location_id"
                  class="form-select custom-input"
                  required
                >
                  <option disabled value="">Select a Location</option>
                  <option v-for="loc in locations" :key="loc.id" :value="loc.id">
                    {{ loc.name }} ({{ loc.city }})
                  </option>
                </select>
              </div>

              <!-- 🗑️ Delete button -->
              <button
                type="button"
                class="btn btn-outline-danger delete-loc-btn mb-1"
                title="Delete selected location"
                :disabled="!form.location_id"
                @click="confirmDeleteLocation(form.location_id)"
              >
                <i class="bi bi-trash3"></i>
              </button>
            </div>

            <div class="col-md-6">
              <label class="form-label text-light-50">Price (per hour)</label>
              <input
                v-model="form.price"
                type="number"
                class="form-control custom-input"
                placeholder="e.g. 50"
                required
                min="0"
              />
            </div>

            <div class="col-md-6">
              <label class="form-label text-light-50">Number of Spots</label>
              <input
                v-model="form.number_of_spots"
                type="number"
                class="form-control custom-input"
                placeholder="e.g. 20"
                required
                min="1"
              />
            </div>

            <div class="col-md-12">
              <label class="form-label text-light-50">Address</label>
              <input
                v-model="form.address"
                type="text"
                class="form-control custom-input"
                placeholder="Enter complete address"
                required
              />
            </div>

            <div class="col-md-6">
              <label class="form-label text-light-50">Pin Code</label>
              <input
                v-model="form.pin_code"
                type="text"
                class="form-control custom-input"
                placeholder="6-digit pin"
                required
                pattern="[0-9]{6}"
                title="Pin code must be 6 digits"
              />
            </div>
          </div>

          <div class="modal-footer border-0 d-flex justify-content-end">
            <button type="button" class="btn btn-secondary px-4" @click="$emit('close')">Cancel</button>
            <button type="submit" class="btn btn-glow px-4">Add Lot</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { toast } from 'vue3-toastify';

export default {
  name: 'AddLotModal',
  data() {
    return {
      form: {
        prime_location_name: '',
        price: '',
        address: '',
        pin_code: '',
        number_of_spots: '',
        location_id: '',
      },
      locations: [],
    };
  },
  async mounted() {
    try {
      const res = await fetch('http://127.0.0.1:5000/get_locations', {
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
        },
      });
      const data = await res.json();
      if (res.ok) {
        this.locations = data.locations;
      } else {
        toast.error(data.message || 'Failed to fetch locations');
      }
    } catch (err) {
      toast.error('Error fetching locations');
    }
  },
  methods: {
        async fetchLocations() {
      try {
        const res = await fetch('http://127.0.0.1:5000/get_locations', {
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
        });
        const data = await res.json();
        if (res.ok) this.locations = data.locations;
        else toast.error(data.message || 'Failed to fetch locations');
      } catch (err) {
        toast.error('Error fetching locations');
      }
    },

      async confirmDeleteLocation(id) {
        try {
          const res = await fetch(`http://127.0.0.1:5000/delete_location/${id}`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              Authorization: 'Bearer ' + localStorage.getItem('access_token'),
            },
          });
          const data = await res.json();
          if (res.ok) {
            toast.success(data.message || 'Location deleted successfully');
            this.form.location_id = ''; // reset select
            this.fetchLocations(); // refresh dropdown
          } else {
            toast.error(data.message || 'Failed to delete location');
          }
        } catch (err) {
          toast.error('Server error deleting location');
        }
      },

    async submitLot() {
      try {
        const response = await fetch('http://127.0.0.1:5000/add_parking_lot', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          },
          body: JSON.stringify(this.form),
        });

        const result = await response.json();
        if (response.ok) {
          toast.success(result.message || 'Lot added successfully');
          this.$emit('lot-added');
        } else {
          toast.error(result.message || 'Failed to add lot');
        }
      } catch (err) {
        toast.error('Server error');
      }
    },
  },
};
</script>

@import 'animate.css';
@import 'bootstrap-icons/font/bootstrap-icons.css';

:root {
  --primary: #00b4db;
  --secondary: #0083b0;
  --accent: #00fff0;
  --dark-bg: #0b132b;
  --light-text: rgba(255, 255, 255, 0.85);
}

/* 🔲 Overlay */
.modal {
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(10px);
}

/* 🧊 Modal Container */
.glass-modal {
  background: linear-gradient(145deg, rgba(15, 20, 40, 0.92), rgba(10, 15, 31, 0.88));
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 24px;
  color: var(--light-text);
  box-shadow: 0 0 40px rgba(0, 255, 255, 0.15);
  overflow: hidden;
  animation: modalPop 0.4s ease-out;
}

@keyframes modalPop {
  from {
    transform: translateY(30px) scale(0.98);
    opacity: 0;
  }
  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

/* 🪩 Header */
.modal-header {
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  border-top-left-radius: 24px;
  border-top-right-radius: 24px;
  padding: 1rem 1.5rem;
}

.modal-title {
  font-size: 1.3rem;
  color: white;
  letter-spacing: 0.5px;
}

.btn-close {
  filter: brightness(0) invert(1);
  opacity: 0.8;
}
.btn-close:hover {
  opacity: 1;
}

/* ✍️ Inputs & Select */
.custom-input {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 12px;
  color: var(--light-text);
  transition: all 0.3s ease;
  padding: 0.6rem 0.75rem;
}

.custom-input::placeholder {
  color: rgba(255, 255, 255, 0.55);
}

.custom-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 14px rgba(0, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.12);
  outline: none;
}

/* 💡 Labels */
.form-label {
  font-weight: 500;
  font-size: 0.95rem;
  color: var(--accent);
}

/* ⚙️ Buttons */
.btn-glow {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: white;
  border: none;
  border-radius: 50px;
  padding: 0.5rem 1.6rem;
  font-weight: 600;
  transition: 0.3s ease;
  letter-spacing: 0.3px;
}

.btn-glow:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 18px rgba(0, 255, 255, 0.5);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 50px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.25);
  color: #fff;
  transform: translateY(-1px);
}

/* 📄 Modal Footer */
.modal-footer {
  background: rgba(255, 255, 255, 0.05);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  border-bottom-left-radius: 24px;
  border-bottom-right-radius: 24px;
}

/* ✨ Typography */
.text-accent {
  color: var(--accent);
}
.text-light-50 {
  color: rgba(255, 255, 255, 0.75);
}

/* 🌈 Hover glow for form controls */
.custom-input:hover {
  border-color: var(--primary);
  box-shadow: 0 0 10px rgba(0, 183, 255, 0.25);
}

