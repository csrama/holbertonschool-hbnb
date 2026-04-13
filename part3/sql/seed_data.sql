-- Admin User
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '1', 'Admin', 'User', 'admin@hbnb.com',
    '$2b$12$examplehashedpassword123', -- 
    TRUE
);

-- Sample Amenities
INSERT INTO amenities (id, name, description) VALUES
('1', 'WiFi', 'Wireless Internet'),
('2', 'Pool', 'Swimming Pool'),
('3', 'Air Conditioning', 'AC in all rooms');

-- Sample Place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES
('1', 'Cozy Apartment', 'Nice and cozy', 100.0, 24.7136, 46.6753, '1');

-- Sample Review
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES
('1', 'Great place!', 5, '1', '1');

-- Link Place to Amenities
INSERT INTO place_amenity (place_id, amenity_id) VALUES
('1', '1'),
('1', '2');
