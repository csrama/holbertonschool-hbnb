# HBnB Database Entity-Relationship Diagram (ERD) Documentation

## Project: Holberton School HBnB
## Part 3: Database Schema Design

---

## 1. Introduction

This document presents the Entity-Relationship Diagram (ERD) for the Holberton HBnB project, a platform similar to Airbnb. The ERD visually represents the database schema, showing all entities (tables), their attributes, and the relationships between them. This diagram serves as a blueprint for the database implementation and ensures all stakeholders have a clear understanding of the data structure.

The diagram was created using **Mermaid.js**, a markdown-like syntax tool that allows for easy integration into documentation and version control platforms like GitHub.

---

## 2. Entity Descriptions

### 2.1 USER
The USER entity stores information about all platform users, including both guests and hosts.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| id | string | PRIMARY KEY | Unique identifier for each user |
| first_name | string | NOT NULL | User's first name |
| last_name | string | NOT NULL | User's last name |
| email | string | UNIQUE, NOT NULL | User's email address for login |
| password | string | NOT NULL | Hashed password for authentication |
| is_admin | boolean | DEFAULT false | Flag indicating if user has admin privileges |

**Relationships:**
- One user can own many places (one-to-many with PLACE)
- One user can write many reviews (one-to-many with REVIEW)

### 2.2 PLACE
The PLACE entity represents properties listed on the platform.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| id | string | PRIMARY KEY | Unique identifier for each place |
| name | string | NOT NULL | Name/title of the place |
| description | string | - | Detailed description of the property |
| city_id | string | FOREIGN KEY | References the City table (external) |
| user_id | string | FOREIGN KEY | References the owner (USER.id) |

**Relationships:**
- Many places belong to one user (many-to-one with USER)
- One place can receive many reviews (one-to-many with REVIEW)
- One place can have many amenities (many-to-many with AMENITY via PLACE_AMENITY)

### 2.3 REVIEW
The REVIEW entity stores user feedback about places they've visited.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| id | string | PRIMARY KEY | Unique identifier for each review |
| user_id | string | FOREIGN KEY | References the author (USER.id) |
| place_id | string | FOREIGN KEY | References the place being reviewed (PLACE.id) |
| text | string | NOT NULL | The review content |
| created_at | datetime | NOT NULL | Timestamp of when review was created |

**Relationships:**
- Many reviews belong to one user (many-to-one with USER)
- Many reviews belong to one place (many-to-one with PLACE)

### 2.4 AMENITY
The AMENITY entity stores available amenities that can be associated with places.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| id | string | PRIMARY KEY | Unique identifier for each amenity |
| name | string | UNIQUE, NOT NULL | Name of the amenity (e.g., "WiFi", "Pool") |

**Relationships:**
- One amenity can belong to many places (many-to-many with PLACE via PLACE_AMENITY)

### 2.5 PLACE_AMENITY (Junction Table)
This associative entity handles the many-to-many relationship between PLACE and AMENITY.

| Attribute | Data Type | Constraints | Description |
|-----------|-----------|-------------|-------------|
| place_id | string | FOREIGN KEY, COMPOSITE PK | References PLACE.id |
| amenity_id | string | FOREIGN KEY, COMPOSITE PK | References AMENITY.id |

**Composite Primary Key:** (place_id, amenity_id) - Ensures each combination is unique, preventing duplicate amenity assignments to the same place.

**Relationships:**
- Many PLACE_AMENITY records belong to one place (many-to-one with PLACE)
- Many PLACE_AMENITY records belong to one amenity (many-to-one with AMENITY)

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
- **Datetime for timestamps**: Enables time-based queries and sorting

---

## 6. ERD Diagram

Below is the complete ERD created with Mermaid.js:

erDiagram
    %% Tables
    USER {
        string id PK "Primary Key"
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }

    PLACE {
        string id PK "Primary Key"
        string name
        string description
        string city_id FK "Foreign Key to City table"
        string user_id FK "Foreign Key to User.id (owner)"
        float price_by_night
        integer max_guest
        integer number_rooms
        integer number_bathrooms
    }

    REVIEW {
        string id PK "Primary Key"
        string user_id FK "Foreign Key to User.id (author)"
        string place_id FK "Foreign Key to Place.id"
        string text
        datetime created_at
    }

    AMENITY {
        string id PK "Primary Key"
        string name
    }

    PLACE_AMENITY {
        string place_id FK "Foreign Key to Place.id"
        string amenity_id FK "Foreign Key to Amenity.id"
    }

    %% Relationships
    USER ||--o{ PLACE : "1 user owns many places"
    USER ||--o{ REVIEW : "1 user writes many reviews"
    PLACE ||--o{ REVIEW : "1 place receives many reviews"
    PLACE ||--o{ PLACE_AMENITY : "1 place can have many amenities"
    AMENITY ||--o{ PLACE_AMENITY : "1 amenity can belong to many places"
