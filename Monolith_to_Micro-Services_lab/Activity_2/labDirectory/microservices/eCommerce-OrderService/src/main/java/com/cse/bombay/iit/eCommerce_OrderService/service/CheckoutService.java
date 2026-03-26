package com.cse.bombay.iit.eCommerce_OrderService.service;

import java.time.LocalDateTime;
import java.util.ArrayList;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import com.cse.bombay.iit.eCommerce_OrderService.dto.InventoryRequest;
import com.cse.bombay.iit.eCommerce_OrderService.dto.PaymentRequest;
import com.cse.bombay.iit.eCommerce_OrderService.dto.ProductDTO;
import com.cse.bombay.iit.eCommerce_OrderService.model.Cart;
import com.cse.bombay.iit.eCommerce_OrderService.model.CartItem;
import com.cse.bombay.iit.eCommerce_OrderService.model.Order;
import com.cse.bombay.iit.eCommerce_OrderService.model.OrderItem;
import com.cse.bombay.iit.eCommerce_OrderService.repository.CartRepository;
import com.cse.bombay.iit.eCommerce_OrderService.repository.OrderRepository;

import jakarta.transaction.Transactional;

@Service
public class CheckoutService {

    @Autowired
    private CartRepository cartRepo;
    @Autowired
    private OrderRepository orderRepo;
    @Autowired
    private RestTemplate restTemplate;

    // Defined in application.properties
    @Value("${microservice.product.url}") // http://localhost:30002/api/v2/products
    private String productServiceUrl;

    @Value("${microservice.inventory.url}") // http://localhost:30001/api/v2/inventory
    private String inventoryServiceUrl;

    @Value("${microservice.payment.url}") // http://localhost:30004/api/v2/payments
    private String paymentServiceUrl;

    @Transactional
    public Order placeOrder(Long userId) {
        // 1. Get User's Cart (Local DB - Same as Monolith)
        Cart cart = cartRepo.findByUserId(userId)
                .orElseThrow(() -> new RuntimeException("Cart not found for user: " + userId));

        if (cart.getItems().isEmpty()) {
            throw new RuntimeException("Cart is empty! Add items before checkout.");
        }

        // 2. Prepare Order Object (Same DB Table Structure)
        Order order = new Order();
        order.setUserId(userId);
        order.setCreatedAt(LocalDateTime.now());
        order.setStatus("PROCESSING");
        order.setItems(new ArrayList<>());

        double calculatedTotal = 0.0;

        // 3. Process Each Cart Item
        for (CartItem cartItem : cart.getItems()) {
            Long productId = cartItem.getProductId();
            int quantity = cartItem.getQuantity();

            // ---------------------------------------------------------
            // A. Fetch Product (EXTERNAL CALL to Python Service)
            // ---------------------------------------------------------
            // Monolith: productService.getProductById(productId);
            ProductDTO product;
            try {
                // GET /api/v2/products/{id}
                product = restTemplate.getForObject(productServiceUrl + "/" + productId, ProductDTO.class);
            } catch (Exception e) {
                throw new RuntimeException("Failed to fetch Product info for ID: " + productId);
            }

            // ---------------------------------------------------------
            // B. Check & Reduce Stock (EXTERNAL CALL to Inventory Service)
            // ---------------------------------------------------------
            // Monolith: inventoryService.checkAndReduceStock(productId, quantity);
            try {
                // POST /api/v2/inventory/reduce
                InventoryRequest invReq = new InventoryRequest(productId, quantity);
                restTemplate.postForEntity(inventoryServiceUrl + "/reduce", invReq, String.class);
            } catch (HttpClientErrorException e) {
                // Activity 1 Service returns 409 Conflict if out of stock
                throw new RuntimeException("Out of Stock for: " + product.getName());
            }

            // ---------------------------------------------------------
            // C. Calculate Price (Same Logic)
            // ---------------------------------------------------------
            double itemTotal = product.getPrice() * quantity;
            calculatedTotal += itemTotal;

            // ---------------------------------------------------------
            // D. Create Order Item (Same DB Table Structure)
            // ---------------------------------------------------------
            OrderItem orderItem = new OrderItem();
            orderItem.setProductId(productId);
            orderItem.setProductName(product.getName());
            orderItem.setPrice(product.getPrice());
            orderItem.setQuantity(quantity);

            // E. Link to Order
            order.addOrderItem(orderItem);
        }

        // 4. Set Final Total
        order.setTotalAmount(calculatedTotal);

        // 5. Save Order (Local DB - Cascades to OrderItems)
        Order savedOrder = orderRepo.save(order);

        // ---------------------------------------------------------
        // 6. Process Payment (EXTERNAL CALL to Payment Service)
        // ---------------------------------------------------------
        try {
            // Prepare Request Payload
            PaymentRequest payReq = new PaymentRequest(savedOrder.getId(), calculatedTotal);

            // POST /api/v2/payments
            restTemplate.postForEntity(paymentServiceUrl, payReq, String.class);

            // If successful (200 OK), update status
            savedOrder.setStatus("PAID");
            orderRepo.save(savedOrder);

        } catch (Exception e) {
            // FAILED: Update status to FAILED so user knows
            savedOrder.setStatus("PAYMENT_FAILED");
            orderRepo.save(savedOrder);

            // Note: In a real Distributed System, we would need to trigger a
            // "Compensating Transaction" here to add items BACK to the Inventory.
            throw new RuntimeException("Payment Service Failed: " + e.getMessage());
        }

        // 7. Clear Cart (Shopping Domain)
        cartRepo.delete(cart);

        return savedOrder;
    }

    // Mock Payment Method
    private void processPaymentMock(Long orderId, double amount) {
        if (amount > 2000)
            throw new RuntimeException("Credit Limit Exceeded");
        System.out.println("Payment processed for Order " + orderId);
    }
}
