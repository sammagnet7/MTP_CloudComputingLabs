package com.cse.bombay.iit.eCommerce_Monolith.model;

import jakarta.persistence.*;
import lombok.Data;

// 👤 User Entity
@Entity
@Data
@Table(name = "users")
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String email;
    private String name;
    private String address;

}