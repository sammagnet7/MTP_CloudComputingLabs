# 📦 eCommerce Inventory Microservice

This is a standalone **Microservice** responsible for managing product stock levels. It is the first service extracted from the Monolith as part of the "Monolith to Microservices" migration lab.

It demonstrates the **Database-per-Service** pattern by using its own dedicated PostgreSQL database, ensuring loose coupling from the legacy system.

---

## 🛠️ Tech Stack

* **Language:** Java 17
* **Framework:** Spring Boot 3.x
* **Database:** PostgreSQL (Containerized)
* **Build Tool:** Maven
* **Port:** `30001` (to avoid conflict with Monolith on 30000)

---

## 🚀 How to Run

Since this service requires a PostgreSQL database, you must start the database container **before** starting the application.

### 1️⃣ Step 1: Start the Database

Run the following Docker command to spin up the dedicated `inventorydb`.

```bash
docker run --name inventory-db \
  -e POSTGRES_DB=inventorydb \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:15

```

### 2️⃣ Step 2: Start the Application

**Option A: Run via Maven (Local)**

```bash
./mvnw clean spring-boot:run

```

**Option B: Run via Docker (Containerized)**

```bash
# 1. Build the image
docker build -t inventory-service .

# 2. Run container (Link to DB)
docker run -d --name inventory-app \
  --network host \
  -e SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/inventorydb \
  inventory-service

```

*(Note: If using Docker Desktop on Mac/Windows, replace `localhost` with `host.docker.internal` inside the container).*

---

## 🔌 API Documentation

**Base URL:** `http://localhost:30001/api/v2/inventory`

| Method | Endpoint | Description |
| --- | --- | --- |
| **GET** | `/{productId}` | Get current stock level for a product. |
| **POST** | `/reduce` | Deduct stock (Atomic transaction). |

### 🧪 Test with cURL

#### 1. Check Stock

Get the quantity for Product ID `1` (Smartphone).

```bash
curl -X GET http://localhost:30001/api/v2/inventory/1

```

**Response:** `50`

#### 2. Deduct Stock (Success)

Simulate a user buying 1 item.

```bash
curl -X POST http://localhost:30001/api/v2/inventory/reduce \
  -H "Content-Type: application/json" \
  -d '{"productId": 1, "quantity": 1}'

```

**Response:** `Stock deducted successfully`

#### 3. Deduct Stock (Failure)

Try to buy more than available.

```bash
curl -X POST http://localhost:30001/api/v2/inventory/reduce \
  -H "Content-Type: application/json" \
  -d '{"productId": 1, "quantity": 100000}'

```

**Response:** `Insufficient Stock` (Status: 409 Conflict)

---

## 💾 Database Schema

The service initializes a table named `inventory` automatically on startup.

| Column | Type | Description |
| --- | --- | --- |
| `id` | SERIAL (PK) | Unique Record ID |
| `product_id` | BIGINT | ID reference to the external Product Catalog |
| `quantity` | INTEGER | Available stock count |

**Seed Data:**
The application pre-loads data via `src/main/resources/data.sql`:

* Product 1: 50
* Product 2: 20
* Product 3: 100

---

## 🐞 Troubleshooting

**Error: `Connection refused` to Database**

* Ensure the Docker container `inventory-db` is running (`docker ps`).
* Ensure port `5432` is not occupied by a local Postgres installation.

**Error: `relation "inventory" does not exist**`

* This happens if `data.sql` runs before Hibernate creates the table.
* **Fix:** Ensure `spring.jpa.defer-datasource-initialization=true` is in `application.properties`.