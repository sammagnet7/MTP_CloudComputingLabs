-- 1. CLEANUP (Only for static data tables)
DELETE FROM inventory;


-- 2. INSERT DATA
-- Initial Data for Postgres
INSERT INTO inventory (product_id, quantity) VALUES (1, 50);  -- Smartphone
INSERT INTO inventory (product_id, quantity) VALUES (2, 20);  -- Laptop
INSERT INTO inventory (product_id, quantity) VALUES (3, 100); -- Microservices Book
INSERT INTO inventory (product_id, quantity) VALUES (4, 30);  -- Headphones
INSERT INTO inventory (product_id, quantity) VALUES (5, 15);  -- Keyboard
INSERT INTO inventory (product_id, quantity) VALUES (6, 10);  -- Monitor
INSERT INTO inventory (product_id, quantity) VALUES (7, 60);  -- Clean Code Book
INSERT INTO inventory (product_id, quantity) VALUES (8, 45);  -- Mouse


-- 3. RESET COUNTERS
ALTER TABLE inventory ALTER COLUMN id RESTART WITH 9;
    