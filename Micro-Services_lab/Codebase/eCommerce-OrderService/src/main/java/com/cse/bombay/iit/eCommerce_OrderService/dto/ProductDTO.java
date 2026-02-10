package com.cse.bombay.iit.eCommerce_OrderService.dto;

import lombok.Data;

@Data
public class ProductDTO {
    private Long id;
    private String name;
    private Double price; // Crucial: We get price from Source of Truth
}
