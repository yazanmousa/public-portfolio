package app.rest.controllers.user;

import app.models.user.User;
import app.repositories.Repository;
import app.rest.exceptions.IdDoesNotMatchException;
import app.rest.exceptions.NotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.List;

@RestController
public class UserController {

    @Autowired
    private Repository<User> usersRepository;


    @GetMapping("/users")
    public List<User> findAll() {
        return usersRepository.findAll();
    }

    @GetMapping("/users/{id}")
    public User findById(@PathVariable long id) {

        User user = usersRepository.findById(id);

        if (user == null) {
            throw new NotFoundException("User with ID: " + id + " does not exist!");
        }

        return user;
    }

    @PostMapping("/users")
    public ResponseEntity<User> addUser(@RequestBody User user) {

        int previousUsersLength = usersRepository.findAll().size();
        User savedUser = usersRepository.save(user);
        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(user.getId()).toUri();

        if (usersRepository.findAll().size() > previousUsersLength) {
            return ResponseEntity.created(location).body(savedUser);
        } else {
            return ResponseEntity.ok(savedUser);
        }

    }

    @PutMapping("/users/{id}")
    public ResponseEntity<User> updateUser(@RequestBody User user, @PathVariable long id) {

        if (user.getId() != id) {
            throw new IdDoesNotMatchException("UserID: " + user.getId() + " does not match with parameterID: " + id);
        }

        User savedUser = usersRepository.save(user);

        return ResponseEntity.ok(savedUser);

    }

    @DeleteMapping("/users/{id}")
    public ResponseEntity<User> deleteUser(@PathVariable long id) {

        User user = usersRepository.findById(id);

        usersRepository.deleteById(id);

        if (user == null) {
            throw new NotFoundException("User with ID: " + id + " does not exist!");
        }

        return ResponseEntity.ok(user);

    }

}
