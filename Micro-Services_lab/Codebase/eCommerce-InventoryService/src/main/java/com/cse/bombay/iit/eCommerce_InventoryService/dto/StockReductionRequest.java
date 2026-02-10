package com.cse.bombay.iit.eCommerce_InventoryService.dto;

import lombok.Data;

@Data
public class StockReductionRequest {
    private Long productId;
    private Integer quantity;
}