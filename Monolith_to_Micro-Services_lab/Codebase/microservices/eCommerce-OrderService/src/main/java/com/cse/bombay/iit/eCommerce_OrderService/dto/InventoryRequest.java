package com.cse.bombay.iit.eCommerce_OrderService.dto;


import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class InventoryRequest {
    private Long productId;
    private Integer quantity;
}
