# 🛍️ eCommerce Order Service (The Aggregator)

This microservice acts as the **Central Orchestrator** for the e-commerce platform. It replaces the monolithic checkout logic by coordinating distributed transactions across the **Inventory**, **Product**, and **Payment** microservices.

It handles **Cart Management** locally (using an embedded H2 database) but delegates critical business logic to external services via REST APIs.

---

## 🏗️ Architecture

This service sits in the center of the architecture, acting as an API Gateway/Aggregator for the checkout process.

| Service | Port | Role | Tech Stack |
| --- | --- | --- | --- |
| **Order Service** | `30003` | **Aggregator (Self)** | Java / Spring Boot |
| **Inventory Service** | `30001` | Stock Management | Java / PostgreSQL |
| **Product Service** | `30002` | Catalog & Pricing | Python / MySQL |
| **Payment Service** | `30004` | Transaction Processing | **Python** / Mock |

---

## 🛠️ Tech Stack

* **Language:** Java 17
* **Framework:** Spring Boot 3.x
* **Database:** H2 (In-Memory for Cart & Order History)
* **Containerization:** Docker (Multi-Stage Build)
* **Communication:** Synchronous REST (RestTemplate)

---

## 🚀 How to Run

### ✅ Prerequisites

Ensure the dependent microservices are running on their respective ports (`30001`, `30002`, `30004`).

### Option A: Run via Docker (Recommended)

This service uses a **Multi-Stage Dockerfile** to build a lightweight image.

**1. Build the Image:**

```bash
docker build -t order-service:v1 .

```

**2. Run the Container:**
*Note: We use `--network host` to easily allow the container to talk to other services running on `localhost`.*

```bash
docker run -d --name order-app \
  --network host \
  order-service:v1

```

### Option B: Run via Maven (Local)

```bash
./mvnw clean spring-boot:run

```

The application will start on **http://localhost:30003**.

---

## 🔌 API Documentation

**Base URL:** `http://localhost:30003/api/v2/orders`

### 1. 🛒 Cart Operations

| Method | Endpoint | Description | Payload Example |
| --- | --- | --- | --- |
| **POST** | `/cart/{userId}/add` | Add item to local cart. | `{"productId": 1, "quantity": 1}` |

### 2. 💳 Checkout (The Orchestrator)

| Method | Endpoint | Description |
| --- | --- | --- |
| **POST** | `/checkout/{userId}` | Triggers the distributed transaction. |

**Process Flow:**

1. **Fetch Cart:** Retrieves items from local H2 DB.
2. **Get Price:** Calls **Product Service** (Python `:30002`) for authoritative price.
3. **Deduct Stock:** Calls **Inventory Service** (Java `:30001`) to reduce quantity.
4. **Calculate Total:** Computes sum based on fetched price.
5. **Process Payment:** Calls **Payment Service** (Python `:30004`) to charge the user.
6. **Save Order:** Persists the final receipt in local H2 DB.

### 3. 📜 Order History

| Method | Endpoint | Description |
| --- | --- | --- |
| **GET** | `/users/{userId}` | Get all past orders for a user. |
| **GET** | `/{orderId}` | Get details of a specific order. |

---

## 🧪 Testing (cURL Commands)

### 1. Add Item to Cart

*User 1 adds Product 1 (Smartphone).*

```bash
curl -X POST http://localhost:30003/api/v2/orders/cart/1/add \
  -H "Content-Type: application/json" \
  -d '{"productId": 1, "quantity": 1}'

```

### 2. Perform Checkout

*Triggers the full orchestration flow.*

```bash
curl -X POST http://localhost:30003/api/v2/orders/checkout/1

```

**Success Response:**

```json
{
    "id": 1,
    "status": "PAID",
    "totalAmount": 699.0,
    "createdAt": "2023-10-25T10:00:00",
    "items": [...]
}

```

### 3. View Order History

```bash
curl -X GET http://localhost:30003/api/v2/orders/users/1

```

---

## ⚙️ Configuration

**`src/main/resources/application.properties`**

If your microservices are running on different hosts (not localhost), update these variables or pass them as Environment Variables to Docker:

```properties
server.port=30003
spring.application.name=order-service

# Dependencies
microservice.inventory.url=http://localhost:30001/api/v2/inventory
microservice.product.url=http://localhost:30002/api/v2/products
microservice.payment.url=http://localhost:30004/api/v2/payments

```
---
## 🛠️ Database Console

Inspect the raw tables and relationships.

1. **URL:** [http://localhost:30003/h2-console](http://localhost:30003/h2-console)
2. **JDBC URL:** `jdbc:h2:mem:orderdb`
3. **User:** `sa`
4. **Password:** *(leave empty)*
5. **Connect** and run: `SELECT * FROM ORDERS`