package com.cse.bombay.iit.eCommerce_Monolith.service;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cse.bombay.iit.eCommerce_Monolith.model.User;
import com.cse.bombay.iit.eCommerce_Monolith.repository.UserRepository;

import java.util.List;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepo;

    public List<User> getAllUsers() {
        return userRepo.findAll();
    }
}
