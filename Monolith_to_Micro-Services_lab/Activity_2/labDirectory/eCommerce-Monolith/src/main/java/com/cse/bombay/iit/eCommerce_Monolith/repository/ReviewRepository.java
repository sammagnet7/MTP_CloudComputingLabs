package com.cse.bombay.iit.eCommerce_Monolith.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.cse.bombay.iit.eCommerce_Monolith.model.Review;

public interface ReviewRepository extends JpaRepository<Review, Long> {
    List<Review> findByProductId(Long productId);
}