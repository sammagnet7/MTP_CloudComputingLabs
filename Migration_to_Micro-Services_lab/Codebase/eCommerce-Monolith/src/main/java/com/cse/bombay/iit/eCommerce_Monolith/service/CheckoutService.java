package com.cse.bombay.iit.eCommerce_Monolith.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.cse.bombay.iit.eCommerce_Monolith.model.Cart;
import com.cse.bombay.iit.eCommerce_Monolith.model.CartItem;
import com.cse.bombay.iit.eCommerce_Monolith.model.Order;
import com.cse.bombay.iit.eCommerce_Monolith.model.Product;
import com.cse.bombay.iit.eCommerce_Monolith.model.User;
import com.cse.bombay.iit.eCommerce_Monolith.repository.CartRepository;
import com.cse.bombay.iit.eCommerce_Monolith.repository.OrderRepository;
import com.cse.bombay.iit.eCommerce_Monolith.repository.ProductRepository;
import com.cse.bombay.iit.eCommerce_Monolith.repository.UserRepository;

@Service
public class CheckoutService {

    @Autowired
    private CartRepository cartRepo;
    @Autowired
    private ProductRepository productRepo;
    @Autowired
    private OrderRepository orderRepo;
    @Autowired
    private UserRepository userRepo;

    // TIGHT COUPLING: Direct dependency on other "domains"
    @Autowired
    private PaymentService paymentService;
    @Autowired
    private NotificationService notificationService;

    @Transactional
    public Order placeOrder(Long userId) {
        // 1. Get Cart
        Cart cart = cartRepo.findByUserId(userId)
                .orElseThrow(() -> new RuntimeException("Cart empty"));

        // 2. Calculate Total & Check Stock
        double total = 0.0;
        for (CartItem item : cart.getItems()) {
            Product p = productRepo.findById(item.getProductId()).orElseThrow();
            if (p.getStock() < item.getQuantity()) {
                throw new RuntimeException("Out of stock: " + p.getName());
            }
            total += p.getPrice() * item.getQuantity();
        }

        // 3. Process Payment
        if (!paymentService.processPayment(total)) {
            throw new RuntimeException("Payment failed");
        }

        // 4. Update Stock
        for (CartItem item : cart.getItems()) {
            Product p = productRepo.findById(item.getProductId()).get();
            p.setStock(p.getStock() - item.getQuantity());
            productRepo.save(p);
        }

        // 5. Save Order
        Order order = new Order();
        order.setUserId(userId);
        order.setTotalAmount(total);
        order.setStatus("PAID");
        orderRepo.save(order);

        // 6. Clear Cart
        cartRepo.delete(cart);

        // 7. Notify User
        User user = userRepo.findById(userId).orElseThrow();
        notificationService.sendEmail(user.getEmail(), "Order " + order.getId() + " Confirmed!");

        return order;
    }
}