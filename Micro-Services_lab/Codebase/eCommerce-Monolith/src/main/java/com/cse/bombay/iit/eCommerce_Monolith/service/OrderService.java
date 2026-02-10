package com.cse.bombay.iit.eCommerce_Monolith.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cse.bombay.iit.eCommerce_Monolith.model.Order;
import com.cse.bombay.iit.eCommerce_Monolith.repository.OrderRepository;

@Service
public class OrderService {

    @Autowired
    private OrderRepository orderRepo;

    // Existing checkout logic...

    // ✅ ADD: Get all orders for a user
    public List<Order> getUserOrders(Long userId) {
        return orderRepo.findByUserId(userId);
    }
    
    // ✅ ADD: Get specific order
    public Order getOrderById(Long orderId) {
        return orderRepo.findById(orderId)
            .orElseThrow(() -> new RuntimeException("Order not found"));
    }
}
