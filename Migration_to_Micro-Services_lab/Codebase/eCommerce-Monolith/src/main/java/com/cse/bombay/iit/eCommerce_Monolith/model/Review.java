package com.cse.bombay.iit.eCommerce_Monolith.model;

import java.time.LocalDateTime;

import com.fasterxml.jackson.annotation.JsonIgnore;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import lombok.Data;

@Entity
@Data
public class Review {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "product_id")
    @JsonIgnore // Prevent infinite recursion in JSON
    private Product product;
    
    private String userName;
    private Integer rating;
    private String comment;
    private LocalDateTime createdAt = LocalDateTime.now();
}