package com.cse.bombay.iit.eCommerce_InventoryService.service;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.cse.bombay.iit.eCommerce_InventoryService.model.Inventory;
import com.cse.bombay.iit.eCommerce_InventoryService.repository.InventoryRepository;

@Service
public class InventoryService {

    @Autowired
    private InventoryRepository repository;

    // Get current stock
    public Integer getStock(Long productId) {
        return repository.findByProductId(productId)
                .map(Inventory::getQuantity)
                .orElse(0); // If not found, assume 0 stock
    }

    // Deduct stock (Returns true if successful, false if not enough stock)
    @Transactional
    public boolean reduceStock(Long productId, Integer quantity) {
        Inventory inventory = repository.findByProductId(productId)
                .orElseThrow(() -> new RuntimeException("Product not found in Inventory"));

        if (inventory.getQuantity() < quantity) {
            return false; // Not enough stock
        }

        inventory.setQuantity(inventory.getQuantity() - quantity);
        repository.save(inventory);
        return true;
    }
}
