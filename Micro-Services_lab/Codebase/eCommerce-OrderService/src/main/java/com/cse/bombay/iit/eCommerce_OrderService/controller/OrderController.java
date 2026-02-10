package com.cse.bombay.iit.eCommerce_OrderService.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import com.cse.bombay.iit.eCommerce_OrderService.model.Cart;
import com.cse.bombay.iit.eCommerce_OrderService.model.CartItem;
import com.cse.bombay.iit.eCommerce_OrderService.model.Order;
import com.cse.bombay.iit.eCommerce_OrderService.service.CartService;
import com.cse.bombay.iit.eCommerce_OrderService.service.CheckoutService;
import com.cse.bombay.iit.eCommerce_OrderService.service.OrderService;

@RestController
@RequestMapping("/api/v2/orders")
public class OrderController {

    @Autowired
    private CartService cartService;
    @Autowired
    private CheckoutService checkoutService;
    @Autowired
    private OrderService orderService;


    @PostMapping("/checkout/{userId}")
    public Order checkout(@PathVariable Long userId) {
        // Delegate complex transaction to Service
        return checkoutService.placeOrder(userId);
    }

    @PostMapping("/cart/{userId}/add")
    public Cart addToCart(@PathVariable Long userId, @RequestBody CartItem item) {
        // Delegate complex logic to Service
        return cartService.addToCart(userId, item);
    }

    // 1. GET User's Order History
    @GetMapping("/users/{userId}")
    public List<Order> getUserOrders(@PathVariable Long userId) {
        return orderService.getUserOrders(userId);
    }

    // 2. GET Specific Order Details
    @GetMapping("/{orderId}")
    public Order getOrderDetails(@PathVariable Long orderId) {
        return orderService.getOrderById(orderId);
    }
}