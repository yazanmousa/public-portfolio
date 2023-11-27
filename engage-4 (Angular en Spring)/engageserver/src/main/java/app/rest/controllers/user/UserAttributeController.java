package app.rest.controllers.user;

import app.models.user.UserAttribute;
import app.models.user.UserReview;
import app.repositories.Repository;
import app.rest.exceptions.IdDoesNotMatchException;
import app.rest.exceptions.NotFoundException;
import org.apache.coyote.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.ArrayList;
import java.util.List;

@RestController
public class UserAttributeController {

    @Autowired
    private Repository<UserAttribute> repository;

    @GetMapping("/user-attributes")
    public List<UserAttribute> findAll() {
        return repository.findAll();
    }

    @GetMapping("/user-attributes/{id}")
    public UserAttribute findById(@PathVariable long id) {

        UserAttribute attribute = repository.findById(id);

        if (attribute == null) {
            throw new NotFoundException("User Attribute with ID: " + id + " does not exist!");
        }

        return attribute;
    }

    @PostMapping("/user-attributes")
    public ResponseEntity<UserAttribute> addUser(@RequestBody UserAttribute attribute) {

        int previousAttributesLength = repository.findAll().size();
        UserAttribute savedAttribute = repository.save(attribute);
        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(attribute.getId()).toUri();

        if (repository.findAll().size() > previousAttributesLength) {
            return ResponseEntity.created(location).body(savedAttribute);
        } else {
            return ResponseEntity.ok(savedAttribute);
        }

    }

    @PostMapping("/user-attributes/multiple")
    public ResponseEntity<UserAttribute[]> addMultipleAttributes(@RequestBody UserAttribute[] attributes) {

        if (attributes.length < 1) {
            throw new NotFoundException("The list of attributes sent with the request body is empty");
        }

        int previousAttributesLength = repository.findAll().size();
        UserAttribute[] savedAttributes = new UserAttribute[attributes.length];

        for (int i = 0; i < attributes.length; i++) {
            UserAttribute savedAttribute = repository.save(attributes[i]);
            savedAttributes[i] = savedAttribute;
        }

        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(savedAttributes[0].getId()).toUri();

        if (repository.findAll().size() > previousAttributesLength) {
            return ResponseEntity.created(location).body(savedAttributes);
        } else {
            return ResponseEntity.ok(savedAttributes);
        }
    }

    @PutMapping("/user-attributes/{id}")
    public ResponseEntity<UserAttribute> updateUser(@RequestBody UserAttribute attribute, @PathVariable long id) {

        if (attribute.getId() != id) {
            throw new IdDoesNotMatchException("User Attribute id: " + attribute.getId() + " does not match with parameterID: " + id);
        }

        UserAttribute savedAttribute = repository.save(attribute);

        return ResponseEntity.ok(savedAttribute);

    }

    @DeleteMapping("/user-attributes/{id}")
    public ResponseEntity<UserAttribute> deleteUser(@PathVariable long id) {

        UserAttribute attribute = repository.findById(id);

        repository.deleteById(id);

        if (attribute == null) {
            throw new NotFoundException("Userattribute with ID: " + id + " does not exist!");
        }

        return ResponseEntity.ok(attribute);
    }

    @DeleteMapping("/user-attributes")
    public ResponseEntity<List<UserAttribute>> deleteMultipleAttributes(@RequestBody List<UserAttribute> attributes) {

        if (attributes.size() < 1) {
            throw new NotFoundException("No attributes were given as a request body");
        }

        for (UserAttribute attribute : attributes) {
            repository.deleteById(attribute.getId());
        }
        return ResponseEntity.ok(attributes);
    }

}
