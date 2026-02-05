
# 🛍️ E-Commerce Monolith API Service

This service provides a centralized API for User Management, Product Catalog, Shopping Cart, and Order Processing.

**Base URL:** `http://localhost:8080/api`

## 📋 API Endpoints

| Method | Endpoint | Description | Request Body / Notes |
| :--- | :--- | :--- | :--- |
| **GET** | `/products` | Retrieve all available products. | None |
| **GET** | `/users` | Retrieve all registered users. | None |
| **POST** | `/cart/{userId}/add` | Add an item to a user's shopping cart. | JSON: `{"productId": 1, "quantity": 1}` |
| **POST** | `/checkout/{userId}` | Checkout, process payment, and create order. | None (Uses current cart state) |

---

## 🧪 Test Data (Pre-loaded)

The system automatically loads the following data on startup (via `data.sql`), so you can test immediately without creating users.

### Users
| ID | Name | Role |
| :--- | :--- | :--- |
| `1` | Alice Dev | Standard User |
| `2` | Bob Ops | Standard User |
| `3` | Charlie Tester | Standard User |

### Products
| ID | Name | Price | Stock |
| :--- | :--- | :--- | :--- |
| `1` | Smartphone | $699.00 | 50 |
| `2` | Laptop | $1200.00 | 20 |
| `3` | Wireless Mouse | $25.00 | 100 |
| `4` | Microservices Book | $45.00 | 30 |

---

## 🚀 Quick Start (cURL Commands)

Use these commands to simulate a full user flow.

### 1. View Catalog
```bash
curl http://localhost:8080/api/products

```

### 2. Add "Smartphone" to Alice's Cart (User ID 1)

```bash
curl -X POST http://localhost:8080/api/cart/1/add \
  -H "Content-Type: application/json" \
  -d '{"productId": 1, "quantity": 1}'

```

### 3. Add "Wireless Mouse" to Alice's Cart

```bash
curl -X POST http://localhost:8080/api/cart/1/add \
  -H "Content-Type: application/json" \
  -d '{"productId": 3, "quantity": 2}'

```

### 4. Checkout (Place Order)

Triggers Payment, Inventory Check, and Email Notification.

```bash
curl -X POST http://localhost:8080/api/checkout/1

```

---