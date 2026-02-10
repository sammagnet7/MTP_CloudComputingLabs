package com.cse.bombay.iit.eCommerce_Monolith.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.cse.bombay.iit.eCommerce_Monolith.model.Product;
import com.cse.bombay.iit.eCommerce_Monolith.model.Review;
import com.cse.bombay.iit.eCommerce_Monolith.repository.ProductRepository;
import com.cse.bombay.iit.eCommerce_Monolith.repository.ReviewRepository;

@Service
public class ReviewService {
    @Autowired private ReviewRepository reviewRepo;
    @Autowired private ProductRepository productRepo;

    public Review addReview(Long productId, String userName, Integer rating, String comment) {
        Product product = productRepo.findById(productId)
                .orElseThrow(() -> new RuntimeException("Product not found"));
        
        Review review = new Review();
        review.setProduct(product);
        review.setUserName(userName);
        review.setRating(rating);
        review.setComment(comment);
        
        return reviewRepo.save(review);
    }

    public List<Review> getReviewsByProductId(Long productId) {
        if (!productRepo.existsById(productId)) {
            throw new RuntimeException("Product not found");
        }
        return reviewRepo.findByProductId(productId);
    }
}
