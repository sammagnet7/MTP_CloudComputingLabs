
-- 2. INSERT DATA
-- 🛒 DUMMY ORDERS (For Little Buddha)

-- Order #1: A Laptop and a Mouse (Total: 1240)
INSERT INTO orders (id, user_id, total_amount, status, created_at) VALUES (1, 1, 1240.00, 'PAID', CURRENT_TIMESTAMP);
-- Order Items for Order #1
INSERT INTO order_item (id, order_id, product_id, product_name, price, quantity) VALUES (1, 1, 2, 'Laptop', 1200.00, 1);
INSERT INTO order_item (id, order_id, product_id, product_name, price, quantity) VALUES (2, 1, 8, 'Ergonomic Mouse', 40.00, 1);

-- Order #2: A Book (Total: 50)
INSERT INTO orders (id, user_id, total_amount, status, created_at) VALUES (2, 1, 50.00, 'DELIVERED', CURRENT_TIMESTAMP);
-- Order Items for Order #2
INSERT INTO order_item (id, order_id, product_id, product_name, price, quantity) VALUES (3, 2, 7, 'Clean Code Book', 50.00, 1);


-- 3. RESET COUNTERS
ALTER TABLE orders ALTER COLUMN id RESTART WITH 3;
ALTER TABLE order_item ALTER COLUMN id RESTART WITH 4;
    