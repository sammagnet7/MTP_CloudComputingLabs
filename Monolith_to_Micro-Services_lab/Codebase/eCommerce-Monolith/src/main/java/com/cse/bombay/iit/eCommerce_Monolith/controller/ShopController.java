package com.cse.bombay.iit.eCommerce_Monolith.controller;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.cse.bombay.iit.eCommerce_Monolith.model.Cart;
import com.cse.bombay.iit.eCommerce_Monolith.model.CartItem;
import com.cse.bombay.iit.eCommerce_Monolith.model.Order;
import com.cse.bombay.iit.eCommerce_Monolith.model.Payment;
import com.cse.bombay.iit.eCommerce_Monolith.model.Product;
import com.cse.bombay.iit.eCommerce_Monolith.model.Review;
import com.cse.bombay.iit.eCommerce_Monolith.model.User;
import com.cse.bombay.iit.eCommerce_Monolith.service.CartService;
import com.cse.bombay.iit.eCommerce_Monolith.service.CheckoutService;
import com.cse.bombay.iit.eCommerce_Monolith.service.InventoryService;
import com.cse.bombay.iit.eCommerce_Monolith.service.OrderService;
import com.cse.bombay.iit.eCommerce_Monolith.service.PaymentService;
import com.cse.bombay.iit.eCommerce_Monolith.service.ProductService;
import com.cse.bombay.iit.eCommerce_Monolith.service.ReviewService;
import com.cse.bombay.iit.eCommerce_Monolith.service.UserService;

@RestController
@RequestMapping("/api")
public class ShopController {

    @Autowired
    private ProductService productService;
    @Autowired
    private UserService userService;
    @Autowired
    private CartService cartService;
    @Autowired
    private CheckoutService checkoutService;
    @Autowired
    private ReviewService reviewService;
    @Autowired
    private InventoryService inventoryService;
    @Autowired
    private OrderService orderService;
    @Autowired
    private PaymentService paymentService;

    // --- Product endpoints---
    @GetMapping("/products")
    public List<Product> getAllProducts() {
        return productService.getAllProducts();
    }

    @GetMapping("/products/{id}")
    public Map<String, Object> getProductDetails(@PathVariable Long id) {
        Product product = productService.getProductById(id); // You need to add this method to ProductService
        Integer stock = inventoryService.getStock(id);

        Map<String, Object> response = new HashMap<>();
        response.put("product", product);
        response.put("stock", stock);
        // response.put("reviews", product.getCategory());
        response.put("reviews", product.getReviews());

        return response;
    }

    // --- User endpoints---

    @GetMapping("/users")
    public List<User> getAllUsers() {
        return userService.getAllUsers();
    }

    // --- Order endpoints---

    @PostMapping("/cart/{userId}/add")
    public Cart addToCart(@PathVariable Long userId, @RequestBody CartItem item) {
        // Delegate complex logic to Service
        return cartService.addToCart(userId, item);
    }

    @PostMapping("/checkout/{userId}")
    public Order checkout(@PathVariable Long userId) {
        // Delegate complex transaction to Service
        return checkoutService.placeOrder(userId);
    }

    // GET User's Order History
    @GetMapping("/users/{userId}/orders")
    public List<Order> getUserOrders(@PathVariable Long userId) {
        return orderService.getUserOrders(userId);
    }

    // GET Specific Order Details
    @GetMapping("/orders/{orderId}")
    public Order getOrderDetails(@PathVariable Long orderId) {
        return orderService.getOrderById(orderId);
    }

    // --- Review endpoints---

    @GetMapping("/products/{productId}/reviews")
    public List<Review> getProductReviews(@PathVariable Long productId) {
        return reviewService.getReviewsByProductId(productId);
    }

    @PostMapping("/products/{id}/reviews")
    public Review addReview(@PathVariable Long id, @RequestBody Map<String, Object> payload) {
        String user = (String) payload.get("userName");
        Integer rating = (Integer) payload.get("rating");
        String comment = (String) payload.get("comment");

        return reviewService.addReview(id, user, rating, comment);
    }

    // --- Payments endpoints---

    // GET Payment Status for an Order
    @GetMapping("/orders/{orderId}/payment")
    public Payment getOrderPaymentStatus(@PathVariable Long orderId) {
        return paymentService.getPaymentByOrderId(orderId);
    }

    // GET User's Payment History
    @GetMapping("/users/{userId}/payments")
    public List<Payment> getUserPayments(@PathVariable Long userId) {
        return paymentService.getUserPaymentHistory(userId);
    }
}
