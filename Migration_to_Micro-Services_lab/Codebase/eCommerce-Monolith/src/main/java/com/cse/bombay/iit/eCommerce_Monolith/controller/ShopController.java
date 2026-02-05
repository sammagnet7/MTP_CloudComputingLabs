package com.cse.bombay.iit.eCommerce_Monolith.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import com.cse.bombay.iit.eCommerce_Monolith.model.Cart;
import com.cse.bombay.iit.eCommerce_Monolith.model.CartItem;
import com.cse.bombay.iit.eCommerce_Monolith.model.Order;
import com.cse.bombay.iit.eCommerce_Monolith.model.Product;
import com.cse.bombay.iit.eCommerce_Monolith.model.User;
import com.cse.bombay.iit.eCommerce_Monolith.repository.CartRepository;
import com.cse.bombay.iit.eCommerce_Monolith.repository.ProductRepository;
import com.cse.bombay.iit.eCommerce_Monolith.repository.UserRepository;
import com.cse.bombay.iit.eCommerce_Monolith.service.CheckoutService;

import java.util.List;

@RestController
@RequestMapping("/api")
public class ShopController {

    @Autowired
    private ProductRepository productRepo;
    @Autowired
    private UserRepository userRepo;
    @Autowired
    private CartRepository cartRepo;
    @Autowired
    private CheckoutService checkoutService;

    // --- Seeding Data for Demo ---
    @PostMapping("/seed")
    public String seedData() {
        User u = new User();
        u.setName("John Doe");
        u.setEmail("john@example.com");
        userRepo.save(u);

        Product p1 = new Product();
        p1.setName("Laptop");
        p1.setPrice(1000.0);
        p1.setStock(10);
        Product p2 = new Product();
        p2.setName("Mouse");
        p2.setPrice(50.0);
        p2.setStock(50);
        productRepo.saveAll(List.of(p1, p2));

        return "Database Seeded! User ID: " + u.getId();
    }

    // --- Shopping Cart Operations ---
    @PostMapping("/cart/{userId}/add")
    public Cart addToCart(@PathVariable Long userId, @RequestBody CartItem item) {
        Cart cart = cartRepo.findByUserId(userId).orElse(new Cart());
        cart.setUserId(userId);
        cart.getItems().add(item);
        return cartRepo.save(cart);
    }

    // --- The Big Monolith Operation ---
    @PostMapping("/checkout/{userId}")
    public Order checkout(@PathVariable Long userId) {
        return checkoutService.placeOrder(userId);
    }

    @GetMapping("/products")
    public List<Product> getAllProducts() {
        return productRepo.findAll();
    }

    @GetMapping("/users")
    public List<User> getAllUsers() {
        return userRepo.findAll();
    }
}
