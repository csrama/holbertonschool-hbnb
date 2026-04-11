// ===== Configuration =====
const API_URL = 'http://127.0.0.1:5000/api/v1';

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

// ===== LOGIN =====
function initLoginForm() {
    const form = document.getElementById('login-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const errorDiv = document.getElementById('error-message'); // ✅ FIXED

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
                if (errorDiv) {
                    errorDiv.style.display = 'block';
                    errorDiv.textContent = data.error || 'Login failed';
                } else {
                    alert('Login failed');
                }
            }
        } catch (err) {
            const msg = 'Network error. Make sure backend is running on port 5000';
            if (errorDiv) {
                errorDiv.style.display = 'block';
                errorDiv.textContent = msg;
            } else {
                alert(msg);
            }
        }
    });
}

// ===== PLACES =====
async function fetchPlaces() {
    const container = document.getElementById('places-list');
    if (!container) return;

    container.innerHTML = '<p>Loading places...</p>';

    try {
        const res = await fetch(`${API_URL}/places`);
        if (!res.ok) throw new Error('Failed to fetch places');

        const places = await res.json();

        if (!places || places.length === 0) {
            container.innerHTML = '<p>No places available.</p>';
            return;
        }

        container.innerHTML = '';

        places.forEach(place => {
            const card = document.createElement('div');
            card.className = 'place-card';
            card.setAttribute('data-price', place.price);

            card.innerHTML = `
                <h3>${escapeHtml(place.title)}</h3>
                <p class="price">$${place.price} / night</p>
                <button class="details-button" data-id="${place.id}">View Details</button>
            `;

            const btn = card.querySelector('.details-button');
            btn.onclick = () => {
                window.location.href = `place.html?id=${place.id}`;
            };

            container.appendChild(card);
        });

        const filter = document.getElementById('price-filter');
        if (filter) {
            filter.onchange = () => {
                const maxPrice = filter.value;
                document.querySelectorAll('.place-card').forEach(card => {
                    const price = parseFloat(card.getAttribute('data-price'));
                    card.style.display = (maxPrice === 'all' || price <= maxPrice) ? 'flex' : 'none';
                });
            };
        }

    } catch (err) {
        container.innerHTML = '<p>Error loading places.</p>';
    }
}

// ===== PLACE DETAILS =====
async function loadPlaceDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (!placeId) {
        document.getElementById('place-details').innerHTML = '<p>No place ID specified.</p>';
        return;
    }

    try {
        const token = getCookie('token'); // ✅ ADD TOKEN

        // ✅ FIXED: send token
        const res = await fetch(`${API_URL}/places/${placeId}`, {
            headers: token ? {
                'Authorization': `Bearer ${token}`
            } : {}
        });

        if (!res.ok) throw new Error('Place not found');

        const place = await res.json();

        document.getElementById('place-details').innerHTML = `
            <h2>${escapeHtml(place.title)}</h2>
            <p>${escapeHtml(place.description || 'No description')}</p>
            <p class="price"><strong>Price:</strong> $${place.price} / night</p>
            <div class="owner-info"><strong>Host:</strong> ${escapeHtml(place.owner?.first_name || 'Unknown')}</div>
            <div class="amenities">
                <strong>Amenities:</strong>
                <ul>
                    ${place.amenities?.map(a => `<li>${escapeHtml(a.name)}</li>`).join('') || '<li>None</li>'}
                </ul>
            </div>
        `;

        // ✅ FIXED: send token in reviews
        const reviewsRes = await fetch(`${API_URL}/reviews/places/${placeId}/reviews`, {
            headers: token ? {
                'Authorization': `Bearer ${token}`
            } : {}
        });

        const reviews = await reviewsRes.json();

        const reviewsContainer = document.getElementById('reviews-list');
        if (reviewsContainer) {
            if (!reviews || reviews.length === 0) {
                reviewsContainer.innerHTML = '<p>No reviews yet.</p>';
            } else {
                reviewsContainer.innerHTML = reviews.map(r => `
                    <div class="review-card">
                        <p>"${escapeHtml(r.text)}"</p>
                        <p>⭐ ${r.rating}/5 - ${escapeHtml(r.user?.first_name || 'Anonymous')}</p>
                    </div>
                `).join('');
            }
        }

        // Show review form if logged in
        const addSection = document.getElementById('add-review-section');
        if (addSection && token) {
            addSection.style.display = 'block';
            document.getElementById('place-id').value = placeId;
        }

    } catch (err) {
        document.getElementById('place-details').innerHTML = '<p>Error loading place details.</p>';
    }
}

// ===== ADD REVIEW =====
function initReviewForm() {
    const form = document.getElementById('review-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const token = getCookie('token');
        if (!token) {
            alert('Please login first');
            window.location.href = 'login.html';
            return;
        }

        const placeId = document.getElementById('place-id').value;
        const text = document.getElementById('review-text').value;
        const rating = document.getElementById('rating').value;

        try {
            const res = await fetch(`${API_URL}/reviews/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ text, rating: parseInt(rating), place_id: placeId })
            });

            if (res.ok) {
                alert('Review added successfully!');
                document.getElementById('review-text').value = '';
                loadPlaceDetails();
            } else {
                const error = await res.json();
                alert(error.error || 'Failed to add review');
            }
        } catch (err) {
            alert('Network error');
        }
    });
}

// ===== HELPER =====
function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('login-form')) initLoginForm();
    if (document.getElementById('places-list')) fetchPlaces();
    if (document.getElementById('place-details')) {
        loadPlaceDetails();
        initReviewForm();
    }
});
