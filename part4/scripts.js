// =====================================================
// HBnB - Frontend JavaScript
// =====================================================

// ===== Configuration =====
const API_URL = 'http://localhost:5000/api/v1';

// ===== Cookie Helpers =====
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value}; path=/; expires=${expires.toUTCString()}`;
}

function deleteCookie(name) {
    document.cookie = `${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;`;
}

// ===== Authentication Check =====
function isAuthenticated() {
    return !!getCookie('token');
}

function getToken() {
    return getCookie('token');
}

// ===== Helper Functions =====
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// =====================================================
// LOGIN PAGE (login.html)
// =====================================================
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorDiv = document.getElementById('error-message');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const res = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                const data = await res.json();

                if (res.ok) {
                    setCookie('token', data.access_token);
                    window.location.href = 'index.html';
                } else {
                    if (errorDiv) errorDiv.textContent = data.error || 'Login failed. Check your credentials.';
                    else alert('Login failed: ' + (data.error || 'Unknown error'));
                }
            } catch (err) {
                const msg = 'Network error. Is the backend running on port 5000?';
                if (errorDiv) errorDiv.textContent = msg;
                else alert(msg);
                console.error(err);
            }
        });
    }

    // =====================================================
    // INDEX PAGE (index.html) - Places List
    // =====================================================
    const placesList = document.getElementById('places-list');
    if (placesList) {
        // Show/hide login link based on authentication
        const loginLink = document.getElementById('login-link');
        if (loginLink) {
            if (isAuthenticated()) {
                loginLink.style.display = 'none';
            } else {
                loginLink.style.display = 'block';
            }
        }
        
        // Fetch and display places
        fetchPlaces();
        
        // Price filter
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', filterPlacesByPrice);
        }
    }

    // =====================================================
    // PLACE DETAILS PAGE (place.html)
    // =====================================================
    const placeId = new URLSearchParams(window.location.search).get('id');
    if (placeId && document.getElementById('place-details')) {
        loadPlaceDetails(placeId);
        
        // Show/hide add review section based on authentication
        const addReviewSection = document.getElementById('add-review-section');
        if (addReviewSection) {
            if (isAuthenticated()) {
                addReviewSection.style.display = 'block';
                const placeIdField = document.getElementById('place-id');
                if (placeIdField) placeIdField.value = placeId;
            } else {
                addReviewSection.style.display = 'none';
            }
        }
    }

    // =====================================================
    // ADD REVIEW PAGE (add_review.html) - Redirect if not authenticated
    // =====================================================
    const reviewForm = document.getElementById('review-form');
    if (reviewForm && window.location.pathname.includes('add_review.html')) {
        if (!isAuthenticated()) {
            window.location.href = 'index.html';
            return;
        }
        
        const reviewPlaceId = new URLSearchParams(window.location.search).get('id');
        const placeIdField = document.getElementById('place-id');
        if (placeIdField && reviewPlaceId) {
            placeIdField.value = reviewPlaceId;
        }
    }

    // =====================================================
    // REVIEW FORM SUBMISSION (works on place.html and add_review.html)
    // =====================================================
    if (reviewForm) {
        reviewForm.addEventListener('submit', submitReview);
    }
});

// =====================================================
// PLACES FUNCTIONS
// =====================================================
async function fetchPlaces() {
    try {
        const token = getToken();
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const res = await fetch(`${API_URL}/places`, { headers });
        if (!res.ok) throw new Error('Failed to fetch places');
        
        const places = await res.json();
        displayPlaces(places);
    } catch (err) {
        console.error(err);
        const container = document.getElementById('places-list');
        if (container) {
            container.innerHTML = '<p class="error">Error loading places. Make sure the API server is running.</p>';
        }
    }
}

function displayPlaces(places) {
    const container = document.getElementById('places-list');
    if (!container) return;
    container.innerHTML = '';

    if (!places || places.length === 0) {
        container.innerHTML = '<p>No places available.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.setAttribute('data-price', place.price);
        card.innerHTML = `
            <h3>${escapeHtml(place.title)}</h3>
            <p class="price">$${place.price} / night</p>
            <button class="details-button" data-id="${place.id}">View Details</button>
        `;
        
        const button = card.querySelector('.details-button');
        button.addEventListener('click', () => {
            window.location.href = `place.html?id=${place.id}`;
        });
        
        container.appendChild(card);
    });
}

function filterPlacesByPrice() {
    const maxPrice = document.getElementById('price-filter').value;
    const cards = document.querySelectorAll('.place-card');
    
    cards.forEach(card => {
        const price = parseFloat(card.getAttribute('data-price'));
        if (maxPrice === 'all' || price <= parseFloat(maxPrice)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// =====================================================
// PLACE DETAILS FUNCTIONS
// =====================================================
async function loadPlaceDetails(placeId) {
    try {
        const res = await fetch(`${API_URL}/places/${placeId}`);
        if (!res.ok) throw new Error('Place not found');
        
        const place = await res.json();
        displayPlaceDetails(place);
        
        // Load reviews separately
        await loadReviews(placeId);
    } catch (err) {
        console.error(err);
        const container = document.getElementById('place-details');
        if (container) {
            container.innerHTML = '<p class="error">Error loading place details. Make sure the backend is running.</p>';
        }
    }
}

function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    if (!container) return;
    
    container.innerHTML = `
        <h2>${escapeHtml(place.title)}</h2>
        <p class="description">${escapeHtml(place.description || 'No description available.')}</p>
        <p class="price"><strong>Price:</strong> $${place.price} / night</p>
        <p class="location"><strong>Location:</strong> ${place.latitude}, ${place.longitude}</p>
        <div class="owner-info">
            <strong>Host:</strong> ${escapeHtml(place.owner?.first_name || 'Unknown')} ${escapeHtml(place.owner?.last_name || '')}
        </div>
        <div class="amenities">
            <strong>Amenities:</strong>
            <ul>
                ${place.amenities?.map(a => `<li>${escapeHtml(a.name)}</li>`).join('') || '<li>No amenities listed</li>'}
            </ul>
        </div>
    `;
}

async function loadReviews(placeId) {
    try {
        const res = await fetch(`${API_URL}/reviews/places/${placeId}/reviews`);
        const reviews = await res.json();
        displayReviews(reviews);
    } catch (err) {
        console.error(err);
        const container = document.getElementById('reviews-list');
        if (container) {
            container.innerHTML = '<p>Unable to load reviews.</p>';
        }
    }
}

function displayReviews(reviews) {
    const container = document.getElementById('reviews-list');
    if (!container) return;
    
    if (!reviews || reviews.length === 0) {
        container.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
        return;
    }
    
    container.innerHTML = reviews.map(review => `
        <div class="review-card">
            <p class="review-text">"${escapeHtml(review.text)}"</p>
            <p class="review-rating">⭐ ${review.rating}/5</p>
            <p class="review-author">- ${escapeHtml(review.user?.first_name || 'Anonymous')}</p>
        </div>
    `).join('');
}

// =====================================================
// REVIEW SUBMISSION
// =====================================================
async function submitReview(e) {
    e.preventDefault();
    
    const token = getToken();
    if (!token) {
        alert('You must be logged in to submit a review.');
        window.location.href = 'login.html';
        return;
    }
    
    // Get place_id from hidden field or URL
    let placeId = document.getElementById('place-id')?.value;
    if (!placeId) {
        placeId = new URLSearchParams(window.location.search).get('id');
    }
    
    const reviewText = document.getElementById('review-text').value;
    const rating = parseInt(document.getElementById('rating').value);
    
    if (!reviewText || !rating) {
        alert('Please fill in all fields.');
        return;
    }
    
    try {
        const res = await fetch(`${API_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: rating,
                place_id: placeId
            })
        });
        
        if (res.ok) {
            alert('Review submitted successfully!');
            // Clear form
            document.getElementById('review-text').value = '';
            document.getElementById('rating').value = '5';
            
            // If on place.html, reload reviews
            if (document.getElementById('reviews-list')) {
                await loadReviews(placeId);
            } else {
                // If on add_review.html, redirect to place page
                window.location.href = `place.html?id=${placeId}`;
            }
        } else {
            const error = await res.json();
            alert(`Failed to submit review: ${error.error || 'Unknown error'}`);
        }
    } catch (err) {
        console.error(err);
        alert('Network error. Could not submit review.');
    }
}

// =====================================================
// LOGOUT FUNCTION (for admin.html or any page)
// =====================================================
function logout() {
    deleteCookie('token');
    window.location.href = 'index.html';
}

// =====================================================
// ADMIN PAGE (admin.html) - Loaded separately in admin.js
// But these helper functions are available
// =====================================================
async function adminFetchUsers() {
    const token = getToken();
    if (!token) return [];
    
    try {
        const res = await fetch(`${API_URL}/users/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error('Failed to fetch users');
        return await res.json();
    } catch (err) {
        console.error(err);
        return [];
    }
}

async function adminFetchPlaces() {
    const token = getToken();
    if (!token) return [];
    
    try {
        const res = await fetch(`${API_URL}/places/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error('Failed to fetch places');
        return await res.json();
    } catch (err) {
        console.error(err);
        return [];
    }
}

async function adminDeleteUser(userId) {
    const token = getToken();
    if (!token || !confirm('Delete this user? This will also delete their places and reviews.')) return false;
    
    try {
        const res = await fetch(`${API_URL}/users/${userId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            alert('User deleted successfully');
            return true;
        } else {
            const error = await res.json();
            alert(`Failed: ${error.error}`);
            return false;
        }
    } catch (err) {
        console.error(err);
        alert('Network error');
        return false;
    }
}

async function adminDeletePlace(placeId) {
    const token = getToken();
    if (!token || !confirm('Delete this place?')) return false;
    
    try {
        const res = await fetch(`${API_URL}/places/${placeId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            alert('Place deleted successfully');
            return true;
        } else {
            const error = await res.json();
            alert(`Failed: ${error.error}`);
            return false;
        }
    } catch (err) {
        console.error(err);
        alert('Network error');
        return false;
    }
}

async function adminDeleteAmenity(amenityId) {
    const token = getToken();
    if (!token || !confirm('Delete this amenity?')) return false;
    
    try {
        const res = await fetch(`${API_URL}/amenities/${amenityId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            alert('Amenity deleted successfully');
            return true;
        } else {
            const error = await res.json();
            alert(`Failed: ${error.error}`);
            return false;
        }
    } catch (err) {
        console.error(err);
        alert('Network error');
        return false;
    }
}

async function adminCreateAmenity(name, description) {
    const token = getToken();
    if (!token) return false;
    
    try {
        const res = await fetch(`${API_URL}/amenities/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ name, description: description || '' })
        });
        if (res.ok) {
            alert('Amenity created successfully');
            return true;
        } else {
            const error = await res.json();
            alert(`Failed: ${error.error}`);
            return false;
        }
    } catch (err) {
        console.error(err);
        alert('Network error');
        return false;
    }
}
