package com.cse.bombay.iit.eCommerce_Monolith.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cse.bombay.iit.eCommerce_Monolith.model.Cart;
import com.cse.bombay.iit.eCommerce_Monolith.model.CartItem;
import com.cse.bombay.iit.eCommerce_Monolith.model.Order;
import com.cse.bombay.iit.eCommerce_Monolith.model.Product;
import com.cse.bombay.iit.eCommerce_Monolith.model.User;
import com.cse.bombay.iit.eCommerce_Monolith.repository.CartRepository;
import com.cse.bombay.iit.eCommerce_Monolith.repository.OrderRepository;
import com.cse.bombay.iit.eCommerce_Monolith.repository.UserRepository;

import jakarta.transaction.Transactional;

@Service
public class CheckoutService {

    @Autowired private CartRepository cartRepo;
    @Autowired private OrderRepository orderRepo;
    @Autowired private UserRepository userRepo;
    
    // THE SEAMS: We inject the new services here
    @Autowired private InventoryService inventoryService;
    @Autowired private PaymentService paymentService;
    @Autowired private NotificationService notificationService;

    @Transactional
    public Order placeOrder(Long userId) {
        // 1. Get Cart
        Cart cart = cartRepo.findByUserId(userId)
                .orElseThrow(() -> new RuntimeException("Cart empty"));
        if(cart.getItems().isEmpty()) throw new RuntimeException("Cart is empty");

        User user = userRepo.findById(userId).orElseThrow();

        // 2. Calculate Total & Prepare Order Items
        double total = 0.0;
        List<Product> productsToOrder = new ArrayList<>(); // To hold temp data
        
        // 3. INVENTORY SERVICE CALL (Step 1)
        for (CartItem item : cart.getItems()) {
            boolean hasStock = inventoryService.checkAndReduceStock(item.getProductId(), item.getQuantity());
            if (!hasStock) {
                throw new RuntimeException("Product ID " + item.getProductId() + " is out of stock!");
            }
            // Logic to calculate price would usually fetch from ProductService here
            // For brevity, assuming we have price access or passed it in
        }
        
        // (Simplified total calc for demo)
        total = 100.00; 

        // 4. SAVE ORDER (Pending State)
        Order order = new Order();
        order.setUserId(userId);
        order.setTotalAmount(total);
        order.setStatus("PROCESSING");
        order = orderRepo.save(order);

        // 5. PAYMENT SERVICE CALL (Step 2)
        try {
            paymentService.processPayment(order.getId(), total);
            order.setStatus("PAID");
        } catch (Exception e) {
            order.setStatus("PAYMENT_FAILED");
            // In real world: Rollback inventory here!
            orderRepo.save(order);
            throw new RuntimeException("Payment failed");
        }
        orderRepo.save(order);

        // 6. CLEAR CART
        cartRepo.delete(cart);

        // 7. NOTIFICATION SERVICE CALL (Step 3)
        notificationService.sendOrderConfirmation(user.getEmail(), order.getId());

        return order;
    }
}