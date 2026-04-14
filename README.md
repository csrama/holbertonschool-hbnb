
## Introduction: HBnB Evolution


**HBnB Evolution is a modern hospitality platform designed to facilitate secure, scalable, and efficient short-term accommodation booking. Built on clean software architecture principles, the system connects hosts and guests through a reliable and well-structured digital ecosystem while ensuring maintainability, performance, and extensibility.**

*This document presents the technical architecture and design foundations that support both current system requirements and future evolution.*

---

## HBnB Evolution: Architectural Overview
---
**System Architecture**
HBnB Evolution follows a three-layer architecture designed for scalability, maintainability, and clean separation of concerns. The system implements the Facade Pattern to simplify complex interactions between components.

---
## Architectural Layers

1. Presentation Layer
Purpose: Handles all user interactions and HTTP communications

Components:

RESTful API endpoints (UserAPI, PlaceAPI, ReviewAPI, etc.)

Request/Response processing and validation

JSON/XML formatting and error handling

Responsibility: User interface, input sanitization, and response delivery

## 2. Business Logic Layer
Purpose: Contains core business rules and entity management

Key Component: HbnbFacade - A simplified interface coordinating complex operations

Entities:

User: Authentication, authorization, profile management

Place: Property listings, availability, pricing logic

Review: Rating system, validation, moderation

Booking: Reservation management, financial operations

Amenity: Property features and facilities

Responsibility: Business rules validation, entity coordination, workflow management

## 3. Persistence Layer
Purpose: Manages data storage and retrieval

Components:

Repositories: Data access abstraction (UserRepository, PlaceRepository, etc.)

Database: PostgreSQL/MySQL with optimized schema

Responsibility: Data persistence, query optimization, transaction management

Communication Flow
The system uses a simplified request flow through the Facade Pattern:

API Request → HbnbFacade → [Business Logic Coordination] → Repository → Database

Instead of API calling multiple models and repositories directly, we use API calls simple Facade methods that handle complex coordination internally.

## Core Business Entities
BaseEntity (Template Method Pattern)
Purpose: Foundation for all domain entities

Features:

UUID-based unique identifiers

Automatic audit trails (created_at, updated_at)

Consistent CRUD operations

Design Principle: DRY (Don't Repeat Yourself) across all entities

User Management
Roles: Guests, Hosts, Administrators

## Key Features:

Multi-factor authentication

Role-based access control

Profile and account lifecycle management

Security: Email verification, password policies, session management

## Place Management

Lifecycle: Creation → Publication → Booking → Archiving

Features:

Dynamic pricing with seasonal rates

Real-time availability checking

Amenity-based categorization

## Review and rating aggregation

Rules: Only published places are bookable; owners control availability

Review System
Validation: Verified stays only, time-bound submissions

Structure: Multi-criteria ratings (cleanliness, accuracy, etc.)

Moderation: Automated and manual review processes

Integrity: One review per verified booking


## Amenity Management

Categorization: Kitchen, bathroom, entertainment, etc.

Pricing: Included vs. additional-cost amenities

Association: Many-to-many relationship with places

Filtering: Enables advanced property search

## Entity Relationships & Constraints

**Key Relationships**

User → Place (1:Many): Owners manage multiple properties


Place → Review (1:Many): Properties receive multiple reviews


User → Review (1:Many): Users write multiple reviews


Place ↔ Amenity (Many:Many): Properties offer multiple amenities


## Business Rule Enforcement

Data Integrity: Foreign key constraints, unique constraints, check constraints

Temporal Rules: Review windows, booking advance limits, cancellation periods

Quantitative Limits: Maximum concurrent bookings, review frequency limits

State Management: User activation, place publication status, booking states


## API Workflow Examples

**1. User Registration**

Client → API → Service → Facade → [User Validation] → Repository → Database

Key Steps: Email uniqueness check, password hashing, verification email

Validation: Duplicate prevention, data integrity, security compliance

**2. Place Creation**

Client → API → Service → Facade → [Owner Verification + Place Validation] → Repository → Database

Key Steps: Owner authentication, place data validation, amenity association

Validation: Owner eligibility, pricing rules, amenity compatibility

**3. Review Submission**

Client → API → Service → Facade → [Booking Verification + Review Validation] → Repository → Database

Key Steps: Verified stay confirmation, duplicate review prevention, rating calculation

Validation: Stay verification, time window compliance, content moderation

**4. Place Search**

Client → API → Service → Facade → [Filter Processing] → Repository → [Database Query] → Response Assembly

Key Steps: Filter parsing, availability checking, amenity matching

Optimization: Pagination, caching, eager loading of amenities

## Design Principles

**SOLID Compliance**

Single Responsibility: Each class has one reason to change

Open/Closed: Extensible without modification

Liskov Substitution: Derived classes substitutable for base classes

Interface Segregation: Client-specific interfaces

Dependency Inversion: Depend on abstractions, not concretions

## Patterns Implemented

Facade Pattern: Simplified interface to complex subsystem

Template Method Pattern: Consistent entity lifecycle in BaseEntity

Repository Pattern: Abstract data access layer

Strategy Pattern: Pluggable pricing and validation algorithms

## Performance Considerations

**Database Optimization**

Indexing: Foreign keys, frequently queried fields

Partitioning: Temporal data (reviews) by date

Caching: Frequently accessed places, user sessions

Connection Pooling: Efficient database connection management

## API Performance

Pagination: Large result sets divided into pages

Lazy Loading: Related entities loaded on demand

Response Compression: Reduced bandwidth usage

Rate Limiting: API endpoint protection

## Security Measures

**Authentication & Authorization**

JWT Tokens: Stateless session management

Role-Based Access: Granular permission control

Input Validation: SQL injection prevention, XSS protection

Data Encryption: Sensitive data at rest and in transit

## Business Logic Security

Ownership Verification: Users can only modify their own resources

State Transitions: Controlled entity state changes

Financial Integrity: Auditable booking and payment trails

Content Moderation: Review and messaging oversight

## Scalability Features

Horizontal Scaling

Stateless API Layer: Easy replication

Database Read Replicas: Load distribution

Caching Layer: Redis/Memcached for frequent queries

Message Queues: Asynchronous processing for emails, notifications

Microservices Readiness
Clear Bounded Contexts: Natural service boundaries

API-First Design: RESTful, versioned endpoints

Event-Driven Architecture: Placeholder for future event bus implementation

## Monitoring & Maintenance 
Observability
Logging: Structured logging for debugging and audit trails

Metrics: API response times, database query performance

Health Checks: System component availability monitoring

Alerting: Proactive issue detection and notification

Maintenance Features
Database Migrations: Version-controlled schema changes

Backup Strategy: Regular data backups with point-in-time recovery

Deployment Pipeline: CI/CD for consistent releases

Feature Flags: Gradual feature rollouts and A/B testing

Integration Points
External Services
Payment Gateways: Stripe/PayPal integration for transactions

Email Service: SendGrid/Mailgun for notifications

SMS Service: Twilio for two-factor authentication

Mapping Service: Google Maps/Mapbox for location services

## Third-Party APIs
Identity Verification: Background checks for hosts

Payment Processing: Secure transaction handling

Review Aggregation: Cross-platform reputation import

Analytics Integration: Usage tracking and business intelligence

*This architecture provides a robust foundation for HBnB Evolution, balancing flexibility with structure, and enabling both current functionality and future growth. The clear separation of concerns, consistent patterns, and comprehensive validation ensure a maintainable, scalable, and secure platform for property rentals and bookings.*

## Contributors 

- *Raghad Almalki* – https://github.com/Raghad717  
- *Rama Alshehri* – https://github.com/csrama  
- *Jana Bakri* – https://github.com/janabakri

- # HBnB - RESTful API Backend

- ## Overview

HBnB is a simplified Airbnb-like backend system developed as part of the Holberton School curriculum. This project implements a fully functional RESTful API that manages users, places, reviews, and amenities using clean architecture principles and industry best practices.

## Features

- Full CRUD operations for all resources
- Structured JSON responses with consistent formatting
- Comprehensive input validation and error handling
- Secure password hashing using hashlib
- UUID-based identifiers for all resources
- Swagger API documentation for easy testing
- Modular and scalable three-layer architecture
- Unit tests with pytest for reliability

## Architecture

The project follows a Three-Layer Architecture pattern:

| Layer | Responsibility | Key Components |
|-------|----------------|-----------------|
| Presentation | API endpoints and request handling | Flask routes, request parsing, response formatting |
| Business Logic | Core rules and validations | Data validation, business rules, authorization |
| Persistence | Data storage and retrieval | In-memory storage, data models, CRUD operations |

## Technologies

- Python 3.8+ - Core programming language
- Flask - Lightweight web framework
- Flask-RESTx - API documentation and validation
- Pytest - Unit testing framework
- UUID - Unique identifier generation
- hashlib - Password hashing and security

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | Retrieve all users |
| POST | `/users` | Create a new user |
| GET | `/users/{id}` | Retrieve a specific user |
| PUT | `/users/{id}` | Update a user |
| DELETE | `/users/{id}` | Delete a user |

### Places
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/places` | Retrieve all places |
| POST | `/places` | Create a new place |
| GET | `/places/{id}` | Retrieve a specific place |
| PUT | `/places/{id}` | Update a place |
| DELETE | `/places/{id}` | Delete a place |

### Reviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reviews` | Retrieve all reviews |
| POST | `/reviews` | Create a new review |
| GET | `/reviews/{id}` | Retrieve a specific review |
| PUT | `/reviews/{id}` | Update a review |
| DELETE | `/reviews/{id}` | Delete a review |

### Amenities
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/amenities` | Retrieve all amenities |
| POST | `/amenities` | Create a new amenity |
| GET | `/amenities/{id}` | Retrieve a specific amenity |
| PUT | `/amenities/{id}` | Update an amenity |
| DELETE | `/amenities/{id}` | Delete an amenity |
---

---

# Part 3 – Database Schema & API Expansion

## Overview

Part 3 of the **HBnB Evolution** project focuses on transforming the system from a simple in-memory architecture into a **structured relational data model** with clearly defined relationships between entities.

This stage introduces:

* A relational database schema
* Entity relationship visualization
* Structured API interactions with persistent data
* Clear documentation of data relationships

The goal is to ensure that the system architecture remains **scalable, maintainable, and aligned with real-world backend design practices**.

---

# Database Schema Design

The database is designed using a **relational model** where each entity is represented as a table and relationships are enforced through **foreign keys and association tables**.

The main entities included in the schema are:

* **User**
* **Place**
* **Review**
* **Amenity**
* **Place_Amenity** (association table)

Each entity extends the base attributes defined in **BaseEntity**, ensuring consistency across the system.

### BaseEntity Fields

| Field      | Type     | Description           |
| ---------- | -------- | --------------------- |
| id         | UUID     | Unique identifier     |
| created_at | datetime | Creation timestamp    |
| updated_at | datetime | Last update timestamp |

---

# Entity Relationship Diagram (ERD)

The following diagram represents the database schema and the relationships between all entities in the HBnB system.

```mermaid
erDiagram

USER {
    UUID id
    string first_name
    string last_name
    string email
    string password
    boolean is_admin
    datetime created_at
    datetime updated_at
}

PLACE {
    UUID id
    string title
    string description
    float price
    float latitude
    float longitude
    UUID owner_id
    datetime created_at
    datetime updated_at
}

REVIEW {
    UUID id
    string text
    int rating
    UUID user_id
    UUID place_id
    datetime created_at
    datetime updated_at
}

AMENITY {
    UUID id
    string name
    datetime created_at
    datetime updated_at
}

PLACE_AMENITY {
    UUID place_id
    UUID amenity_id
}

USER ||--o{ PLACE : owns
USER ||--o{ REVIEW : writes
PLACE ||--o{ REVIEW : receives
PLACE ||--o{ PLACE_AMENITY : has
AMENITY ||--o{ PLACE_AMENITY : includes
```

---

# Relationship Explanation

### User → Place (One-to-Many)

A **user can own multiple places**, but each place belongs to **one owner only**.

Example:

```
User (Host)
 ├── Place 1
 ├── Place 2
 └── Place 3
```

---

### User → Review (One-to-Many)

A user can write multiple reviews for different places.

```
User
 ├── Review for Place A
 ├── Review for Place B
 └── Review for Place C
```

---

### Place → Review (One-to-Many)

Each place can receive multiple reviews from different users.

```
Place
 ├── Review 1
 ├── Review 2
 └── Review 3
```

---

### Place ↔ Amenity (Many-to-Many)

A place can have multiple amenities, and each amenity can belong to multiple places.

This relationship is implemented using the **Place_Amenity association table**.

Example:

```
Place
 ├── WiFi
 ├── Pool
 └── Parking
```

Another place may share the same amenities.

---

# Association Table: Place_Amenity

The **Place_Amenity** table is used to manage the many-to-many relationship between places and amenities.

| Field      | Description           |
| ---------- | --------------------- |
| place_id   | References a place    |
| amenity_id | References an amenity |

Example:

| place_id | amenity_id |
| -------- | ---------- |
| 1        | WiFi       |
| 1        | Pool       |
| 2        | WiFi       |

---

# API Integration with Database

In Part 3, the API endpoints interact with the database through the **Repository Pattern** and the **Facade Layer**.

### Request Flow

```
Client Request
     ↓
API Endpoint
     ↓
HBnBFacade
     ↓
Repository Layer
     ↓
Database
```

This architecture ensures that:

* The **API layer remains simple**
* Business logic stays centralized
* Database access remains modular and maintainable

---

# Benefits of the Schema Design

This relational schema provides several advantages:

### Data Integrity

Foreign keys ensure that relationships remain valid.

### Scalability

New entities (such as bookings or payments) can be easily added.

### Query Optimization

Indexes and relational joins allow efficient queries.

### Maintainability

The separation between entities simplifies updates and debugging.

---

# Documentation

Additional documentation for the API endpoints can be found in:

```
API_DOCUMENTATION.md
```

This document includes:

* Endpoint descriptions
* Request/response formats
* Example API calls
* Error handling documentation

---

# Conclusion

Part 3 completes the transformation of HBnB into a **fully structured backend system with a relational database model**.

With the introduction of:

* a normalized schema
* entity relationship diagrams
* clear API integration

the platform now provides a strong foundation for future development, including booking systems, payments, and large-scale deployment.

---
 
## Contributors 

- *Raghad Almalki* – https://github.com/Raghad717  
- *Rama Alshehri* – https://github.com/csrama  
- *Jana Bakri* – https://github.com/janabakri
