package com.cse.bombay.iit.eCommerce_Monolith.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cse.bombay.iit.eCommerce_Monolith.model.Inventory;
import com.cse.bombay.iit.eCommerce_Monolith.repository.InventoryRepository;

@Service
public class InventoryService {
    @Autowired private InventoryRepository inventoryRepo;

    public boolean checkAndReduceStock(Long productId, Integer quantity) {
        Inventory inventory = inventoryRepo.findByProductId(productId)
                .orElseThrow(() -> new RuntimeException("Product " + productId + " not found in inventory"));

        if (inventory.getQuantity() < quantity) {
            return false; // Out of stock
        }

        inventory.setQuantity(inventory.getQuantity() - quantity);
        inventoryRepo.save(inventory);
        return true;
    }
    
    public Integer getStock(Long productId) {
        return inventoryRepo.findByProductId(productId)
                .map(Inventory::getQuantity)
                .orElse(0);
    }
}
