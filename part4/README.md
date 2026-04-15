# HBnB – Part 4 (Simple Web Client)

## Overview

This is the frontend of the HBnB project. It is built with:

- HTML5
- CSS3
- JavaScript (ES6)

It connects to a backend API to:

- Secure user authentication and session management
- Dynamic listing of available places via AJAX
- Detailed place views including host info and amenity icons
- Interactive review submission system
- **Filter Feature**: Client-side filtering by **Maximum Price** (10$, 50$, 100$)

## Pages

### 1. Login (`login.html`)
- Handles user authentication.
- Stores JWT token in a secure cookie.
- Redirects to the homepage upon success.

### 2. Index (`index.html`)
- Displays all places as interactive cards.
- **Filtering**: Fully functional Max Price dropdown filter.
- **Auth State**: Automatically hides the Login link when the user is authenticated.

### 3. Place Details (`place.html`)
- Shows full info about a place:
  - Title
  - Description
  - Price
  - Owner
  - Amenities
- Shows reviews
- Shows review form if user is logged in

### 4. Add Review (`add_review.html`)
- Only for logged-in users
- Submit review + rating (1-5)

### 5. Admin Dashboard (`admin.html`)
- Only for admin users
- View all users
- View all places
- View and delete amenities
- Create new amenities

## How It Works

### Login Flow
1. User submits credentials via the login form.
2. AJAX request sent to backend: `POST /api/v1/auth/login`.
3. Backend returns a JWT token.
4. Token is stored in a cookie.
5. `scripts.js` detects the token and hides the "Login" link globally.

### Price Filtering Logic
The filter logic in `scripts.js` uses `data-price` attributes on cards to instantly toggle visibility based on the selected maximum value, providing a smooth user experience without page refreshes.

### Fetch Data
All data is fetched using Fetch API:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/places` | GET | Get all places |
| `/api/v1/places/{id}` | GET | Get place details |
| `/api/v1/reviews/places/{id}/reviews` | GET | Get reviews for a place |
| `/api/v1/reviews` | POST | Add a review |
| `/api/v1/users` | GET | Get all users (admin only) |
| `/api/v1/amenities` | GET/POST | Get/create amenities |

### Authentication
- Token is stored in cookies
- Used in requests

- ## Project Structure
part4/
├── index.html
├── login.html
├── place.html
├── add_review.html
├── admin.html
├── css/
│ └── styles.css
├── js/
│ └── scripts.js
└── images/


text

## How to Run

### 1. Start Backend (Part 3)
```bash
cd part3
python3 run.py
Backend runs on: http://localhost:5000

2. Start Frontend
Option 1: VS Code Live Server (Recommended)
Open part4 folder in VS Code

Right-click index.html → "Open with Live Server"

Frontend runs on: http://127.0.0.1:5500

Option 2: Python HTTP Server
bash
cd part4
python3 -m http.server 8080
Then open: http://localhost:8080/index.html

### 3. Login Credentials (Synced with Database)
| Role | Email | Password |
|------|-------|----------|
| **Admin** | raghad@hbnb.com | admin123 |
| **Regular User** | jana@hbnb.com | jana123 |
| **Regular User** | rama@hbnb.com | rama123 |
CORS Fix
If you get CORS errors, add this to part3/app/__init__.py:

python
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # ← Add this line
    # ... rest of your code
Then restart the backend server.

Requirements
Python 3.8+

Flask backend running (Part 3)

Modern web browser (Chrome, Firefox, Edge)

Important JavaScript Functions
Function	Purpose
getCookie(name)	Read token from cookie
setCookie(name, value)	Save token to cookie
isAuthenticated()	Check if user is logged in
fetchPlaces()	Load all places from API
displayPlaces(places)	Render places as cards
filterPlacesByPrice()	Filter places client-side
loadPlaceDetails(placeId)	Load place info
loadReviews(placeId)	Load reviews for a place
displayReviews(reviews)	Render reviews
submitReview(e)	Send review to API
## Testing & Verification
1. **Initialize**: Run `python setup_database.py` in the `part3` folder.
2. **Login**: Use `raghad@hbnb.com` to log in. Verify the "Login" link disappears.
3. **Filter**: Set "Max Price" to 50$. Verify that places over 50$ are hidden.
4. **Details**: Click "View Details" to see deep info and amenity icons.
5. **Navigation**: Click the HBnB Logo from any sub-page to return home instantly.

Author

Rama Alshehri – @csrama

Jana Bakri – @janabakri

Raghad Almalki – @Raghad717

Project
HBnB Project (Part 4) – Simple Web Client
Holberton School

