# HBnB API Documentation

## Overview

The **HBnB API** provides a RESTful interface for managing users, places, reviews, and amenities.
This API is built using **Flask** and follows standard HTTP methods to interact with resources.

All responses are returned in **JSON format**.

---

# Base URL

```
http://localhost:5000/api/v1
```

---

# Authentication

Some endpoints require authentication using **JWT tokens**.

Example header:

```
Authorization: Bearer <your_token>
```

Admin-only endpoints require the authenticated user to have:

```
"is_admin": true
```

---

# Data Models

## User

| Field      | Type    | Description                               |
| ---------- | ------- | ----------------------------------------- |
| id         | string  | Unique identifier                         |
| first_name | string  | User first name                           |
| last_name  | string  | User last name                            |
| email      | string  | User email address                        |
| password   | string  | User password                             |
| is_admin   | boolean | Indicates if the user is an administrator |

---

## Place

| Field       | Type   | Description              |
| ----------- | ------ | ------------------------ |
| id          | string | Unique identifier        |
| title       | string | Name of the place        |
| description | string | Description of the place |
| price       | float  | Price per night          |
| latitude    | float  | Geographic latitude      |
| longitude   | float  | Geographic longitude     |
| owner_id    | string | Owner (User) ID          |

---

## Review

| Field    | Type    | Description          |
| -------- | ------- | -------------------- |
| id       | string  | Unique identifier    |
| text     | string  | Review content       |
| rating   | integer | Rating score         |
| user_id  | string  | Author of the review |
| place_id | string  | Reviewed place       |

---

## Amenity

| Field | Type   | Description         |
| ----- | ------ | ------------------- |
| id    | string | Unique identifier   |
| name  | string | Name of the amenity |

---

# Users Endpoints

## Get All Users

Retrieve all users in the system.

```
GET /users/
```

### Response Example

```json
[
  {
    "id": "123",
    "first_name": "Raghad",
    "last_name": "Almalki",
    "email": "raghad@example.com",
    "is_admin": false
  }
]
```

---

## Get User by ID

Retrieve details of a specific user.

```
GET /users/<user_id>
```

### Example Response

```json
{
  "id": "123",
  "first_name": "Raghad",
  "last_name": "Almalki",
  "email": "raghad@example.com",
  "is_admin": false
}
```

---

## Create User

Create a new user.

```
POST /users/
```

### Request Body

```json
{
  "first_name": "Raghad",
  "last_name": "Almalki",
  "email": "raghad@example.com",
  "password": "mypassword"
}
```

### Response

```
201 Created
```

---

## Update User

Update user information.

```
PUT /users/<user_id>
```

### Request Body

```json
{
  "first_name": "Updated",
  "last_name": "Name"
}
```

### Response

```
200 OK
```

---

# Places Endpoints

## Get All Places

Retrieve all places.

```
GET /places/
```

### Response Example

```json
[
  {
    "id": "1",
    "title": "Beach House",
    "price": 200,
    "latitude": 25.2048,
    "longitude": 55.2708
  }
]
```

---

## Get Place by ID

Retrieve details of a specific place.

```
GET /places/<place_id>
```

---

# Reviews Endpoints

## Get Reviews for a Place

Retrieve all reviews for a specific place.

```
GET /places/<place_id>/reviews
```

### Response Example

```json
[
  {
    "id": "10",
    "text": "Great place!",
    "rating": 5,
    "user_id": "123"
  }
]
```

---

# Amenities Endpoints

## Get All Amenities

Retrieve all amenities.

```
GET /amenities/
```

### Response Example

```json
[
  {
    "id": "1",
    "name": "WiFi"
  },
  {
    "id": "2",
    "name": "Swimming Pool"
  }
]
```

---

# Error Handling

The API uses standard HTTP response codes.

| Status Code | Meaning               |
| ----------- | --------------------- |
| 200         | Success               |
| 201         | Resource created      |
| 400         | Bad request           |
| 401         | Unauthorized          |
| 403         | Forbidden             |
| 404         | Resource not found    |
| 500         | Internal server error |

---

# Notes

* All requests and responses use **JSON format**.
* Authentication is required for protected endpoints.
* Admin privileges are required for certain operations such as creating users.
* The API follows **RESTful design principles**.

---
### Authors 
- Raghad Almalki
- Jana Bakr
- Rama Alsheheri
