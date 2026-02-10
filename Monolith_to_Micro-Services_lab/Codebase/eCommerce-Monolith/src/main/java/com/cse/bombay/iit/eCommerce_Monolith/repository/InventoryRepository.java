package com.cse.bombay.iit.eCommerce_Monolith.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.cse.bombay.iit.eCommerce_Monolith.model.Inventory;

public interface InventoryRepository extends JpaRepository<Inventory, Long> {
    Optional<Inventory> findByProductId(Long productId);
}
