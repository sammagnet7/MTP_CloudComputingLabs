# 🎨 MicroShop Frontend (SPA)

This is the client-facing **Single Page Application (SPA)** for the distributed eCommerce platform.

It is built with **Vue.js 3** (using the Composition API) and **Tailwind CSS**. It is designed to demonstrate the **Microservices Aggregation** pattern, where a single frontend fetches data from multiple distinct backend services seamlessly.

---

## 🏗️ Architecture

This frontend is a "No-Build" application. It runs directly in the browser using CDN imports, making it lightweight and easy to inspect.

It connects to the following backend services:

| Feature | Backend Service | Port | Tech Stack |
| --- | --- | --- | --- |
| **Product Catalog** | Product Service | `:30002` | Python (FastAPI) |
| **Live Stock** | Inventory Service | `:30001` | Java (Spring Boot) |
| **Cart & Checkout** | Order Service | `:30003` | Java (Spring Boot) |
| **Payment History** | Payment Service | `:30004` | Python (FastAPI) |
| **User Auth** | Monolith (Legacy) | `:30000` | Java (Spring Boot) |

---

## 🛠️ Tech Stack

* **Framework:** Vue.js 3 (Global Build via CDN)
* **Styling:** Tailwind CSS (via CDN)
* **Server:** Nginx (Alpine Docker Image)
* **Notifications:** Toastify.js

---

## 🚀 How to Run


1. Open your browser to: **[http://localhost:30005](http://localhost:30005)**

### Option A: Standalone Docker Run (Nginx)

If you want to run *only* the frontend container manually:

1. Navigate to the `eCommerce-Frontend` directory.
2. Run the following command:
```bash
docker run -d --name frontend-ui \
  -p 30005:80 \
  -v $(pwd):/usr/share/nginx/html \
  nginx:alpine

```



### Option B: Local Python Server

Since this is a static HTML file, you can also serve it using Python's built-in server:

```bash
# Run inside the eCommerce-Frontend folder
python3 -m http.server 30005

```

---

## 🧩 Key Features & Implementation

### 1. Product Details Aggregation

When you click "View Details", the frontend performs **Client-Side Aggregation**:

1. Fetches **Description & Price** from the **Product Service** (Python).
2. Fetches **Real-time Stock** from the **Inventory Service** (Java).
3. Merges the data to display the full modal.

### 2. Orchestrated Checkout

When you click **Checkout**:

1. The frontend sends a request to the **Order Service** (Aggregator).
2. The Order Service internally calls Inventory (to deduct stock) and Payment (to charge money).
3. The frontend receives a simple "Success" or "Fail" response.

### 3. Distributed Dashboard

The "My Dashboard" section demonstrates the **Distributed Data** pattern:

* **Order Tab:** Fetches history from the **Order Service DB**.
* **Payments Tab:** Fetches transaction logs from the **Payment Service DB**.

---

## ⚙️ Configuration

The API endpoints are hardcoded in the `index.html` file (inside the `<script>` tag) for demonstration purposes:

```javascript
const API = {
    MONOLITH:  'http://localhost:30000/api',
    INVENTORY: 'http://localhost:30001/api/v2/inventory',
    PRODUCT:   'http://localhost:30002/api/v2/products',
    ORDER:     'http://localhost:30003/api/v2/orders',
    PAYMENT:   'http://localhost:30004/api/v2/payments'
};

```

If you change the ports of your backend services, ensure you update these constants in `index.html`.
