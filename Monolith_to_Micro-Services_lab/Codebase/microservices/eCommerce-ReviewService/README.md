# 🌟 Review Service (Microservice)

Part of the **Strangler Fig Migration** pattern.

This service manages user-generated content (reviews and ratings). It is decoupled from the Monolith but maintains data integrity by communicating with the **Product Service** to validate items before allowing reviews. It is built with **Python (FastAPI)**.

---

## 📋 Prerequisites

* **Docker** installed on your machine.
* **Python 3.9+** (only if running without Docker).

---

## ⚙️ Environment Variables

The application is configured via environment variables.

| Variable | Description | Default Value |
| --- | --- | --- |
| `DATABASE_URL` | Connection string for the database. | `sqlite:///./reviews.db` |
| `PORT` | Port the app runs on (internal to container). | `30006` |
| `PRODUCT_SERVICE_URL` | URL to reach the Product Service API. | `http://product-service:30002/api/v2/products` |

---

## 🐳 Docker Instructions

### 1. Build the Image

Build a lightweight image using the provided `Dockerfile`.

```bash
docker build -t review-service:v1 .

```

### 2. Run the Container

Run the service on host port **30006**. Note that we link it to the network so it can reach the Product Service.

```bash
docker run --rm \
  -p 30006:30006 \
  --name review-service \
  --network ecommerce-network \
  -e PRODUCT_SERVICE_URL="http://product-service:30002/api/v2/products" \
  review-service:v1

```

### 3. Verify Running

Check if the container is up:

```bash
docker ps

```

### 4. Stop & Remove

```bash
docker stop review-service && docker rm review-service

```

---

## 🔌 API Endpoints & Schemas

**Base URL:** `http://localhost:30006/api/v2`

### 1. List Product Reviews

Fetches all reviews for a specific product ID.

* **Endpoint:** `GET /reviews/products/{id}`
* **Full URL:** `http://localhost:30006/api/v2/reviews/products/{id}`
* **Curl Example:**

```bash
curl -s http://localhost:30006/api/v2/reviews/products/1 | json_pp

```

#### **Response Schema (JSON Array)**

```json
[
  {
    "id": 1,
    "productId": 1,
    "userName": "Alice",
    "rating": 5,
    "comment": "Great phone!"
  },
  {
    "id": 2,
    "productId": 1,
    "userName": "Bob",
    "rating": 4,
    "comment": "Battery life could be better."
  }
]

```

---

### 2. Add a Review

Adds a new review. **Note:** This endpoint calls the Product Service to verify the `id` exists before saving.

* **Endpoint:** `POST /reviews/products/{id}`
* **Full URL:** `http://localhost:30006/api/v2/reviews/products/{id}`
* **Curl Example:**

```bash
curl -X POST http://localhost:30006/api/v2/reviews/products/1 \
  -H "Content-Type: application/json" \
  -d '{"userName": "Charlie", "rating": 5, "comment": "Fast delivery!"}' | json_pp

```

#### **Request Schema (JSON Object)**

```json
{
  "userName": "Charlie",
  "rating": 5,
  "comment": "Fast delivery!"
}

```

#### **Response Schema (JSON Object)**

```json
{
  "id": 3,
  "productId": 1,
  "userName": "Charlie",
  "rating": 5,
  "comment": "Fast delivery!"
}

```

#### **Error Schema (404 Not Found)**

Occurs if the product ID does not exist in the Product Service.

```json
{
  "detail": "Product not found or Product Service unavailable"
}

```

---

## 📚 Automatic Documentation

Swagger UI docs are automatically generated and available for testing.

* **Swagger UI:** [http://localhost:30006/docs](https://www.google.com/search?q=http://localhost:30006/docs)
* **ReDoc:** [http://localhost:30006/redoc](https://www.google.com/search?q=http://localhost:30006/redoc)
