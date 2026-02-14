package com.cse.bombay.iit.eCommerce_OrderService.repository;


import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.cse.bombay.iit.eCommerce_OrderService.model.Order;

public interface OrderRepository extends JpaRepository<Order, Long> {

    List<Order> findByUserId(Long userId);
}
