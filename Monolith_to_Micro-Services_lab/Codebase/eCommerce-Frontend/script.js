const { createApp, ref, computed, onMounted } = Vue;

// 🏗️ MICROSERVICES GATEWAY CONFIG
const API = {
	MONOLITH: 'http://localhost:30000/api',               // Legacy Auth
	INVENTORY: 'http://localhost:30001/api/v2/inventory',  // Stock
	PRODUCT: 'http://localhost:30002/api/v2/products',   // Catalog
	ORDER: 'http://localhost:30003/api/v2/orders',     // Aggregator
	PAYMENT: 'http://localhost:30004/api/v2/payments',   // Transactions
	REVIEWS: 'http://localhost:30006/api/v2/reviews'     // Reviews (New)
};

const USER_ID = 1;

createApp({
	setup() {
		// View State
		const currentView = ref('home');
		const dashboardTab = ref('orders');
		const showCart = ref(false);

		// Data State
		const products = ref([]);
		const orders = ref([]);
		const payments = ref([]);
		const cart = ref([]);
		const reviews = ref([]);

		// UI State
		const loading = ref(true);
		const processing = ref(false);
		const detailLoading = ref(false);
		const currentStock = ref(0);
		const selectedProduct = ref(null);

		// Form State
		const newReview = ref({ rating: 5, comment: '' });

		// 1. FETCH CATALOG (Python Service)
		const fetchProducts = async () => {
			try {
				const res = await fetch(API.PRODUCT);
				if (res.ok) products.value = await res.json();
			} catch (e) { showToast("Catalog Service Unavailable", "error"); }
			finally { loading.value = false; }
		};

		// 2. FETCH DASHBOARD DATA (Distributed)
		const openDashboard = async () => {
			currentView.value = 'dashboard';
			orders.value = [];
			payments.value = [];

			try {
				const oRes = await fetch(`${API.ORDER}/users/${USER_ID}`);
				if (oRes.ok) orders.value = await oRes.json();
			} catch (e) { console.error("Order Service failed"); }

			try {
				const pRes = await fetch(`${API.PAYMENT}/users/${USER_ID}`);
				if (pRes.ok) payments.value = await pRes.json();
			} catch (e) { console.error("Payment Service failed"); }
		};

		// 3. PRODUCT DETAILS AGGREGATOR (3-Way Parallel Fetch)
		const openProductDetails = async (product) => {
			selectedProduct.value = product;
			detailLoading.value = true;
			currentStock.value = 0;
			reviews.value = []; // Clear old reviews

			try {
				// Fetch Price (Py), Stock (Java), Reviews (New Svc) simultaneously
				const [stockRes, revRes] = await Promise.all([
					fetch(`${API.INVENTORY}/${product.id}`),
					fetch(`${API.REVIEWS}/products/${product.id}`)
				]);

				if (stockRes.ok) currentStock.value = await stockRes.json();
				if (revRes.ok) reviews.value = await revRes.json();

			} catch (e) { showToast("Failed to aggregate details", "error"); }
			finally { detailLoading.value = false; }
		};

		// 4. SUBMIT REVIEW (Reviews Service)
		const submitReview = async () => {
			if (!selectedProduct.value || !newReview.value.comment) return;

			try {
				const res = await fetch(`${API.REVIEWS}/products/${selectedProduct.value.id}`, {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({
						userName: 'Little Buddha', // Hardcoded for demo
						rating: parseInt(newReview.value.rating),
						comment: newReview.value.comment
					})
				});

				if (res.ok) {
					showToast("Review Added via Service :30006! 🎉", "success");
					// Optimistically update UI
					reviews.value.unshift({
						id: Date.now(),
						userName: 'Little Buddha',
						rating: parseInt(newReview.value.rating),
						comment: newReview.value.comment
					});
					newReview.value.comment = ''; // Reset form
				} else {
					throw new Error("Review service failed");
				}
			} catch (e) { showToast("Failed to post review", "error"); }
		};

		// 5. CART & CHECKOUT (Order Service)
		const addToCart = async (product) => {
			try {
				await fetch(`${API.ORDER}/cart/${USER_ID}/add`, {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({ productId: product.id, quantity: 1 })
				});
				showToast("Added to Cart (Order Svc)");
				selectedProduct.value = null;
			} catch (e) { showToast("Failed to add to cart", "error"); }
		};

		const checkout = async () => {
			processing.value = true;
			try {
				const res = await fetch(`${API.ORDER}/checkout/${USER_ID}`, { method: 'POST' });
				if (res.ok) {
					const receipt = await res.json();
					showToast(`Order #${receipt.id} Confirmed! 🎉`, "success");
					cart.value = [];
					showCart.value = false;
					openDashboard();
				} else { throw new Error("Checkout failed"); }
			} catch (e) { showToast("Transaction Failed", "error"); }
			finally { processing.value = false; }
		};

		// Helpers
		const getIcon = (name) => {
			if (!name) return '📦';
			if (name.includes('Laptop')) return '💻';
			if (name.includes('Phone')) return '📱';
			if (name.includes('Mouse')) return '🖱️';
			return '📦';
		};
		const formatDate = (d) => new Date(d).toLocaleDateString('en-IN');
		const openCart = () => showCart.value = true;

		// Optimistic Cart Add (Visual Only)
		const originalAddToCart = addToCart;
		const enhancedAddToCart = async (p) => {
			await originalAddToCart(p);
			cart.value.push({ productId: p.id, productName: p.name, quantity: 1 });
		};

		const showToast = (msg, type) => Toastify({
			text: msg, duration: 4000,
			style: { background: type === 'error' ? "#ef4444" : "#10b981", borderRadius: "8px" },
			gravity: "bottom"
		}).showToast();

		onMounted(fetchProducts);

		return {
			currentView, dashboardTab, openDashboard,
			products, orders, payments, cart, reviews,
			showCart, loading, processing, detailLoading,
			selectedProduct, currentStock, newReview,
			openProductDetails, submitReview, addToCart: enhancedAddToCart, checkout, openCart,
			getIcon, formatDate, cartCount: computed(() => cart.value.length)
		};
	}
}).mount('#app');
