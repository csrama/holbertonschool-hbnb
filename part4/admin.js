// ========== admin.js ==========
// Admin Control Panel

// ===== Admin Permissions Verification =====
async function checkAdmin() {
    const token = getToken();
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }

    try {
// Decrypt JWT to verify is_admin
        const payload = JSON.parse(atob(token.split('.')[1]));
        if (!payload.is_admin) {
            alert('Access denied. Admin privileges required.');
            window.location.href = 'index.html';
            return false;
        }
        return true;
    } catch (err) {
        console.error(err);
        window.location.href = 'login.html';
        return false;
    }
}

// ===== Loading Control Panel Data =====
async function loadDashboard() {
    const token = getToken();

    try {
// Retrieve all users
        const usersRes = await fetch(`${API_URL}/users/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const users = await usersRes.json();
        displayUsers(users);

// Retrieve all places
        const placesRes = await fetch(`${API_URL}/places/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const places = await placesRes.json();
        displayPlaces(places);

        // Retrieve all Amenities (Amenities)
        const amenitiesRes = await fetch(`${API_URL}/amenities/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const amenities = await amenitiesRes.json();
        displayAmenities(amenities);

    } catch (err) {
        console.error(err);
        const container = document.getElementById('dashboard-content');
        if (container) {
            container.innerHTML = '<p class="error">Error loading dashboard. Make sure the server is running.</p>';
        }
    }
}

// ===== View Users Table =====
function displayUsers(users) {
    const container = document.getElementById('users-list');
    if (!container) return;

    if (!users || users.length === 0) {
        container.innerHTML = '<tr><td colspan="5">No users found</td></tr>';
        return;
    }

    container.innerHTML = users.map(user => `
        <tr>
            <td>${escapeHtml(user.id.substring(0, 8))}...</td>
            <td>${escapeHtml(user.first_name)} ${escapeHtml(user.last_name)}</td>
            <td>${escapeHtml(user.email)}</td>
            <td>${user.is_admin ? '✅ Admin' : '👤 User'}</td>
            <td>
                <button class="btn-delete" onclick="deleteUser('${user.id}')">Delete</button>
            </td>
        </tr>
    `).join('');
}

// ===== Show Table of Places =====
function displayPlaces(places) {
    const container = document.getElementById('admin-places-list');
    if (!container) return;

    if (!places || places.length === 0) {
        container.innerHTML = '<tr><td colspan="4">No places found</td></tr>';
        return;
    }

    container.innerHTML = places.map(place => `
        <tr>
            <td>${escapeHtml(place.title)}</td>
            <td>$${place.price}</td>
            <td>${escapeHtml(place.owner?.first_name || 'Unknown')}</td>
            <td>
                <button class="btn-delete" onclick="deletePlace('${place.id}')">Delete</button>
            </td>
        </tr>
    `).join('');
}

// ===== View amenities Schedule =====
function displayAmenities(amenities) {
    const container = document.getElementById('amenities-list');
    if (!container) return;

    if (!amenities || amenities.length === 0) {
        container.innerHTML = '<tr><td colspan="3">No amenities found</td></tr>';
        return;
    }

    container.innerHTML = amenities.map(amenity => `
        <tr>
            <td>${escapeHtml(amenity.id.substring(0, 8))}...</td>
            <td>${escapeHtml(amenity.name)}</td>
            <td>
                <button class="btn-edit" onclick="editAmenity('${amenity.id}')">Edit</button>
                <button class="btn-delete" onclick="deleteAmenity('${amenity.id}')">Delete</button>
            </td>
        </tr>
    `).join('');
}

// ===== Delete Functions =====
async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user? This will also delete all their places and reviews.')) return;

    const token = getToken();
    try {
        const res = await fetch(`${API_URL}/users/${userId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok) {
            alert('User deleted successfully');
            loadDashboard();
        } else {
            const error = await res.json();
            alert(`Failed: ${error.error}`);
        }
    } catch (err) {
        console.error(err);
        alert('Network error');
    }
}

async function deletePlace(placeId) {
    if (!confirm('Are you sure you want to delete this place?')) return;

    const token = getToken();
    try {
        const res = await fetch(`${API_URL}/places/${placeId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok) {
            alert('Place deleted successfully');
            loadDashboard();
        } else {
            const error = await res.json();
            alert(`Failed: ${error.error}`);
        }
    } catch (err) {
        console.error(err);
        alert('Network error');
    }
}

async function deleteAmenity(amenityId) {
    if (!confirm('Are you sure you want to delete this amenity?')) return;

    const token = getToken();
    try {
        const res = await fetch(`${API_URL}/amenities/${amenityId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok) {
            alert('Amenity deleted successfully');
            loadDashboard();
        } else {
            const error = await res.json();
            alert(`Failed: ${error.error}`);
        }
    } catch (err) {
        console.error(err);
        alert('Network error');
    }
}

// ===== Creating new amenity =====
document.addEventListener('DOMContentLoaded', () => {
    const createForm = document.getElementById('create-amenity-form');
    if (createForm) {
        createForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const token = getToken();
            const name = document.getElementById('amenity-name')?.value;
            const description = document.getElementById('amenity-description')?.value || '';

            try {
                const res = await fetch(`${API_URL}/amenities/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ name, description })
                });

                if (res.ok) {
                    alert('Amenity created successfully');
                    createForm.reset();
                    loadDashboard();
                } else {
                    const error = await res.json();
                    alert(`Failed: ${error.error}`);
                }
            } catch (err) {
                console.error(err);
                alert('Network error');
            }
        });
    }
});

// ===== Modification functions (we can expand them later) =====
function editUser(userId) {
    alert(`Edit user ${userId} - Feature to be implemented`);
}

function editAmenity(amenityId) {
    alert(`Edit amenity ${amenityId} - Feature to be implemented`);
}

// ===== Setting up the admin page =====
document.addEventListener('DOMContentLoaded', async () => {
    const isAdmin = await checkAdmin();
    if (isAdmin) {
        loadDashboard();
    }
});
