package com.cse.bombay.iit.eCommerce_Monolith.service;

import org.springframework.stereotype.Service;

@Service
public class NotificationService {
    public void sendEmail(String email, String subject) {
        System.out.println("📧 [EMAIL SENT] To: " + email + " | Subject: " + subject);
    }
}