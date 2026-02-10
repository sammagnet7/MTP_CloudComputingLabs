package com.cse.bombay.iit.eCommerce_OrderService.model;

import jakarta.persistence.Embeddable;
import lombok.Data;

@Embeddable
@Data
public class CartItem {
    private Long productId;
    private Integer quantity;
}
