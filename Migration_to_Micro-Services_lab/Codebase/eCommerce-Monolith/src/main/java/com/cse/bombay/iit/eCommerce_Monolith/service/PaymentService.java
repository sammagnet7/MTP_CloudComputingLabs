package com.cse.bombay.iit.eCommerce_Monolith.service;

import org.springframework.stereotype.Service;

@Service
public class PaymentService {
    public boolean processPayment(Double amount) {
        System.out.println("💳 [PAYMENT] Processing $" + amount);
        return true; // Always succeeds for demo
    }
}
