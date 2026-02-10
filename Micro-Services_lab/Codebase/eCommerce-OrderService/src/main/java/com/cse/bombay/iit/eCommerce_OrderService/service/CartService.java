package com.cse.bombay.iit.eCommerce_OrderService.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cse.bombay.iit.eCommerce_OrderService.model.Cart;
import com.cse.bombay.iit.eCommerce_OrderService.model.CartItem;
import com.cse.bombay.iit.eCommerce_OrderService.repository.CartRepository;

import jakarta.transaction.Transactional;

@Service
public class CartService {

    @Autowired
    private CartRepository cartRepo;

    @Transactional
    public Cart addToCart(Long userId, CartItem item) {
        // Business Logic: Find existing cart or create a new one
        Cart cart = cartRepo.findByUserId(userId)
                .orElse(new Cart());
        
        // Ensure the cart belongs to the correct user (if new)
        if (cart.getUserId() == null) {
            cart.setUserId(userId);
        }

        // Logic: Add item (in a real app, we'd check if product exists here too)
        cart.getItems().add(item);
        
        return cartRepo.save(cart);
    }
}
