-- 🏷️ Categories
INSERT INTO category (id, name) VALUES (1, 'Electronics');
INSERT INTO category (id, name) VALUES (2, 'Books');
INSERT INTO category (id, name) VALUES (3, 'Home & Kitchen');

-- 👤 Users
INSERT INTO users (id, name, email, address) VALUES (1, 'Alice Dev', 'alice@test.com', '123 Monolith St');
INSERT INTO users (id, name, email, address) VALUES (2, 'Bob Ops', 'bob@test.com', '456 Microservice Ave');
INSERT INTO users (id, name, email, address) VALUES (3, 'Charlie Tester', 'charlie@test.com', '789 QA Blvd');

-- 📦 Products
-- Note: category_id refers to the IDs created above
INSERT INTO product (id, name, price, stock, category_id) VALUES (1, 'Smartphone', 699.00, 50, 1);
INSERT INTO product (id, name, price, stock, category_id) VALUES (2, 'Laptop', 1200.00, 20, 1);
INSERT INTO product (id, name, price, stock, category_id) VALUES (3, 'Wireless Mouse', 25.00, 100, 1);
INSERT INTO product (id, name, price, stock, category_id) VALUES (4, 'Microservices Patterns', 45.00, 30, 2);
INSERT INTO product (id, name, price, stock, category_id) VALUES (5, 'Clean Code', 40.00, 25, 2);
INSERT INTO product (id, name, price, stock, category_id) VALUES (6, 'Coffee Maker', 89.99, 15, 3);