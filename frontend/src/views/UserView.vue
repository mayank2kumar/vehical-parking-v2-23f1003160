<template>
    <NavBar />
    <div class="container py-5">
        <br>    </br>
        <div class="text-center mb-5">
            <h2 class="fw-bold">User Dashboard</h2>
        </div>

        <div v-if="userReservations.length > 0" class="mb-5">
            <div class="card shadow border-0">
                <div class="card-header bg-dark text-white text-center">
                    <h4 class="mb-0">Your Reservations</h4>
                </div>
                <div class="card-body p-4">
                    <div class="table-responsive">
                        <table class="table table-striped align-middle mb-9">
                            <thead class="table-light">
                                <tr>
                                    <th scope="col" class="text-center">Lot Name</th>
                                    <th scope="col" class="text-center">Address</th>
                                    <th scope="col" class="text-center">Spot ID</th>
                                    <th scope="col" class="text-center">Park Time</th>
                                    <th scope="col" class="text-center">Exit Time</th>
                                    <th scope="col" class="text-center">Total Cost</th>
                                    <th scope="col" class="text-center">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="reservation in userReservations" :key="reservation.id">
                                    <td class="text-center">{{ reservation.lot_name }}</td>
                                    <!-- UPDATED: Use reservation.lot_address here -->
                                    <td class="text-center">{{ reservation.lot_address }}</td>
                                    <td class="text-center">{{ reservation.spot_id }}</td>
                                    <td class="text-center">{{ formatDateTime(reservation.park_time) }}</td>
                                    <td class="text-center">
                                        <span v-if="reservation.exit_time">{{ formatDateTime(reservation.exit_time)
                                        }}</span>
                                        <span v-else class="text-warning">Ongoing</span>
                                    </td>
                                    <td class="text-center">
                                        <span v-if="reservation.total_cost !== null">₹{{
                                            reservation.total_cost.toFixed(2) }}</span>
                                        <span v-else class="text-primary">Calculating</span>
                                    </td>
                                    <td v-if="reservation.exit_time" class="text-center">
                                        <button class="btn btn-sm btn-danger" disabled>Released</button>
                                    </td>
                                    <td v-else class="text-center">
                                        <button class="btn btn-sm btn-primary"
                                            @click="releaseSpot(reservation.id)">Release</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <div v-else class="alert alert-info text-center" role="alert">
            You currently have no reservations.
        </div>
        <hr class="my-5" />
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import { toast } from 'vue3-toastify';

export default {
    name: 'UserView',
    components: {
        NavBar,
    },
    data() {
        return {
            username: '',
            userReservations: []
        };
    },
    async mounted() {
        const token = localStorage.getItem('access_token');
        if (!token) {
            toast.error('No access token found.', { position: 'top-center' });
            this.$router.push('/login');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/user_dashboard', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                toast.error('Access Denied. Logging out.', {
                    position: 'top-center',
                    onClose: () => {
                        // logout user
                        this.logout();
                    },
                });
                return;
            }

            await this.getUserInfo();
            if (this.username) {
                await this.getUserReservations();
            } else {
                toast.error('Failed to retrieve user data. Please log in again.', { position: 'top-center' });
                localStorage.removeItem('access_token'); // Clear potentially bad token
                this.$router.push('/login');
            }
        } catch (error) {
            toast.error('Server error or network issue loading dashboard.', { position: 'top-center' });
            console.error("Dashboard mounted error:", error);
            localStorage.removeItem('access_token');
            this.$router.push('/login');
        }
    },
    methods: {
        async logout() {
            try {
                const token = localStorage.getItem('access_token');
                if (!token) {
                    toast.error('No access token found.', { position: 'top-center' });
                    return;
                }
                const res = await fetch('http://127.0.0.1:5000/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                if (!res.ok) {
                    toast.error('Failed to log out.', { position: 'top-center' });
                    return;
                }
                localStorage.removeItem('access_token');
                toast.success('Logged out successfully.', { position: 'top-center', onClose: () => this.$router.push('/login') });
            } catch (error) {
                console.error("Logout error:", error);
                toast.error('Failed to log out.', { position: 'top-center' });
            }
        },
        async getUserReservations() {
            try {
                if (!this.username) {
                    console.warn("Username not available to fetch reservations.");
                    return;
                }
                const res = await fetch(`http://127.0.0.1:5000/get_user_reservations/${this.username}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                    },
                });

                if (!res.ok) {
                    const errorData = await res.json();
                    toast.error(errorData.message || 'Failed to fetch reservations.', { position: 'top-center' });
                    if (res.status === 401 || res.status === 403) {
                        localStorage.removeItem('access_token');
                        this.$router.push('/login');
                    }
                    return;
                }

                const data = await res.json();
                this.userReservations = data.reservations;

                // Create lookup maps for efficient access
                const spotMap = new Map();
                if (data.spots && Array.isArray(data.spots)) {
                    for (const spot of data.spots) {
                        spotMap.set(spot.id, spot);
                    }
                } else {
                    console.warn("Backend response does not contain a 'spots' array or it's empty. Cannot map spots to lots.");
                }

                const lotMap = new Map();
                if (data.lots && Array.isArray(data.lots)) {
                    for (const lot of data.lots) {
                        lotMap.set(lot.id, lot);
                    }
                } else {
                    console.warn("Backend response does not contain a 'lots' array or it's empty.");
                }

                // Location map is no longer strictly needed for display in the 'Location' column,
                // but keeping it in case it's used elsewhere or for future features.
                const locationMap = new Map();
                if (data.locations && Array.isArray(data.locations)) {
                    for (const location of data.locations) {
                        locationMap.set(location.id, location);
                    }
                } else {
                    console.warn("Backend response does not contain a 'locations' array or it's empty.");
                }

                // Add lot_name and lot_address to each reservation
                for (const reservation of this.userReservations) {
                    let lotInfoFound = false; // Flag to check if lot info was found

                    const spot = spotMap.get(reservation.spot_id);

                    if (spot && spot.lot_id) {
                        const lot = lotMap.get(spot.lot_id); // Get the full lot object using the lot_id from the spot

                        if (lot) {
                            reservation.lot_name = lot.prime_location_name;
                            reservation.lot_address = lot.address; // Assign the lot's address
                            lotInfoFound = true;
                            // Optionally, you can still get location_name if needed for other purposes
                            // const location = locationMap.get(lot.location_id);
                            // if (location) {
                            //     reservation.location_name = location.name;
                            // }
                        }
                    }

                    // Fallback for cases where lot info couldn't be found
                    if (!lotInfoFound) {
                        reservation.lot_name = 'Unknown Lot';
                        reservation.lot_address = 'N/A'; // Fallback for address
                        // reservation.location_name = 'Unknown Location'; // If you still need this property
                    }
                }

                // Add these console.logs back to verify your data at each step
                console.log("Processed User Reservations:", this.userReservations);
                console.log("Spot Map:", spotMap);
                console.log("Lot Map:", lotMap);
                console.log("Location Map:", locationMap);


            } catch (error) {
                console.error("Error fetching user reservations:", error);
                toast.error('Network error fetching reservations.', { position: 'top-center' });
            }
        },
        async getUserInfo() {
            try {
                const token = localStorage.getItem('access_token');
                if (!token) {
                    console.warn("No token to fetch user info.");
                    return;
                }
                const res = await fetch('http://127.0.0.1:5000/get_user_info', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token,
                    },
                });

                if (!res.ok) {
                    const errorData = await res.json();
                    toast.error(errorData.message || 'Failed to fetch user info.', { position: 'top-center' });
                    // Handle specific errors like 401/403:
                    if (res.status === 401 || res.status === 403) {
                        localStorage.removeItem('access_token');
                        this.$router.push('/login');
                    }
                    return;
                }

                const data = await res.json();
                if (data.user && data.user.username) {
                    this.username = data.user.username;
                } else {
                    console.warn("User info received but username is missing:", data);
                    toast.error('User information incomplete.', { position: 'top-center' });
                    localStorage.removeItem('access_token'); // Clear potentially bad token
                    this.$router.push('/login');
                }
            } catch (error) {
                console.error("Error fetching user info:", error);
                toast.error('Network error fetching user details.', { position: 'top-center' });
            }
        },
        async releaseSpot(reservationId) {
            try {
                const token = localStorage.getItem('access_token');
                const res = await fetch(`http://127.0.0.1:5000/release_parking/${reservationId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token,
                    },
                    body: JSON.stringify({}),
                });
                if (!res.ok) {
                    // It's good practice to parse the error response if available
                    const errorData = await res.json();
                    toast.error(errorData.message || 'Unauthorized or server error.', { position: 'top-center' });
                    return;
                }
                toast.success('Spot released successfully.', { position: 'top-center' });
                // Refresh reservations after releasing a spot
                this.getUserReservations();
            } catch (error) {
                console.error("Error releasing spot:", error);
                toast.error('Network error releasing spot. Try again later.', { position: 'top-center' });
            }
        },
        formatDateTime(datetimeStr) {
            if (!datetimeStr) return '';
            const options = {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                hour12: true,
            };
            return new Date(datetimeStr).toLocaleString(undefined, options);
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
  --text-light: #e5e5e5;
  --text-muted: #a0a0a0;
}

/* 🌌 Page Base */
.container {
  background: linear-gradient(160deg, var(--dark-bg) 0%, #001122 80%);
  min-height: 100vh;
  color: var(--text-light);
  border-radius: 12px;
  padding: 2rem;
  animation: fadeIn 1s ease;
}

/* 🎯 Heading */
h2.fw-bold {
  color: var(--accent);
  text-shadow: 0 0 15px rgba(0, 238, 255, 0.4);
  letter-spacing: 1px;
  margin-bottom: 1.5rem;
}

/* 🧊 Card */
.card {
  background: rgba(152, 191, 203, 0.77);
  border: 1px solid rgba(0, 238, 255, 0.15);
  border-radius: 16px;
  backdrop-filter: blur(14px);
  transition: all 0.3s ease;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0 25px rgba(0, 238, 255, 0.25);
}

/* 💡 Card Header */
.card-header {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border: none;
  border-radius: 16px 16px 0 0;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* 📊 Table */
.table {
  color: var(--text-light);
}
.table th {
  background-color: rgba(255, 255, 255, 0.05);
  color: var(--accent);
  border-bottom: 1px solid rgba(0, 238, 255, 0.2);
}
.table-striped tbody tr:nth-of-type(odd) {
  background-color: rgba(255, 255, 255, 0.03);
}
.table-striped tbody tr:hover {
  background-color: rgba(0, 238, 255, 0.08);
  transition: background 0.3s ease;
}

/* 🔘 Buttons */
.btn {
  border-radius: 25px;
  font-weight: 500;
  transition: all 0.3s ease;
}
.btn-primary {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border: none;
  color: rgb(96, 197, 45);
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 15px rgba(0, 238, 255, 0.6);
  background: linear-gradient(135deg, var(--secondary), var(--primary));
}
.btn-danger {
  background: rgba(255, 77, 77, 0.85);
  border: none;
}
.btn-danger:hover {
  box-shadow: 0 0 10px rgba(255, 77, 77, 0.6);
}

/* 💬 Alert */
.alert {
  background: rgba(0, 238, 255, 0.1);
  border: 1px solid rgba(0, 238, 255, 0.25);
  color: var(--text-light);
  border-radius: 12px;
  font-weight: 500;
}

/* ✨ Texts */
.text-accent {
  color: var(--accent);
}
.text-warning {
  color: #ffc107 !important;
}
.text-muted {
  color: var(--text-muted);
}

/* 📱 Responsive */
@media (max-width: 768px) {
  .table td,
  .table th {
    font-size: 0.85rem;
  }
}

/* 🎞️ Animation */
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
</style>