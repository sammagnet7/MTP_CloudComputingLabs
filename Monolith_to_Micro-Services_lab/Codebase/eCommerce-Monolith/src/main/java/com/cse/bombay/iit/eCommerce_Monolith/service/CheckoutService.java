package com.cse.bombay.iit.eCommerce_Monolith.service;

import java.time.LocalDateTime;
import java.util.ArrayList;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cse.bombay.iit.eCommerce_Monolith.model.Cart;
import com.cse.bombay.iit.eCommerce_Monolith.model.CartItem;
import com.cse.bombay.iit.eCommerce_Monolith.model.Order;
import com.cse.bombay.iit.eCommerce_Monolith.model.OrderItem;
import com.cse.bombay.iit.eCommerce_Monolith.model.Product;
//import com.cse.bombay.iit.eCommerce_Monolith.model.User;
import com.cse.bombay.iit.eCommerce_Monolith.repository.CartRepository;
import com.cse.bombay.iit.eCommerce_Monolith.repository.OrderRepository;

import jakarta.transaction.Transactional;

@Service
public class CheckoutService {

    @Autowired private CartRepository cartRepo;
    @Autowired private OrderRepository orderRepo;
    @Autowired private ProductService productService;
    @Autowired private InventoryService inventoryService;
    @Autowired private PaymentService paymentService;

    @Transactional
    public Order placeOrder(Long userId) {
        // 1. Get User's Cart
        Cart cart = cartRepo.findByUserId(userId)
                .orElseThrow(() -> new RuntimeException("Cart not found for user: " + userId));

        if (cart.getItems().isEmpty()) {
            throw new RuntimeException("Cart is empty! Add items before checkout.");
        }

        // 2. Prepare Order Object
        Order order = new Order();
        order.setUserId(userId);
        order.setCreatedAt(LocalDateTime.now());
        order.setStatus("PROCESSING");
        order.setItems(new ArrayList<>()); // Initialize list to avoid NullPointer

        double calculatedTotal = 0.0;

        // 3. Process Each Cart Item
        for (CartItem cartItem : cart.getItems()) {
            Long productId = cartItem.getProductId();
            int quantity = cartItem.getQuantity();

            // A. Fetch Product (To get real Name & Price)
            Product product = productService.getProductById(productId);

            // B. Check & Reduce Stock (Inventory Domain)
            boolean hasStock = inventoryService.checkAndReduceStock(productId, quantity);
            if (!hasStock) {
                throw new RuntimeException("Out of Stock: " + product.getName());
            }

            // C. Calculate Price for this item
            double itemTotal = product.getPrice() * quantity;
            calculatedTotal += itemTotal;

            // D. Create Order Item (History Record)
            // This preserves the price *at the time of purchase*
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

        // 5. Save Order (Cascade will save OrderItems automatically)
        Order savedOrder = orderRepo.save(order);

        // 6. Process Payment (Payment Domain)
        try {
            // We pass the REAL calculated total here
            paymentService.processPayment(savedOrder.getId(), calculatedTotal);
            
            // If successful, update status
            savedOrder.setStatus("PAID");
            orderRepo.save(savedOrder);
            
        } catch (Exception e) {
            // If Payment fails, RuntimeException triggers @Transactional rollback
            // This undoes the Inventory reduction and Order save automatically
            throw new RuntimeException("Payment Failed: " + e.getMessage());
        }

        // 7. Clear Cart (Shopping Domain)
        cartRepo.delete(cart);

        return savedOrder;
    }
}