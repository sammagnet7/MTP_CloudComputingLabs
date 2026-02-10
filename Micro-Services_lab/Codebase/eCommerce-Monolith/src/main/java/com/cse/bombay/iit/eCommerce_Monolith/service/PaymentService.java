package com.cse.bombay.iit.eCommerce_Monolith.service;

import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cse.bombay.iit.eCommerce_Monolith.model.Payment;
import com.cse.bombay.iit.eCommerce_Monolith.repository.PaymentRepository;

@Service
public class PaymentService {
    @Autowired private PaymentRepository paymentRepo;

    public void processPayment(Long orderId, Double amount) {
        // 1. Simulate external gateway call
        System.out.println("💳 Contacting PayPal/Stripe for $" + amount);
        
        // 2. Record transaction in OUR database
        Payment payment = new Payment();
        payment.setOrderId(orderId);
        payment.setAmount(amount);
        payment.setStatus("SUCCESS");
        payment.setTransactionId(UUID.randomUUID().toString());
        
        paymentRepo.save(payment);
    }

    public Payment getPaymentByOrderId(Long orderId) {
        return paymentRepo.findByOrderId(orderId)
                .orElseThrow(() -> new RuntimeException("Payment info not found for Order ID: " + orderId));
    }

    public List<Payment> getUserPaymentHistory(Long userId) {
        return paymentRepo.findHistoryByUserId(userId);
    }
}
