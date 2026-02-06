-- 1. CLEANUP
DELETE FROM payment;
DELETE FROM review;
DELETE FROM inventory;
DELETE FROM product;
DELETE FROM category;
DELETE FROM users;

-- 2. INSERT DATA
-- Categories
INSERT INTO category (id, name) VALUES (1, 'Electronics');
INSERT INTO category (id, name) VALUES (2, 'Books');

-- Users
INSERT INTO users (id, name, email, address) VALUES (1, 'Alice Dev', 'alice@test.com', '123 Monolith St');
INSERT INTO users (id, name, email, address) VALUES (2, 'Bob Ops', 'bob@test.com', '456 Microservice Ave');

-- Products
INSERT INTO product (id, name, description, price, category_id) VALUES (1, 'Smartphone', 'Latest model with 5G and AI camera', 699.00, 1);
INSERT INTO product (id, name, description, price, category_id) VALUES (2, 'Laptop', 'High performance developer machine', 1200.00, 1);
INSERT INTO product (id, name, description, price, category_id) VALUES (3, 'Microservices Book', 'Learn how to break monoliths safely', 45.00, 2);

-- Inventory
INSERT INTO inventory (id, product_id, quantity) VALUES (1, 1, 50);
INSERT INTO inventory (id, product_id, quantity) VALUES (2, 2, 20);
INSERT INTO inventory (id, product_id, quantity) VALUES (3, 3, 100);

-- Reviews
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (1, 1, 'TechReviewer', 5, 'Great battery life!', CURRENT_TIMESTAMP);
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (2, 1, 'Alice Dev', 4, 'Good, but expensive.', CURRENT_TIMESTAMP);
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (3, 3, 'Bob Ops', 5, 'Changed my career.', CURRENT_TIMESTAMP);

-- 3. RESET COUNTERS (The Fix)
ALTER TABLE category ALTER COLUMN id RESTART WITH 3;
ALTER TABLE users ALTER COLUMN id RESTART WITH 3;
ALTER TABLE product ALTER COLUMN id RESTART WITH 4;
ALTER TABLE inventory ALTER COLUMN id RESTART WITH 4;
ALTER TABLE review ALTER COLUMN id RESTART WITH 4;