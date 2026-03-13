# HBnB Database Entity-Relationship Diagram (ERD) Documentation

## Project: Holberton School HBnB
### Part 3: Database Schema Design

---

## 1. Introduction

This document presents the Entity-Relationship Diagram (ERD) for the Holberton HBnB project, a platform similar to Airbnb. The ERD visually represents the database schema, showing all entities (tables), their attributes, and the relationships between them. This diagram serves as a blueprint for the database implementation and ensures all stakeholders have a clear understanding of the data structure.

The diagram was created using **Mermaid.js**, a markdown-like syntax tool that allows for easy integration into documentation and version control platforms like GitHub.

---

## 2. Entity Descriptions

### 2.1 USERS
The USERS table stores information about all platform users, including both guests and hosts.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| id | string | PRIMARY KEY | Unique identifier for each user |
| first_name | string | NOT NULL | User's first name |
| last_name | string | NOT NULL | User's last name |
| email | string | UNIQUE, NOT NULL | Unique email address used for login |
| password | string | NOT NULL | Hashed password for authentication |
| is_admin | boolean | DEFAULT false | Admin privileges flag (true = administrator) |
| created_at | datetime | NOT NULL | Record creation timestamp |
| updated_at | datetime | NOT NULL | Record last update timestamp |

**Relationships:**
- One user can own many places (one-to-many with PLACES)
- One user can write many reviews (one-to-many with REVIEWS)

---

### 2.2 PLACES
The PLACES table represents properties listed on the platform by users.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| id | string | PRIMARY KEY | Unique identifier for each place |
| title | string | NOT NULL | Place title/name |
| description | text | - | Detailed description of the property |
| price | float | NOT NULL | Price per night in local currency |
| latitude | float | - | Geographic latitude coordinate |
| longitude | float | - | Geographic longitude coordinate |
| owner_id | string | FOREIGN KEY | References USERS.id (the property owner) |
| created_at | datetime | NOT NULL | Record creation timestamp |
| updated_at | datetime | NOT NULL | Record last update timestamp |

**Relationships:**
- Many places belong to one user (many-to-one with USERS)
- One place can receive many reviews (one-to-many with REVIEWS)
- One place can have many amenities (many-to-many with AMENITIES via PLACE_AMENITY)

---

### 2.3 REVIEWS
The REVIEWS table stores user feedback and ratings about places they've visited.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| id | string | PRIMARY KEY | Unique identifier for each review |
| user_id | string | FOREIGN KEY | References USERS.id (the review author) |
| place_id | string | FOREIGN KEY | References PLACES.id (the place being reviewed) |
| text | text | NOT NULL | Review content/text |
| created_at | datetime | NOT NULL | Review creation timestamp |
| updated_at | datetime | NOT NULL | Record last update timestamp |

**Relationships:**
- Many reviews belong to one user (many-to-one with USERS)
- Many reviews belong to one place (many-to-one with PLACES)

---

### 2.4 AMENITIES
The AMENITIES table stores available amenities that can be associated with places.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| id | string | PRIMARY KEY | Unique identifier for each amenity |
| name | string | UNIQUE, NOT NULL | Unique amenity name (e.g., "WiFi", "Pool", "Air Conditioning") |
| created_at | datetime | NOT NULL | Record creation timestamp |
| updated_at | datetime | NOT NULL | Record last update timestamp |

**Relationships:**
- One amenity can belong to many places (many-to-many with PLACES via PLACE_AMENITY)

---

### 2.5 PLACE_AMENITY (Junction Table)
The PLACE_AMENITY table handles the many-to-many relationship between PLACES and AMENITIES.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| place_id | string | PRIMARY KEY, FOREIGN KEY | References PLACES.id (part of composite key) |
| amenity_id | string | PRIMARY KEY, FOREIGN KEY | References AMENITIES.id (part of composite key) |
| created_at | datetime | NOT NULL | Junction record creation timestamp |

**Composite Primary Key:** (place_id, amenity_id) - Ensures each combination is unique, preventing duplicate amenity assignments to the same place.

**Relationships:**
- Many PLACE_AMENITY records belong to one place (many-to-one with PLACES)
- Many PLACE_AMENITY records belong to one amenity (many-to-one with AMENITIES)


---

## 3. Relationship Analysis

### 3.1 One-to-Many Relationships

| Relationship | Type | Description |
|--------------|------|-------------|
| USER → PLACE | One-to-Many | A user can own multiple properties, but each property has exactly one owner |
| USER → REVIEW | One-to-Many | A user can write multiple reviews, but each review has exactly one author |
| PLACE → REVIEW | One-to-Many | A place can receive multiple reviews, but each review is for exactly one place |

### 3.2 Many-to-Many Relationship

The relationship between PLACE and AMENITY is many-to-many:
- A place can have multiple amenities (WiFi, Pool, Kitchen, etc.)
- An amenity can be available in multiple places

This is implemented using the **PLACE_AMENITY** junction table, which:
- Resolves the many-to-many relationship into two one-to-many relationships
- Uses a composite primary key to ensure data integrity
- Allows for efficient querying of amenities by place and places by amenity

---

## 4. Data Integrity and Constraints

### 4.1 Primary Keys
- All entities use string-based UUIDs as primary keys for scalability and distributed system compatibility

### 4.2 Foreign Keys
- `PLACE.user_id` references `USER.id` (cascade delete behavior should be considered)
- `REVIEW.user_id` references `USER.id`
- `REVIEW.place_id` references `PLACE.id`
- `PLACE_AMENITY.place_id` references `PLACE.id`
- `PLACE_AMENITY.amenity_id` references `AMENITY.id`

### 4.3 Composite Keys
- `PLACE_AMENITY` uses a composite primary key (place_id, amenity_id) to ensure unique combinations

### 4.4 Additional Constraints
- `USER.email` should have a UNIQUE constraint
- `AMENITY.name` should have a UNIQUE constraint
- All NOT NULL constraints as specified in entity tables

---

## 5. Performance Considerations

### 5.1 Recommended Indexes
For optimal query performance, indexes should be created on:

| Table | Column(s) | Reason |
|-------|-----------|--------|
| USER | email | Used for login authentication |
| PLACE | user_id | Frequently used to find places by owner |
| PLACE | city_id | Used for location-based searches |
| REVIEW | place_id | Used to load all reviews for a place |
| REVIEW | user_id | Used to load all reviews by a user |
| PLACE_AMENITY | place_id | Used to find amenities for a place |
| PLACE_AMENITY | amenity_id | Used to find places with specific amenities |

### 5.2 Data Types Choice
- **String IDs**: Using strings for primary keys allows for UUID generation, which is preferable in distributed systems
- **Float for price**: Accommodates decimal values for accurate pricing
- **int for rating**: to make rating frome 1 to 5
- **Datetime for timestamps**: Enables time-based queries and sorting

---

## 6. ERD Diagram

Below is the complete ERD created with Mermaid.js:

```mermaid
erDiagram
    %% HBnB Database Schema
    %% Project: Holberton School HBnB
    %% Version: 1.0

    %% Tables
    USERS {
        string id PK "Primary Key"
        string first_name "User's first name"
        string last_name "User's last name"
        string email UK "Unique email address"
        string password "Hashed password"
        boolean is_admin "Admin privileges flag"
        datetime created_at "Record creation timestamp"
        datetime updated_at "Record last update timestamp"
    }

    PLACES {
        string id PK "Primary Key"
        string title "Place title/name"
        string description "Detailed description"
        float price "Price per night"
        float latitude "Geographic latitude"
        float longitude "Geographic longitude"
        string owner_id FK "References USERS.id (owner)"
        datetime created_at "Record creation timestamp"
        datetime updated_at "Record last update timestamp"
    }

    REVIEWS {
        string id PK "Primary Key"
        string user_id FK "References USERS.id (author)"
        string place_id FK "References PLACES.id"
        string text "Review content"
        datetime created_at "Review creation timestamp"
        datetime updated_at "Record last update timestamp"
    }

    AMENITIES {
        string id PK "Primary Key"
        string name UK "Unique amenity name"
        datetime created_at "Record creation timestamp"
        datetime updated_at "Record last update timestamp"
    }

    PLACE_AMENITY {
        string place_id PK, FK "References PLACES.id"
        string amenity_id PK, FK "References AMENITIES.id"
        datetime created_at "Junction record creation timestamp"
    }

    %% Relationships
    USERS ||--o{ PLACES : "1 user owns many places"
    USERS ||--o{ REVIEWS : "1 user writes many reviews"
    PLACES ||--o{ REVIEWS : "1 place receives many reviews"
    PLACES ||--o{ PLACE_AMENITY : "1 place has many amenities"
    AMENITIES ||--o{ PLACE_AMENITY : "1 amenity belongs to many places"
```

---
### 7. Conclusion
The ERD provides a complete and accurate representation of the HBnB database schema. It captures all required entities and their relationships, ensuring:

- Data integrity through proper primary and foreign key constraints

- Flexibility with a many-to-many relationship between places and amenities

- Scalability with string-based UUID primary keys

- Clarity with comprehensive attribute definitions and relationship cardinalities

The diagram serves as an essential reference for developers implementing the database layer and for future maintenance of the HBnB platform.

---
### Authors 
- Raghad Almalki
- Jana Bakri
- Rama Alsheheri
