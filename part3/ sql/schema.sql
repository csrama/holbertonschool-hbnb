-- HBnB Database Schema
-- Compatible with MySQL and SQLite

-- Create database
CREATE DATABASE IF NOT EXISTS hbnb_db;
USE hbnb_db;

-- =====================================================
-- Table: accounts (users)
-- =====================================================
CREATE TABLE IF NOT EXISTS accounts (
    user_id VARCHAR(36) PRIMARY KEY,
    given_name VARCHAR(50) NOT NULL,
    family_name VARCHAR(50) NOT NULL,
    email_address VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    is_administrator BOOLEAN DEFAULT FALSE,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_accounts_email (email_address),
    INDEX idx_accounts_name (given_name, family_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: facilities (amenities)
-- =====================================================
CREATE TABLE IF NOT EXISTS facilities (
    facility_id VARCHAR(36) PRIMARY KEY,
    facility_name VARCHAR(50) NOT NULL UNIQUE,
    facility_description VARCHAR(250),
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_facilities_name (facility_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: properties (places)
-- =====================================================
CREATE TABLE IF NOT EXISTS properties (
    property_id VARCHAR(36) PRIMARY KEY,
    property_title VARCHAR(100) NOT NULL,
    property_description TEXT,
    nightly_rate DECIMAL(10, 2) NOT NULL,
    location_latitude DECIMAL(10, 8) NOT NULL,
    location_longitude DECIMAL(11, 8) NOT NULL,
    owner_id VARCHAR(36) NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (owner_id) REFERENCES accounts(user_id) ON DELETE CASCADE,
    
    INDEX idx_properties_owner (owner_id),
    INDEX idx_properties_location (location_latitude, location_longitude),
    INDEX idx_properties_price (nightly_rate)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: feedbacks (reviews)
-- =====================================================
CREATE TABLE IF NOT EXISTS feedbacks (
    feedback_id VARCHAR(36) PRIMARY KEY,
    comment TEXT NOT NULL,
    score INT NOT NULL CHECK (score BETWEEN 1 AND 5),
    author_id VARCHAR(36) NOT NULL,
    property_id VARCHAR(36) NOT NULL,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (author_id) REFERENCES accounts(user_id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(property_id) ON DELETE CASCADE,
    
    UNIQUE KEY unique_user_property_review (author_id, property_id),
    
    INDEX idx_feedbacks_author (author_id),
    INDEX idx_feedbacks_property (property_id),
    INDEX idx_feedbacks_rating (score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: property_facility (many-to-many relationship)
-- =====================================================
CREATE TABLE IF NOT EXISTS property_facility (
    property_id VARCHAR(36) NOT NULL,
    facility_id VARCHAR(36) NOT NULL,
    added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (property_id, facility_id),
    FOREIGN KEY (property_id) REFERENCES properties(property_id) ON DELETE CASCADE,
    FOREIGN KEY (facility_id) REFERENCES facilities(facility_id) ON DELETE CASCADE,
    
    INDEX idx_property_facility_facility (facility_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
