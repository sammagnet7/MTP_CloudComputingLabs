package com.cse.bombay.iit.eCommerce_Monolith.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.cse.bombay.iit.eCommerce_Monolith.model.Cart;

@Repository public interface CartRepository extends JpaRepository<Cart, Long> {
    Optional<Cart> findByUserId(Long userId);
}
