package com.cse.bombay.iit.eCommerce_InventoryService.repository;


import org.springframework.data.jpa.repository.JpaRepository;

import com.cse.bombay.iit.eCommerce_InventoryService.model.Inventory;

import java.util.Optional;

public interface InventoryRepository extends JpaRepository<Inventory, Long> {
    Optional<Inventory> findByProductId(Long productId);
}