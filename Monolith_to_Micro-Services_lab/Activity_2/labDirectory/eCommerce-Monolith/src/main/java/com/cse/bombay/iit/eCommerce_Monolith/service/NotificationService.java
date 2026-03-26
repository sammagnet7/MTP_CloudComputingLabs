package com.cse.bombay.iit.eCommerce_Monolith.service;

import org.springframework.stereotype.Service;

@Service
public class NotificationService {
    // In a real app, this might save to a 'notification_log' table
    public void sendOrderConfirmation(String email, Long orderId) {
        System.out.println("📧 Sending email to " + email + " for Order #" + orderId);
        // Logic to insert into DB or call SMTP server
    }
}