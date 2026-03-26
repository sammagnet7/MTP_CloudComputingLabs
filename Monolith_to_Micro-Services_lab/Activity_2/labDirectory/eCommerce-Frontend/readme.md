# 🛍️ Monolith to Microservices: Strangler Fig Migration

This repository demonstrates a complete transformation of a legacy **Java Spring Boot Monolith** into a distributed **Microservices Architecture**.

The application uses the **Strangler Fig Pattern** to incrementally replace functionality. The frontend (Vue.js) acts as a **BFF (Backend for Frontend)**, aggregating data from **6 distributed services** to create a seamless user experience.

---

## 🏗️ Architecture Overview

The system is split into polyglot microservices (Java & Python) communicating via REST.

| Service | Port | Tech Stack | Role | Dependencies |
| --- | --- | --- | --- | --- |
| **Monolith** | `30000` | Java / Spring | **Monolith eCommerce** |  |
| **Inventory** | `30001` | Java / Postgres | **Stock Management** | Database-per-service pattern. |
| **Product** | `30002` | Python / FastAPI | **Catalog** | Single Source of Truth for products. |
| **Order** | `30003` | Java / H2 | **Orchestrator** | Coordinates Checkout (Cart → Pay → Stock). |
| **Payment** | `30004` | Python / SQLite | **Transactions** | Mock payment gateway. |
| **Reviews** | `30006` | Node / Express* | **User Sentiment** | Verifies IDs with **Product Service**. |

*(Note: Reviews service tech stack is illustrative; works with any HTTP server).*

---

## 📋 Prerequisites

* **Java:** JDK 17+
* **Python:** 3.9+
* **Docker:** Recommended for databases.
* **Node.js:** (Optional, if running Reviews locally without Docker)

---

## 🚀 How to Run

### 1. Start Infrastructure (Databases)

Ensure PostgreSQL is running for the Inventory Service.

```bash
docker run --name inventory-db \
  -e POSTGRES_DB=inventorydb \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:15

```

### 2. Start Services

Open separate terminals for each service:

1. **Monolith (Frontend Host):**
`cd eCommerce-Monolith && ./mvnw spring-boot:run`
2. **Inventory Service:**
`cd eCommerce-InventoryService && ./mvnw spring-boot:run`
3. **Product Catalog:**
`cd eCommerce-ProductService && uvicorn main:app --port 30002`
4. **Order Service:**
`cd eCommerce-OrderService && ./mvnw spring-boot:run`
5. **Payment Service:**
`cd eCommerce-PaymentService && uvicorn main:app --port 30004`
6. **Reviews Service:**
`cd eCommerce-ReviewsService && npm start` (or equivalent python command)

### 3. Access the Application

Open **[http://localhost:30000](https://www.google.com/search?q=http://localhost:30000)** in your browser.

* **Note:** The HTML file now loads logic from `script.js`. Ensure your browser cache is cleared if updates don't appear.

---

## 📡 API Reference

### 1. 🐍 Product Catalog (`:30002`)

*Single source of truth for item details.*

* `GET /api/v2/products` - List all products.
* `GET /api/v2/products/{id}` - Get details (Name, Price, Desc).

### 2. ☕ Inventory Service (`:30001`)

*Manages stock levels atomically.*

* `GET /api/v2/inventory/{id}` - Get live stock count (int).
* `POST /api/v2/inventory/reduce` - Deduct stock.
* **Payload:** `{ "productId": 1, "quantity": 1 }`



### 3. ⭐ Reviews Service (`:30006`) **(NEW)**

*Manages user ratings. Decoupled from Catalog.*

* `GET /api/v2/reviews/products/{id}` - Get all reviews for a product.
* `POST /api/v2/reviews/products/{id}` - Add a review.
* **Payload:** `{ "userName": "Alice", "rating": 5, "comment": "Great!" }`
* *Constraint:* Validates `productId` against **Product Service** before saving.



### 4. 🧠 Order Service (`:30003`)

*The Central Nervous System. Orchestrates the checkout transaction.*

* `POST /api/v2/orders/cart/{uid}/add` - Add item to cart.
* `POST /api/v2/orders/checkout/{uid}` - **Trigger Checkout.**
* *Flow:* Validates Price (Product Svc) -> Deducts Stock (Inventory Svc) -> Charges Card (Payment Svc) -> Saves Order.


* `GET /api/v2/orders/users/{uid}` - Get order history.

### 5. 💳 Payment Service (`:30004`)

*Handles monetary transactions.*

* `POST /api/v2/payments/` - Process payment.
* `GET /api/v2/payments/users/{uid}` - Get transaction history.

