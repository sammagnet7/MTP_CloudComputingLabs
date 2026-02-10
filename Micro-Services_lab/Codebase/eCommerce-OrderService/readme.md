# 🛒 eCommerce Order Service (The Aggregator)

This microservice acts as the **Central Orchestrator** for the checkout process. It replaces the Monolithic `CheckoutService` by coordinating distributed transactions across the **Inventory**, **Product**, and **Payment** microservices.

It handles **Cart Management** locally (using an embedded H2 database) but delegates critical business logic to external services via REST APIs.

---

## 🛠️ Tech Stack

* **Language:** Java 17
* **Framework:** Spring Boot 3.x
* **Database:** H2 (In-Memory for Cart/Orders)
* **Communication:** `RestTemplate` (Synchronous HTTP)
* **Port:** `30003`

---

## 🔗 Architecture & Dependencies

This service sits in the middle of the architecture, acting as the client to three other services:

| Service | Port | Role | Integration Point |
| --- | --- | --- | --- |
| **Inventory Service** | `30001` | Deducts Stock. | `POST /api/v2/inventory/reduce` |
| **Product Service** | `30002` | Fetches Live Price. | `GET /api/v2/products/{id}` |
| **Payment Service** | `30004` | Charges Credit Card. | `POST /api/v2/payments` |

---

## 🚀 How to Run

### 1️⃣ Prerequisites

Ensure the dependent microservices are running:

* **Inventory Service:** [Codebase](https://www.google.com/search?q=../eCommerce-InventoryService)
* **Product Service:** [Codebase](https://www.google.com/search?q=../eCommerce-ProductService)
* **Payment Service:** [Codebase](https://www.google.com/search?q=../eCommerce-PaymentService)

### 2️⃣ Start the Application

```bash
# Option A: Maven
./mvnw clean spring-boot:run

# Option B: Java JAR
java -jar target/eCommerce-OrderService-0.0.1-SNAPSHOT.jar

```

The application will start on **http://localhost:30003**.

---

## 🔌 API Documentation

**Base URL:** `http://localhost:30003/api/v2/orders`

### 1. 🛒 Cart Management

| Method | Endpoint | Description | Payload Example |
| --- | --- | --- | --- |
| **POST** | `/cart/{userId}/add` | Add item to user's local cart. | `{"productId": 1, "quantity": 1}` |

### 2. 💳 Checkout (The Orchestrator)

| Method | Endpoint | Description |
| --- | --- | --- |
| **POST** | `/checkout/{userId}` | Triggers the distributed transaction. |

**Process Flow:**

1. **Fetch Cart:** Retrieves items from local H2 DB.
2. **Get Price:** Calls **Product Service** (`:30002`) for each item.
3. **Deduct Stock:** Calls **Inventory Service** (`:30001`) to reduce quantity.
4. **Calculate Total:** Computes sum based on *external* price.
5. **Process Payment:** Calls **Payment Service** (`:30004`).
6. **Save Order:** Persists the final receipt in local H2 DB.

### 3. 📜 Order History

| Method | Endpoint | Description |
| --- | --- | --- |
| **GET** | `/users/{userId}` | Get all past orders for a user. |
| **GET** | `/{orderId}` | Get details of a specific order. |

---

## 🧪 Test Scenarios (cURL)

### Scenario A: Successful Purchase

**1. Add Smartphone to Cart:**

```bash
curl -X POST http://localhost:30003/api/v2/orders/cart/1/add \
  -H "Content-Type: application/json" \
  -d '{"productId": 1, "quantity": 1}'

```

**2. Checkout:**

```bash
curl -X POST http://localhost:30003/api/v2/orders/checkout/1

```

**Response:** `{"status": "PAID", "totalAmount": 699.0, ...}`

---

### Scenario B: Out of Stock Failure

If you try to buy 10,000 units, the **Inventory Service** will return `409 Conflict`, and this service will propagate the error.

```bash
curl -X POST http://localhost:30003/api/v2/orders/cart/1/add \
  -H "Content-Type: application/json" \
  -d '{"productId": 1, "quantity": 10000}'

curl -X POST http://localhost:30003/api/v2/orders/checkout/1

```

**Response:** `{"error": "Out of Stock for: Smartphone"}`

---

## ⚙️ Configuration (`application.properties`)

If you are running dependent services on different hosts (e.g., Docker Bridge network), update these lines:

```properties
microservice.inventory.url=http://localhost:30001/api/v2/inventory
microservice.product.url=http://localhost:30002/api/v2/products
microservice.payment.url=http://localhost:30004/api/v2/payments

```