# 🛍️ E-Commerce Monolith App

This repository contains a **Sample Monolithic Application** designed for "Monolith to Microservices" migration demos. It handles User Management, Products, Inventory, Cart, Orders, and Mock Payments in a single Spring Boot application.

The frontend is a built-in **Single Page Application (SPA)** using Vue.js & Tailwind CSS.

---

## 📋 Prerequisites

* **Java:** JDK 17 or higher.
* **Docker:** (Optional) For containerization demos.

---

## 🏃‍♂️ How to Run

### Option A: Local Run (Java)

1. Open your terminal in the project root.
2. Run the application:
* **Mac/Linux:** `./mvnw clean spring-boot:run`
* **Windows:** `mvnw clean spring-boot:run`


3. The app will start on **port 30000**.

### Option B: Run with Docker

1. **Build:** `docker build --no-cache -t monolith-shop .`
2. **Run:** `docker run -p 30000:30000 monolith-shop`

---

## 💻 Web UI (Frontend)

The application serves a Vue.js frontend directly.

1. Open browser to: **[http://localhost:30000](https://www.google.com/search?q=http://localhost:30000)**
2. **Default Login:** You are automatically logged in as **"Little Buddha" (User ID 1)**.
3. **Features:**
* Browse Products (prices in **Rs.**).
* View Details (Live Stock + Reviews).
* **Dashboard:** View Order History & Download Receipts.



---

## 🔌 API Endpoints

**Base URL:** `http://localhost:30000/api`

### 📦 Products & Catalog

| Method | Endpoint | Description |
| --- | --- | --- |
| **GET** | `/products` | List all available products. |
| **GET** | `/products/{id}` | Get detailed info (includes Stock & Reviews). |
| **POST** | `/products/{id}/reviews` | Add a review (`userName`, `rating`, `comment`). |

### 🛒 Shopping & Checkout

| Method | Endpoint | Description |
| --- | --- | --- |
| **GET** | `/users` | List all users. |
| **POST** | `/cart/{userId}/add` | Add item to cart (`productId`, `quantity`). |
| **POST** | `/checkout/{userId}` | **(Transactional)** Place order, deduct stock, charge payment. |

### 📜 History & Profile

| Method | Endpoint | Description |
| --- | --- | --- |
| **GET** | `/users/{userId}/orders` | Get full order history for a user. |
| **GET** | `/orders/{orderId}` | Get itemized receipt of a specific order. |
| **GET** | `/users/{userId}/payments` | View all past transaction records. |

---

## 💾 Pre-Loaded Data (H2 Database)

The database is reset on every restart.

### 👤 Default User

| ID | Name | Role |
| --- | --- | --- |
| `1` | **Little Buddha** | Default Login (Premium Member) |
| `2` | Alice Dev | Demo User |

### 📦 Key Products

| ID | Name | Price | Stock |
| --- | --- | --- | --- |
| `1` | Smartphone | Rs. 699.00 | 50 |
| `2` | Laptop | Rs. 1200.00 | 20 |
| `5` | Mechanical Keyboard | Rs. 120.00 | 15 |
| `8` | Ergonomic Mouse | Rs. 40.00 | 45 |

---

## 🧪 Quick Test (cURL)

Simulate a full purchase flow for **Little Buddha (User 1)** using the terminal.

### 1. View Product Details

Fetches aggregated data (Product + Review + Inventory).

```bash
curl -s http://localhost:30000/api/products/1 | json_pp

```

### 2. Post a Review

```bash
curl -X POST http://localhost:30000/api/products/1/reviews \
  -H "Content-Type: application/json" \
  -d '{"userName": "Little Buddha", "rating": 5, "comment": "Best purchase ever!"}'

```

### 3. Purchase Flow (Transactional)

Add the **Smartphone** to cart and checkout.

```bash
# Add to Cart
curl -X POST http://localhost:30000/api/cart/1/add \
  -H "Content-Type: application/json" \
  -d '{"productId": 1, "quantity": 1}'

# Checkout (Triggers Payment & Stock Reduction)
curl -X POST http://localhost:30000/api/checkout/1 | json_pp

```

---

## 🛠️ Database Console

Inspect the raw tables and relationships.

1. **URL:** [http://localhost:30000/h2-console](https://www.google.com/search?q=http://localhost:30000/h2-console)
2. **JDBC URL:** `jdbc:h2:mem:shopdb`
3. **User:** `sa`
4. **Password:** *(leave empty)*
5. **Connect** and run: `SELECT * FROM ORDER_ITEM`