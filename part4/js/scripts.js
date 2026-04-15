/*scripts.js */

const API_URL = 'http://127.0.0.1:5000/api/v1';

/**
 * Retrieves a value from either localStorage or cookies.
 * This ensures compatibility across different browser environments.
 */
function getCookie(name) {
    // Primary: check localStorage
    const lsVal = localStorage.getItem(name);
    if (lsVal) return lsVal;

    // Fallback: check cookies (for compatibility)
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value;
    }
    return null;
}

/**
 * Saves a value to BOTH localStorage and cookies.
 * Used primarily for storing the JWT authentication token.
 */
function setCookie(name, value, days = 7) {
    // Store in localStorage for reliable cross-page access
    localStorage.setItem(name, value);
    // Also set cookie as fallback
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/`;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

function updateLoginLinkState(loginLink, token) {
    if (!loginLink) return;
    if (token) {
        loginLink.textContent = 'Logout';
        loginLink.href = '#';
        loginLink.style.backgroundColor = 'var(--primary-purple)';
        loginLink.style.color = 'white';
        loginLink.style.display = 'block';
        loginLink.onclick = (e) => {
            e.preventDefault();
            // Clear token from both localStorage and cookie
            localStorage.removeItem('token');
            document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            window.location.href = 'index.html';
        };
    } else {
        loginLink.textContent = 'Login';
        loginLink.href = 'login.html';
        loginLink.style.backgroundColor = 'white';
        loginLink.style.color = 'var(--primary-purple)';
        loginLink.style.display = 'block';
        loginLink.onclick = null;
    }
}

/**
 * Sends a POST request to the API to authenticate a user.
 * Returns the raw response object.
 */
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

    updateLoginLinkState(loginLink, token);

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

/**
 * Renders the fetched places into the index page grid.
 * Displays the name and price for each card as required.
 * @param {Array} places - Array of place objects from the API.
 */
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

/**
 * Initializes the client-side price filter.
 * Hides or shows cards based on the selected maximum price.
 */
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

    // Map amenity keywords → Font Awesome icon classes
    const amenityIconMap = [
        { keywords: ['wifi', 'wi-fi', 'internet', 'wireless'], icon: 'fa-solid fa-wifi' },
        { keywords: ['bed', 'bedroom', 'sleep', 'beds'], icon: 'fa-solid fa-bed' },
        { keywords: ['bath', 'bathroom', 'bathtub', 'shower'], icon: 'fa-solid fa-shower' },
        { keywords: ['pool', 'swimming'], icon: 'fa-solid fa-person-swimming' },
        { keywords: ['parking', 'garage', 'car'], icon: 'fa-solid fa-square-parking' },
        { keywords: ['kitchen', 'cooking', 'oven', 'microwave'], icon: 'fa-solid fa-kitchen-set' },
        { keywords: ['air', 'ac', 'conditioning', 'cooling'], icon: 'fa-solid fa-snowflake' },
        { keywords: ['heating', 'heater', 'heat'], icon: 'fa-solid fa-temperature-high' },
        { keywords: ['tv', 'television', 'netflix', 'cable'], icon: 'fa-solid fa-tv' },
        { keywords: ['washer', 'laundry', 'dryer', 'washing'], icon: 'fa-solid fa-jug-detergent' },
        { keywords: ['gym', 'fitness', 'workout', 'exercise'], icon: 'fa-solid fa-dumbbell' },
        { keywords: ['pet', 'dog', 'cat', 'animal'], icon: 'fa-solid fa-paw' },
        { keywords: ['smoke', 'smoking'], icon: 'fa-solid fa-smoking' },
        { keywords: ['breakfast', 'coffee', 'food', 'meal'], icon: 'fa-solid fa-mug-hot' },
        { keywords: ['balcony', 'terrace', 'patio', 'garden'], icon: 'fa-solid fa-umbrella-beach' },
        { keywords: ['elevator', 'lift'], icon: 'fa-solid fa-elevator' },
        { keywords: ['fireplace', 'fire'], icon: 'fa-solid fa-fire' },
        { keywords: ['desk', 'workspace', 'office', 'work'], icon: 'fa-solid fa-briefcase' },
        { keywords: ['security', 'lock', 'safe', 'alarm'], icon: 'fa-solid fa-shield-halved' },
        { keywords: ['baby', 'crib', 'children', 'kid'], icon: 'fa-solid fa-baby' },
        { keywords: ['bbq', 'grill', 'barbecue'], icon: 'fa-solid fa-fire-burner' },
        { keywords: ['boat', 'kayak', 'canoe', 'water sport'], icon: 'fa-solid fa-sailboat' },
        { keywords: ['beach', 'sea', 'ocean', 'lake'], icon: 'fa-solid fa-water' },
        { keywords: ['mountain', 'ski', 'snow', 'hill'], icon: 'fa-solid fa-mountain-sun' },
    ];

    function getAmenityIcon(name) {
        const key = name.toLowerCase();
        for (const entry of amenityIconMap) {
            if (entry.keywords.some(k => key.includes(k))) {
                return `<i class="${entry.icon} amenity-icon-fa"></i>`;
            }
        }
        // Default fallback icon
        return `<i class="fa-solid fa-tag amenity-icon-fa"></i>`;
    }

    const amenitiesHTML = place.amenities && place.amenities.length > 0
        ? place.amenities.map(a => {
            const label = a.name || a;
            return `<span class="amenity-tag">${getAmenityIcon(label)}${label}</span>`;
        }).join('')
        : '<span class="amenity-tag"><i class="fa-solid fa-circle-info amenity-icon-fa"></i>None listed</span>';

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

        const response = await fetch(`${API_URL}/reviews/places/${placeId}/reviews`, {
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

    section.innerHTML = '';

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
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) {
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
                    window.location.href = 'index.html';
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
        updateLoginLinkState(loginLink, token);

        const addReviewSection = document.getElementById('add-review-section');
        if (addReviewSection) {
            addReviewSection.style.display = token ? 'block' : 'none';
        }

        if (placeId) {
            fetchPlaceDetails(token, placeId);
        }

        const reviewForm = document.getElementById('review-form');

        // Star Rating Logic
        const stars = document.querySelectorAll('.star');
        const ratingInput = document.getElementById('rating');
        if (stars.length > 0) {
            stars.forEach(star => {
                star.addEventListener('click', () => {
                    const value = parseInt(star.getAttribute('data-value'), 10);
                    ratingInput.value = value;
                    stars.forEach(s => {
                        if (parseInt(s.getAttribute('data-value'), 10) <= value) {
                            s.classList.add('active');
                        } else {
                            s.classList.remove('active');
                        }
                    });
                });
            });
        }

        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();

                if (!placeId) {
                    alert('Error: No place ID found in URL. Please navigate here from the home page!');
                    return;
                }

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
