package com.cse.bombay.iit.eCommerce_Monolith.model;

import com.fasterxml.jackson.annotation.JsonBackReference;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
public class OrderItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long productId;
    private String productName;
    private Double price; // Price at the time of purchase
    private Integer quantity;

    @ManyToOne
    @JoinColumn(name = "order_id")
    @JsonBackReference // Prevents infinite recursion in JSON
    private Order order;

    public OrderItem(Long productId, String productName, Double price, Integer quantity, Order order) {
        this.productId = productId;
        this.productName = productName;
        this.price = price;
        this.quantity = quantity;
        this.order = order;
    }
}
