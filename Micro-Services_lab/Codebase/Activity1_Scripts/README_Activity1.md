# 🛍️ eCommerce Strangler Fig Architecture

We are currently in the process of migrating from a **Monolith** to **Microservices** using the **Strangler Fig Pattern**.



## 🏗️ Architecture Overview

The system runs on a **Hybrid Architecture**:
1.  **Core Domain Services (v2)**: Extracted into standalone microservices (Inventory, Product, Order, Payment).
2.  **Legacy System (v1)**: The original Monolith handles remaining domains (Users, Reviews).
3.  **Frontend (Port 30005)**: Consumes both v1 and v2 endpoints transparently.

---

## 🔌 API Reference (For Frontend Developers)

**⚠️ Important:** Use **v2** endpoints for migrated services.
* Fallback to **v1** (Monolith) *only* for non-migrated features.

### 📦 1. Product Catalog (Migrated)
*Service: Product Service (Python)*

| Feature | Method | Endpoint | Port | Version |
| :--- | :--- | :--- | :--- | :--- |
| **List Products** | `GET` | `http://localhost:30002/api/v2/products` | `30002` | ✅ **v2** |
| **Product Details** | `GET` | `http://localhost:30002/api/v2/products/{id}` | `30002` | ✅ **v2** |

### 📦 2. Inventory (Migrated)
*Service: Inventory Service (Java)*

| Feature | Method | Endpoint | Port | Version |
| :--- | :--- | :--- | :--- | :--- |
| **Check Stock** | `GET` | `http://localhost:30001/api/v2/inventory/{id}` | `30001` | ✅ **v2** |
| **Deduct Stock** | `POST` | `http://localhost:30001/api/v2/inventory/reduce` | `30001` | ✅ **v2** |

### 🛒 3. Cart & Checkout (Migrated)
*Service: Order Service (Java Aggregator)*

| Feature | Method | Endpoint | Port | Version |
| :--- | :--- | :--- | :--- | :--- |
| **Add to Cart** | `POST` | `http://localhost:30003/api/v2/orders/cart/{uid}/add` | `30003` | ✅ **v2** |
| **Place Order** | `POST` | `http://localhost:30003/api/v2/orders/checkout/{uid}` | `30003` | ✅ **v2** |
| **Order History** | `GET` | `http://localhost:30003/api/v2/orders/users/{uid}` | `30003` | ✅ **v2** |

### 💳 4. Payments (Migrated)
*Service: Payment Service (Python)*

| Feature | Method | Endpoint | Port | Version |
| :--- | :--- | :--- | :--- | :--- |
| **Transaction History** | `GET` | `http://localhost:30004/api/v2/payments/users/{uid}` | `30004` | ✅ **v2** |

---

### 🏛️ 5. Legacy Domains (Not Migrated)
*Service: Monolith (Java)*

| Feature | Method | Endpoint | Port | Version |
| :--- | :--- | :--- | :--- | :--- |
| **Get User Profile** | `GET` | `http://localhost:30000/api/users/{id}` | `30000` | ⚠️ **v1** |
| **List Reviews** | `GET` | `http://localhost:30000/api/products/{id}/reviews` | `30000` | ⚠️ **v1** |
| **Post Review** | `POST` | `http://localhost:30000/api/products/{id}/reviews` | `30000` | ⚠️ **v1** |

---

## 🚀 How to Run (Automated)

We use **Docker Compose** to spin up the entire backend ecosystem (5 Apps + Databases) with one command.

### Prerequisites
* Docker Desktop installed and running.
* Ports `30000-30005` must be free.

### Start All Services
```bash
docker-compose up --build -d
```

### Stop All Services
```bash
docker-compose down
```

### verify Status
```bash
docker-compose ps
```