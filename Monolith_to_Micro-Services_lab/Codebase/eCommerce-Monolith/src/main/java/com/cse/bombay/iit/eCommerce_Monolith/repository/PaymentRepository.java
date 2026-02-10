package com.cse.bombay.iit.eCommerce_Monolith.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.cse.bombay.iit.eCommerce_Monolith.model.Payment;

public interface PaymentRepository extends JpaRepository<Payment, Long> {

    Optional<Payment> findByOrderId(Long orderId);

    @Query("SELECT p FROM Payment p WHERE p.orderId IN (SELECT o.id FROM Order o WHERE o.userId = :userId)")
    List<Payment> findHistoryByUserId(@Param("userId") Long userId);
}
