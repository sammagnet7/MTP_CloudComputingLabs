package com.cse.bombay.iit.eCommerce_Monolith.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.cse.bombay.iit.eCommerce_Monolith.model.User;

@Repository public interface UserRepository extends JpaRepository<User, Long> {}

