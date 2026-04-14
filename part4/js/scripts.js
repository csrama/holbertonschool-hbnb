/*scripts.js */

const API_URL = 'http://127.0.0.1:5000/api/v1';

/*UTILITY: Cookie helpers */
function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
            return value;
        }
    }

    return null;
}

function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/`;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

/* LOGIN */
async function loginUser(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    return response;
}

/* INDEX PAGE HELPERS */
let allPlaces = [];

function checkAuthIndex() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }

    fetchPlaces(token);
}

async function fetchPlaces(token) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/places/`, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) {
            throw new Error('Failed to fetch places');
        }

        const places = await response.json();

        if (Array.isArray(places)) {
            allPlaces = places;
        } else if (places && Array.isArray(places.places)) {
            allPlaces = places.places;
        } else {
            allPlaces = [];
        }

        displayPlaces(allPlaces);
    } catch (error) {
        const list = document.getElementById('places-list');
        if (list) {
            list.innerHTML = '<p style="color: var(--text-light);">Could not load places. Please try again later.</p>';
        }
    }
}

function displayPlaces(places) {
    const list = document.getElementById('places-list');
    if (!list) return;

    list.innerHTML = '';

    if (!places || places.length === 0) {
        list.innerHTML = '<p style="color: var(--text-light);">No places found.</p>';
        return;
    }

    places.forEach(place => {
        const placeId = place.id || '';
        const placeName = place.name || place.title || 'Unnamed place';
        const placePrice = place.price || place.price_by_night || 0;

        const card = document.createElement('div');
        card.className = 'place-card';
        card.dataset.price = placePrice;

        card.innerHTML = `
            <h3>${placeName}</h3>
            <p class="price">$${placePrice} / night</p>
            <a href="place.html?id=${placeId}" class="details-button">View Details</a>
        `;

        list.appendChild(card);
    });
}

function setupPriceFilter() {
    const filter = document.getElementById('price-filter');
    if (!filter) return;

    filter.addEventListener('change', (event) => {
        const selected = event.target.value;
        const cards = document.querySelectorAll('.place-card');

        cards.forEach(card => {
            const price = parseFloat(card.dataset.price);

            if (selected === 'all' || price <= parseFloat(selected)) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

/*PLACE DETAILS HELPERS */
async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) {
            throw new Error('Place not found');
        }

        const place = await response.json();
        displayPlaceDetails(place);
        fetchReviews(token, placeId);
    } catch (error) {
        const section = document.getElementById('place-details');
        if (section) {
            section.innerHTML = '<p>Could not load place details.</p>';
        }
    }
}

function displayPlaceDetails(place) {
    const section = document.getElementById('place-details');
    if (!section) return;

    const placeName = place.name || place.title || 'Unnamed place';
    const placePrice = place.price || place.price_by_night || 0;
    const hostName = place.host || place.owner_name || place.owner_id || 'N/A';
    const description = place.description || 'No description provided.';
    const location = place.location || (
        place.latitude !== undefined && place.longitude !== undefined
            ? `${place.latitude}, ${place.longitude}`
            : 'N/A'
    );

    const amenitiesHTML = place.amenities && place.amenities.length > 0
        ? place.amenities.map(a => `<span class="amenity-tag">${a.name || a}</span>`).join('')
        : '<span class="amenity-tag">None listed</span>';

    section.innerHTML = `
        <div class="place-details">
            <h1>${placeName}</h1>
            <div class="place-info">
                <p><strong>Host:</strong> ${hostName}</p>
                <p><strong>Price:</strong> $${placePrice} / night</p>
                <p><strong>Location:</strong> ${location}</p>
                <p><strong>Description:</strong> ${description}</p>
            </div>
            <div>
                <strong>Amenities:</strong>
                <div class="amenities-list">${amenitiesHTML}</div>
            </div>
        </div>
    `;
}

async function fetchReviews(token, placeId) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/places/${placeId}/reviews`, {
            method: 'GET',
            headers: headers
        });

        if (!response.ok) return;

        const reviews = await response.json();
        displayReviews(reviews);
    } catch (error) {
        console.error('Could not load reviews');
    }
}

function displayReviews(reviews) {
    const section = document.getElementById('reviews-list');
    if (!section) return;

    section.innerHTML = '<h2>Reviews</h2>';

    if (!reviews || reviews.length === 0) {
        section.innerHTML += '<p style="color: var(--text-light);">No reviews yet. Be the first!</p>';
        return;
    }

    reviews.forEach(review => {
        const stars = '⭐'.repeat(review.rating || 0);
        const reviewer = review.user_name || review.user || 'Anonymous';
        const reviewText = review.text || review.comment || 'No review text provided.';

        const card = document.createElement('div');
        card.className = 'review-card';
        card.innerHTML = `
            <p class="reviewer">${reviewer}</p>
            <p class="rating">${stars}</p>
            <p>${reviewText}</p>
        `;
        section.appendChild(card);
    });
}

/*ADD REVIEW HELPERS */
function checkAuthentication() {
    const token = getCookie('token');

    if (!token) {
        window.location.href = 'index.html';
        return null;
    }

    return token;
}

function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch(e) {
        return null;
    }
}

async function submitReview(token, placeId, text, rating) {
    try {
        const payload = parseJwt(token);
        const userId = payload ? payload.sub : "";

        const response = await fetch(`${API_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: text,
                rating: rating,
                place_id: placeId,
                user_id: userId
            })
        });

        await handleReviewResponse(response);
    } catch (error) {
        alert('Connection error. Please try again.');
    }
}

async function handleReviewResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');

        const form = document.getElementById('review-form');
        if (form) {
            form.reset();
        }

        const placeId = getPlaceIdFromURL();
        if (placeId && window.location.pathname.includes('add_review')) {
            window.location.href = `place.html?id=${placeId}`;
        }
    } else {
        const data = await response.json().catch(() => ({}));
        alert('Failed to submit review: ' + (data.error || response.statusText));
    }
}

/*PAGE INITIALIZATION */
document.addEventListener('DOMContentLoaded', () => {
    /* -- LOGIN PAGE -- */
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            const errorMsg = document.getElementById('error-message');

            try {
                const response = await loginUser(email, password);

                if (response.ok) {
                    const data = await response.json();
                    setCookie('token', data.access_token);
                    window.location.href = document.referrer || 'index.html';
                } else {
                    errorMsg.style.display = 'block';
                    errorMsg.textContent = 'Invalid email or password. Please try again.';
                }
            } catch (error) {
                errorMsg.style.display = 'block';
                errorMsg.textContent = 'Connection error. Please try again.';
            }
        });
    }

    /* -- INDEX PAGE -- */
    const placesList = document.getElementById('places-list');
    if (placesList) {
        checkAuthIndex();
        setupPriceFilter();
    }

    /* -- PLACE DETAILS PAGE -- */
    const placeDetails = document.getElementById('place-details');
    if (placeDetails) {
        const placeId = getPlaceIdFromURL();
        const token = getCookie('token');

        const loginLink = document.getElementById('login-link');
        if (loginLink) {
            loginLink.style.display = token ? 'none' : 'block';
        }

        const addReviewSection = document.getElementById('add-review-section');
        if (addReviewSection) {
            addReviewSection.style.display = token ? 'block' : 'none';
        }

        if (placeId) {
            fetchPlaceDetails(token, placeId);
        }

        const reviewForm = document.getElementById('review-form');
        if (reviewForm && placeId) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();

                const text = document.getElementById('review-text').value.trim();
                const rating = parseInt(document.getElementById('rating').value, 10);

                await submitReview(token, placeId, text, rating);
            });
        }
    }

    /* -- ADD REVIEW PAGE -- */
    const addReviewPageForm = document.getElementById('review-form');
    if (addReviewPageForm && !document.getElementById('place-details')) {
        const token = checkAuthentication();
        const placeId = getPlaceIdFromURL();

        addReviewPageForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const text = document.getElementById('review-text').value.trim();
            const rating = parseInt(document.getElementById('rating').value, 10);

            await submitReview(token, placeId, text, rating);
        });
    }
});
