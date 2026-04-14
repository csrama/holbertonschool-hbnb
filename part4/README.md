# HBnB – Part 4 (Simple Web Client)

## Overview

This is the frontend of the HBnB project. It is built with:

- HTML5
- CSS3
- JavaScript (ES6)

It connects to a backend API to:

- Login users
- Show places
- Show place details
- Add reviews
- Admin dashboard

## Pages

### 1. Login (`login.html`)
- User enters email and password
- Sends request to API (`/auth/login`)
- Saves JWT token in cookie
- Redirects to index page

### 2. Index (`index.html`)
- Shows all places as cards
- Each place has:
  - Title
  - Price
  - "View Details" button
- Filter places by price (client-side)
- Shows login link only if user is not logged in

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
1. User submits form
2. Request sent to: `POST /api/v1/auth/login`
3. API returns token
4. Token saved in cookie
5. User redirected to index page

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

3. Login Credentials
Role	Email	Password
Admin	admin@example.com	admin123
Regular User	test123@example.com	test123
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
Testing
After running both backend and frontend:

Open login.html

Login with admin credentials

You should be redirected to index.html

Click "View Details" on any place

Add a review (as regular user)

Visit admin.html to manage amenities

Troubleshooting
Issue	Solution
"Invalid credentials"	Check email/password, or create admin in database
CORS error	Add CORS(app) to Flask app
"Failed to fetch"	Make sure backend is running on port 5000
404 errors	Check API endpoints and place IDs
No places showing	Create places in database using Python script

Author

Rama Alshehri – @csrama

Jana Bakri – @janabakri

Raghad Almalki – @Raghad717

Project
HBnB Project (Part 4) – Simple Web Client
Holberton School

