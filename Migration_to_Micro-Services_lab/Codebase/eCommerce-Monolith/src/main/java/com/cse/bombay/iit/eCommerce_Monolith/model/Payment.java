package com.cse.bombay.iit.eCommerce_Monolith.model;

import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Data;

@Entity
@Data
public class Payment {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private Long orderId;
    private Double amount;
    private String status; // SUCCESS, FAILED
    private String transactionId;
    private LocalDateTime timestamp = LocalDateTime.now();
}