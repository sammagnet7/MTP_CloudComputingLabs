package com.cse.bombay.iit.eCommerce_Monolith.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.cse.bombay.iit.eCommerce_Monolith.model.Order;

@Repository public interface OrderRepository extends JpaRepository<Order, Long> {

    List<Order> findByUserId(Long userId);
    
}