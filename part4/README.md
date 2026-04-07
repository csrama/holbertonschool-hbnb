# HBnB – Part 4 (Simple Web Client)

## Overview

This is the **frontend** of the HBnB project. It is built with:

* HTML
* CSS
* JavaScript (ES6)

It connects to a backend API to:

* Login users
* Show places
* Show place details
* Add reviews

---

## Pages

### 1. Login (login.html)

* User enters email and password
* Sends request to API
* Saves token in cookie
* Redirects to index page

### 2. Index (index.html)

* Shows all places
* Each place has:

  * Title
  * Price
  * "View Details" button
* Filter places by price
* Shows login link only if user is not logged in

### 3. Place Details (place.html)

* Shows full info about a place:

  * Title
  * Description
  * Price
  * Owner
  * Amenities
* Shows reviews
* Shows review form if user is logged in

### 4. Add Review (add_review.html)

* Only for logged-in users
* Submit review + rating

---

## How It Works

### Login Flow

1. User submits form
2. Request sent to:
   `/auth/login`
3. API returns token
4. Token saved in cookie
5. User redirected to index page

---

### Fetch Data

All data is fetched using **Fetch API**:

* Get places:
  `/places`
* Get place details:
  `/places/:id`
* Get reviews:
  `/reviews/...`
* Add review:
  `/reviews/`

---

### Authentication

* Token is stored in cookies
* Used in requests like:

```
Authorization: Bearer <token>
```

---

## Important Functions

* `getCookie()` → read token
* `setCookie()` → save token
* `fetchPlaces()` → load places
* `displayPlaces()` → show places
* `loadPlaceDetails()` → load place info
* `submitReview()` → send review

---

## Run the Project

1. Start backend:

```
http://localhost:5000
```

2. Open in browser:

```
index.html
```

---

## Notes

* Make sure backend is running
* Fix CORS if needed in Flask:

```python
from flask_cors import CORS
CORS(app)
```

---

## Author
 Rama ALahehri
 Jana Bakri
 Raghad ALmalki

HBnB Project (Part 4)
