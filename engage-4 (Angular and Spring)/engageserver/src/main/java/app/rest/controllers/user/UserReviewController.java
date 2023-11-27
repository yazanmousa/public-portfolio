package app.rest.controllers.user;

import app.models.project.PendingRequest;
import app.models.user.UserAttribute;
import app.models.user.UserReview;
import app.repositories.Repository;
import app.rest.exceptions.IdDoesNotMatchException;
import app.rest.exceptions.NotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.ArrayList;
import java.util.List;

@RestController
public class UserReviewController {

    @Autowired
    private Repository<UserReview> repository;

    @GetMapping("/user-reviews")
    public List<UserReview> findAll() {
        return repository.findAll();
    }

    @GetMapping("/user-reviews/{id}")
    public UserReview findById(@PathVariable long id) {

        UserReview review = repository.findById(id);

        if (review == null) {
            throw new NotFoundException("User review with ID: " + id + " does not exist!");
        }

        return review;
    }

    @PostMapping("/user-reviews")
    public ResponseEntity<UserReview> addUser(@RequestBody UserReview review) {

        int previousReviewsLength = repository.findAll().size();
        UserReview savedReview = repository.save(review);
        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(review.getId()).toUri();

        if (repository.findAll().size() > previousReviewsLength) {
            return ResponseEntity.created(location).body(savedReview);
        } else {
            return ResponseEntity.ok(savedReview);
        }

    }

    @PostMapping("/user-reviews/multiple")
    public ResponseEntity<UserReview[]> addMultipleReviews(@RequestBody UserReview[] reviews) {

        if (reviews.length < 1) {
            throw new NotFoundException("The list of reviews sent with the request body is empty");
        }

        int previousReviewsLength = repository.findAll().size();

        // Set the length to the same length of the reviews list that is being received as parameter
        UserReview[] savedReviews = new UserReview[reviews.length];

        for (int i = 0; i < reviews.length; i++) {
            UserReview savedReview = repository.save(reviews[i]);
            savedReviews[i] = savedReview;
        }

        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(savedReviews[0].getId()).toUri();

        if (repository.findAll().size() > previousReviewsLength) {
            return ResponseEntity.created(location).body(savedReviews);
        } else {
            return ResponseEntity.ok(savedReviews);
        }

    }

    @PutMapping("/user-reviews/{id}")
    public ResponseEntity<UserReview> updateUser(@RequestBody UserReview review, @PathVariable long id) {

        if (review.getId() != id) {
            throw new IdDoesNotMatchException("User review with id: " + review.getId() + " does not match with parameterID: " + id);
        }

        UserReview savedReview = repository.save(review);

        return ResponseEntity.ok(savedReview);

    }

    @DeleteMapping("/user-reviews/{id}")
    public ResponseEntity<UserReview> deleteUser(@PathVariable long id) {

        UserReview review = repository.findById(id);

        repository.deleteById(id);

        if (review == null) {
            throw new NotFoundException("Review with ID: " + id + " does not exist!");
        }

        return ResponseEntity.ok(review);
    }

    @DeleteMapping("/user-reviews")
    public ResponseEntity<List<UserReview>> deleteMultipleReviews(@RequestBody List<UserReview> reviews) {

        if (reviews.size() < 1) {
            throw new NotFoundException("No reviews were given as a request body");
        }

        for (UserReview review : reviews) {
            repository.deleteById(review.getId());
        }
        return ResponseEntity.ok(reviews);
    }

}
