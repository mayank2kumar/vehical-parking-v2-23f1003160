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

            <div class="col-md-6">
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
