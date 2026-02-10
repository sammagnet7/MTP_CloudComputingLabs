package com.cse.bombay.iit.eCommerce_InventoryService.controller;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.cse.bombay.iit.eCommerce_InventoryService.dto.StockReductionRequest;
import com.cse.bombay.iit.eCommerce_InventoryService.service.InventoryService;

@RestController
@RequestMapping("/api/v2/inventory")
public class InventoryController {

    @Autowired
    private InventoryService inventoryService;

    @GetMapping("/{productId}")
    public ResponseEntity<Integer> getStock(@PathVariable Long productId) {
        Integer stock = inventoryService.getStock(productId);
        return ResponseEntity.ok(stock);
    }

    @PostMapping("/reduce")
    public ResponseEntity<String> reduceStock(@RequestBody StockReductionRequest request) {
        boolean success = inventoryService.reduceStock(request.getProductId(), request.getQuantity());
        
        if (success) {
            return ResponseEntity.ok("Stock deducted successfully");
        } else {
            return ResponseEntity.status(409).body("Insufficient Stock");
        }
    }
}