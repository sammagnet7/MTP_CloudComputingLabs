package com.cse.bombay.iit.eCommerce_Monolith.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.cse.bombay.iit.eCommerce_Monolith.model.Payment;

public interface PaymentRepository extends JpaRepository<Payment, Long> {}
