# 🛍️ E-Commerce Monolith API Service

This repository contains a sample E-commerce Monolithic application designed for "Monolith to Microservices" migration demos. It handles User Management, Products, Cart, Orders, and Mock Payments in a single Spring Boot application.

---

## 📋 Prerequisites & Requirements

Before running the application, ensure you have the following installed:

### 1. Java (Required for Local Run)
* **Version:** Java 17 or higher (JDK 17+)
* **Check version:** `java -version`

### 2. Docker (Optional - for Containerization Demo)
* **Requirement:** Docker Desktop or Docker Engine
* **Version:** 20.10+ recommended
* **Why?** Used if you want to demonstrate containerizing the monolith before splitting it, or if you want to deploy it to Kubernetes later.

### 3. Maven (Optional)
* The project includes a Maven Wrapper (`mvnw`), so a local Maven installation is not strictly required.

---

## 🏃‍♂️ How to Run

### Option A: Local Run (Java)
This is the fastest way to start the demo if you have Java installed.

1.  Open your terminal in the project root.
2.  Run the application using the wrapper:
    * **Mac/Linux:** `./mvnw spring-boot:run`
    * **Windows:** `mvnw spring-boot:run`
3.  The app will start on `http://localhost:30000`.

### Option B: Run with Docker
The repository already includes a **Multi-Stage `Dockerfile`**. This allows you to build and run the application without installing Java or Maven on your host machine.

1.  **Build the Image:**
    Run this command in the project root:
    ```bash
    docker build --no-cache -t monolith-shop .
    ```

2.  **Run the Container:**
    ```bash
    docker run -p 30000:30000 monolith-shop
    ```

---
## 💻 Web UI (Frontend)

The application includes a built-in **Vue.js + Tailwind** storefront served directly by the backend (typical monolithic pattern).

1.  Start the application (via Java or Docker).
2.  Open your browser to: [http://localhost:8080](http://localhost:30000)
3.  You can browse products, add them to the cart, and perform the "Checkout" operation visually without using cURL.

---
## 🔌 API Endpoints

**Base URL:** `http://localhost:30000/api`

| Method | Endpoint | Description | Request Body Example |
| --- | --- | --- | --- |
| **GET** | `/products` | List all products (summary). | N/A |
| **GET** | `/products/{id}` | **(New)** Get details + Stock + Reviews. | N/A |
| **POST** | `/products/{id}/reviews` | **(New)** Add a review for a product. | `{"userName": "Dave", "rating": 5, "comment": "Great!"}` |
| **POST** | `/cart/{userId}/add` | Add item to cart. | `{"productId": 1, "quantity": 1}` |
| **POST** | `/checkout/{userId}` | Place order (Inventory/Payment/Email). | N/A |

---

## 💾 Pre-Loaded Data (H2 Database)

The application uses an **In-Memory H2 Database**. Data is reset on restart.

### 📦 Products & Stock

| ID | Name | Price | Initial Stock |
| --- | --- | --- | --- |
| `1` | Smartphone | $699.00 | 50 |
| `2` | Laptop | $1200.00 | 20 |
| `3` | Microservices Book | $45.00 | 100 |

### ⭐ Pre-Loaded Reviews

* **Smartphone:** 5 Stars ("Great battery life!")
* **Smartphone:** 4 Stars ("Good, but expensive.")
* **Book:** 5 Stars ("Changed my career.")

---

## 🧪 Quick Test (cURL Commands)

Copy and paste these commands into your terminal to test the specific domains.

### 1. View Product Details (Aggregated Data)

This fetches data from Product, Inventory, and Review services in one call.

```bash
curl -s http://localhost:30000/api/products/1

```

### 2. Post a Review

Add a new review for the Smartphone.

```bash
curl -X POST http://localhost:30000/api/products/1/reviews \
  -H "Content-Type: application/json" \
  -d '{"userName": "Charlie", "rating": 5, "comment": "Amazing phone, fast delivery!"}'

```

### 3. Add to Cart & Checkout

This flow tests the **Transactional boundary** across Inventory and Payment.

```bash
# Add to Cart
curl -X POST http://localhost:30000/api/cart/1/add \
  -H "Content-Type: application/json" \
  -d '{"productId": 1, "quantity": 1}'

# Checkout (Triggers Payment & Stock Reduction)
curl -X POST http://localhost:30000/api/checkout/1

```

---

## 🛠️ Database Console

You can view the raw database tables using the H2 Web Console.

1. Go to: [http://localhost:30000/h2-console](https://www.google.com/search?q=http://localhost:30000/h2-console)
2. **Driver Class:** `org.h2.Driver`
3. **JDBC URL:** `jdbc:h2:mem:shopdb`
4. **Username:** `sa`
5. **Password:** *(leave empty)*
6. Click **Connect**.

---