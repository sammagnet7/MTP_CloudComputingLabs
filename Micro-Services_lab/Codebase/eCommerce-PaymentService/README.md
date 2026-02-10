# 💳 Payment Service (Microservice)

Part of the **Strangler Fig Migration** pattern.

This service manages payment processing and transaction history. It replaces the Monolith's payment module and introduces the **Strangler Fig** pattern by communicating back to the Monolith to fetch legacy Order-to-User mappings while keeping Payment data separate.

Built with **Python (FastAPI)** and **SQLite**.

---

## 📋 Prerequisites

* **Docker** installed on your machine.
* **Python 3.9+** (only if running locally without Docker).
* **Monolith App** running on port `30000` (required for User History features).

---

## ⚙️ Environment Variables

The application is configured via environment variables.

| Variable | Description | Default Value |
| --- | --- | --- |
| `ORDER_SERVICE_URL` | URL to fetch User Orders from the legacy system. | `http://localhost:30003/api/v2/orders/users/{userId}` |
| `DATABASE_URL` | Connection string for the local database. | `sqlite:///./payments.db` |
| `PORT` | Internal container port. | `30004` |

---

## 🐳 Docker Instructions

### 1. Build the Image

```bash
docker build -t payment-service:v2 .

```

### 2. Run the Container

Run the service on host port **30004**.

> **Note:** If running the Monolith on your host machine, use `host.docker.internal` instead of `localhost` for the `ORDER_SERVICE_URL` so the container can reach your computer.

```bash
docker run --rm \
  -p 30004:30004 \
  --name payment-service \
  -e ORDER_SERVICE_URL="http://localhost:30003/api/v2/orders/users/{userId}" \
  payment-service:v2

```

### 3. Verify Running

Check if the container is up:

```bash
docker ps

```

### 4. Stop & Remove

```bash
docker stop payment-service && docker rm payment-service

```

---

## 🔌 API Endpoints & Schemas

**Base URL:** `http://localhost:30004/api/v2`

### 1. Process New Payment

Records a successful transaction locally.

* **Method:** `POST`
* **Endpoint:** `/payments/`
* **Curl Example:**

```bash
curl -X POST http://localhost:30004/api/v2/payments/ \
  -H "Content-Type: application/json" \
  -d '{"orderId": 105, "amount": 120.50}' | json_pp

```

#### **Response Schema**

```json
{
  "id": 3,
  "orderId": 105,
  "amount": 120.5,
  "status": "SUCCESS",
  "transactionId": "d9f8c7b6-...",
  "timestamp": "2023-10-27T10:00:00"
}

```

---

### 2. Get Payment by Order

Retrieves transaction details for a specific Order ID.

* **Method:** `GET`
* **Endpoint:** `/payments/order/{id}`
* **Curl Example:**

```bash
curl -s http://localhost:30004/api/v2/payments/order/105 | json_pp

```

---

### 3. Get User Payment History (Strangler Fig)

This endpoint demonstrates the migration pattern. It **calls the Monolith** to get the list of orders for a user, then queries the local database for matching payments.

* **Method:** `GET`
* **Endpoint:** `/payments/users/{id}`
* **Curl Example:** (For User 1 "Little Buddha")

```bash
curl -s http://localhost:30004/api/v2/payments/users/1 | json_pp

```

#### **Response Schema (JSON Array)**

```json
[
  {
    "id": 1,
    "orderId": 1,
    "amount": 1240.0,
    "status": "SUCCESS",
    "transactionId": "TXN_BUDDHA_001",
    "timestamp": "2023-10-26T09:30:00"
  },
  {
    "id": 2,
    "orderId": 2,
    "amount": 50.0,
    "status": "SUCCESS",
    "transactionId": "TXN_BUDDHA_002",
    "timestamp": "2023-10-26T14:15:00"
  }
]

```

---

## 📚 Automatic Documentation

Interactive API documentation provided by FastAPI.

* **Swagger UI:** [http://localhost:30004/docs](https://www.google.com/search?q=http://localhost:30004/docs)
* **ReDoc:** [http://localhost:30004/redoc](https://www.google.com/search?q=http://localhost:30004/redoc)
