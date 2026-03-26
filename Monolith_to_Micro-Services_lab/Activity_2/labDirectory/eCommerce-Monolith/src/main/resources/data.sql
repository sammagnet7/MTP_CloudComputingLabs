-- 1. CLEANUP (Only for static data tables)
-- We skip deleting from cart/order tables to avoid "Table Not Found" errors on startup
DELETE FROM review;
DELETE FROM inventory;
DELETE FROM product;
DELETE FROM users;
DELETE FROM category;

-- 2. INSERT DATA

-- Categories
INSERT INTO category (id, name) VALUES (1, 'Electronics');
INSERT INTO category (id, name) VALUES (2, 'Books');
INSERT INTO category (id, name) VALUES (3, 'Accessories');

-- Users (Little Buddha is ID 1 to match default Frontend Login)
INSERT INTO users (id, name, email, address) VALUES (1, 'Little Buddha', 'buddha@zen.com', '108 Nirvana Lane, Highland');
INSERT INTO users (id, name, email, address) VALUES (2, 'Alice Dev', 'alice@test.com', '123 Monolith St');
INSERT INTO users (id, name, email, address) VALUES (3, 'Bob Ops', 'bob@test.com', '456 Microservice Ave');

-- Products
INSERT INTO product (id, name, description, price, category_id) VALUES (1, 'Smartphone', 'Latest model with 5G and AI camera', 699.00, 1);
INSERT INTO product (id, name, description, price, category_id) VALUES (2, 'Laptop', 'High performance developer machine', 1200.00, 1);
INSERT INTO product (id, name, description, price, category_id) VALUES (3, 'Microservices Book', 'Learn how to break monoliths safely', 45.00, 2);
INSERT INTO product (id, name, description, price, category_id) VALUES (4, 'Wireless Headphones', 'Noise cancelling over-ear headphones', 250.00, 1);
INSERT INTO product (id, name, description, price, category_id) VALUES (5, 'Mechanical Keyboard', 'RGB Backlit with Cherry MX Red switches', 120.00, 3);
INSERT INTO product (id, name, description, price, category_id) VALUES (6, '4K Monitor', '27-inch Ultra HD display for coding', 350.00, 1);
INSERT INTO product (id, name, description, price, category_id) VALUES (7, 'Clean Code Book', 'A Handbook of Agile Software Craftsmanship', 50.00, 2);
INSERT INTO product (id, name, description, price, category_id) VALUES (8, 'Ergonomic Mouse', 'Vertical mouse to prevent wrist strain', 40.00, 3);

-- Inventory (Stock)
INSERT INTO inventory (id, product_id, quantity) VALUES (1, 1, 50);
INSERT INTO inventory (id, product_id, quantity) VALUES (2, 2, 20);
INSERT INTO inventory (id, product_id, quantity) VALUES (3, 3, 100);
INSERT INTO inventory (id, product_id, quantity) VALUES (4, 4, 30);
INSERT INTO inventory (id, product_id, quantity) VALUES (5, 5, 15);
INSERT INTO inventory (id, product_id, quantity) VALUES (6, 6, 10);
INSERT INTO inventory (id, product_id, quantity) VALUES (7, 7, 60);
INSERT INTO inventory (id, product_id, quantity) VALUES (8, 8, 45);

-- ⭐ REVIEWS (Expanded)
-- Smartphone (ID 1)
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (1, 1, 'TechReviewer', 5, 'Great battery life, lasts 2 days!', CURRENT_TIMESTAMP);
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (2, 1, 'Alice Dev', 4, 'Good, but a bit expensive for the specs.', CURRENT_TIMESTAMP);
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (3, 1, 'PhotoPro', 5, 'The AI camera night mode is insane.', CURRENT_TIMESTAMP);

-- Laptop (ID 2)
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (4, 2, 'DevDave', 5, 'Compiles my monolithic Java app in seconds!', CURRENT_TIMESTAMP);
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (5, 2, 'MobileWarrior', 3, 'Battery life is average when running Docker containers.', CURRENT_TIMESTAMP);

-- Microservices Book (ID 3)
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (6, 3, 'Bob Ops', 5, 'Changed my career. A must-read.', CURRENT_TIMESTAMP);
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (7, 3, 'Student101', 4, 'Concepts are great, but examples are dense.', CURRENT_TIMESTAMP);

-- Headphones (ID 4)
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (8, 4, 'Audiophile', 3, 'Bass is too heavy for classical music.', CURRENT_TIMESTAMP);
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (9, 4, 'Commuter', 5, 'Noise cancellation is a lifesaver on the train.', CURRENT_TIMESTAMP);

-- Keyboard (ID 5)
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (10, 5, 'GamerOne', 5, 'Clicky keys are satisfying. RGB is bright.', CURRENT_TIMESTAMP);
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (11, 5, 'OfficeWorker', 2, 'Too loud for the office, coworkers hate me.', CURRENT_TIMESTAMP);

-- Monitor (ID 6)
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (12, 6, 'PixelPeepers', 4, 'Colors are accurate, but the stand is a bit wobbly.', CURRENT_TIMESTAMP);
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (13, 6, 'DualScreenGuy', 5, 'Bought two of these. Productivity skyrocketed.', CURRENT_TIMESTAMP);

-- Clean Code Book (ID 7)
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (14, 7, 'JuniorDev', 5, 'Every developer must read this at least once.', CURRENT_TIMESTAMP);

-- Mouse (ID 8)
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (15, 8, 'CarpalTunnelSurvivor', 5, 'My wrist pain vanished after two days.', CURRENT_TIMESTAMP);
INSERT INTO review (id, product_id, user_name, rating, comment, created_at) VALUES (16, 8, 'ClickyFan', 4, 'Takes some getting used to, but very comfortable.', CURRENT_TIMESTAMP);

-- 🛒 DUMMY ORDERS (For Little Buddha)

-- Order #1: A Laptop and a Mouse (Total: 1240)
INSERT INTO orders (id, user_id, total_amount, status, created_at) VALUES (1, 1, 1240.00, 'PAID', CURRENT_TIMESTAMP);
-- Order Items for Order #1
INSERT INTO order_item (id, order_id, product_id, product_name, price, quantity) VALUES (1, 1, 2, 'Laptop', 1200.00, 1);
INSERT INTO order_item (id, order_id, product_id, product_name, price, quantity) VALUES (2, 1, 8, 'Ergonomic Mouse', 40.00, 1);
-- Payment for Order #1
INSERT INTO payment (id, order_id, amount, status, transaction_id) VALUES (1, 1, 1240.00, 'SUCCESS', 'TXN_BUDDHA_001');

-- Order #2: A Book (Total: 50)
INSERT INTO orders (id, user_id, total_amount, status, created_at) VALUES (2, 1, 50.00, 'DELIVERED', CURRENT_TIMESTAMP);
-- Order Items for Order #2
INSERT INTO order_item (id, order_id, product_id, product_name, price, quantity) VALUES (3, 2, 7, 'Clean Code Book', 50.00, 1);
-- Payment for Order #2
INSERT INTO payment (id, order_id, amount, status, transaction_id) VALUES (2, 2, 50.00, 'SUCCESS', 'TXN_BUDDHA_002');

-- 3. RESET COUNTERS
ALTER TABLE category ALTER COLUMN id RESTART WITH 4;
ALTER TABLE users ALTER COLUMN id RESTART WITH 4;
ALTER TABLE product ALTER COLUMN id RESTART WITH 9;
ALTER TABLE inventory ALTER COLUMN id RESTART WITH 9;
ALTER TABLE review ALTER COLUMN id RESTART WITH 17; -- ✅ Updated for new reviews
ALTER TABLE orders ALTER COLUMN id RESTART WITH 3;
ALTER TABLE order_item ALTER COLUMN id RESTART WITH 4;
ALTER TABLE payment ALTER COLUMN id RESTART WITH 3;