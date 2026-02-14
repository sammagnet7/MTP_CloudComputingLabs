package com.cse.bombay.iit.eCommerce_OrderService.repository;


import org.springframework.data.jpa.repository.JpaRepository;

import com.cse.bombay.iit.eCommerce_OrderService.model.Cart;

import java.util.Optional;

public interface CartRepository extends JpaRepository<Cart, Long> {
    Optional<Cart> findByUserId(Long userId);
}
