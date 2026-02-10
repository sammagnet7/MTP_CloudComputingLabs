# 🐍 Product Catalog Service (Microservice)

Part of the **Strangler Fig Migration** pattern.

This service is the first step in migrating functionality away from the Java Monolith. It serves as the **Single Source of Truth** for product details and pricing. It is built with **Python (FastAPI)** and is designed to be lightweight, fast, and containerized.

---

## 📋 Prerequisites

* **Docker** installed on your machine.
* **Python 3.9+** (only if running without Docker).

---

## ⚙️ Environment Variables

The application is configured via environment variables. You can pass these to the Docker container or set them in a `.env` file.

| Variable | Description | Default Value |
| --- | --- | --- |
| `DATABASE_URL` | Connection string for the database. | `sqlite:///./test.db` |
| `PORT` | Port the app runs on (internal to container). | `30002` |

---

## 🐳 Docker Instructions

### 1. Build the Image

Build a lightweight, optimized image using the provided `Dockerfile`.

```bash
docker build -t product-service:v1 .

```

### 2. Run the Container

Run the service on host port **30002**.

```bash
docker run --rm \
  -p 30002:30002 \
  --name product-catalog \
  -e DATABASE_URL="sqlite:///./products.db" \
  product-service:v1

```

### 3. Verify Running

Check if the container is up:

```bash
docker ps

```

### 4. Stop & Remove

```bash
docker stop product-catalog && docker rm product-catalog

```

---

## 🔌 API Endpoints & Schemas

**Base URL:** `http://localhost:30002`

### 1. List All Products

Fetches the full catalog list. Replaces the monolith's `/api/products` endpoint.

* **Endpoint:** `GET /products`
* **Curl Example:**
```bash
curl -s http://localhost:30002/products | json_pp

```



#### **Response Schema (JSON Array)**

```json
[
  {
    "id": 1,
    "name": "Smartphone",
    "price": 699.0,
    "description": "Flagship phone",
    "category_id": 101
  },
  {
    "id": 2,
    "name": "Laptop",
    "price": 1200.0,
    "description": "Gaming Laptop",
    "category_id": 102
  }
]

```

---

### 2. Get Product Details

Fetches details for a single product. Used by the Checkout service to validate prices.

* **Endpoint:** `GET /products/{id}`
* **Curl Example:**
```bash
curl -s http://localhost:30002/products/1 | json_pp

```



#### **Response Schema (JSON Object)**

```json
{
  "id": 1,
  "name": "Smartphone",
  "price": 699.0,
  "description": "Flagship phone",
  "category_id": 101
}

```

#### **Error Schema (404 Not Found)**

```json
{
  "detail": "Product not found"
}

```

---

## 📚 Automatic Documentation

Since this service uses FastAPI, interactive documentation is available out-of-the-box when the container is running.

* **Swagger UI:** [http://localhost:30002/docs](https://www.google.com/search?q=http://localhost:30002/docs)
* **ReDoc:** [http://localhost:30002/redoc](https://www.google.com/search?q=http://localhost:30002/redoc)
