package app.rest.controllers.user;

import app.models.user.UserReview;
import app.models.user.UserUpdate;
import app.repositories.Repository;
import app.rest.exceptions.IdDoesNotMatchException;
import app.rest.exceptions.NotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.ArrayList;
import java.util.List;

@RestController
public class UserUpdateController {

    @Autowired
    private Repository<UserUpdate> repository;

    @GetMapping("/user-updates")
    public List<UserUpdate> findAll() {
        return repository.findAll();
    }

    @GetMapping("/user-updates/{id}")
    public UserUpdate findById(@PathVariable long id) {

        UserUpdate update = repository.findById(id);

        if (update == null) {
            throw new NotFoundException("User update with ID: " + id + " does not exist!");
        }

        return update;
    }

    @PostMapping("/user-updates")
    public ResponseEntity<UserUpdate> addUserUpdate(@RequestBody UserUpdate update) {

        int previousUpdatesLength = repository.findAll().size();
        UserUpdate savedUpdate = repository.save(update);
        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(update.getId()).toUri();

        if (repository.findAll().size() > previousUpdatesLength) {
            return ResponseEntity.created(location).body(savedUpdate);
        } else {
            return ResponseEntity.ok(savedUpdate);
        }

    }

    @PostMapping("/user-updates/multiple")
    public ResponseEntity<UserUpdate[]> addMultipleUpdates(@RequestBody UserUpdate[] updates) {
        
        if (updates.length < 1) {
            throw new NotFoundException("The list of updates sent with the request body is empty");
        }

        int previousUpdatesLength = repository.findAll().size();
        UserUpdate[] savedUpdates = new UserUpdate[updates.length];
        for (int i = 0; i < updates.length; i++) {
            UserUpdate savedUpdate = repository.save(updates[i]);
            savedUpdates[i] = savedUpdate;
        }

        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(savedUpdates[0].getId()).toUri();

        if (repository.findAll().size() > previousUpdatesLength) {
            return ResponseEntity.created(location).body(savedUpdates);
        } else {
            return ResponseEntity.ok(savedUpdates);
        }

    }

    @PutMapping("/user-updates/{id}")
    public ResponseEntity<UserUpdate> updateUser(@RequestBody UserUpdate update, @PathVariable long id) {

        if (update.getId() != id) {
            throw new IdDoesNotMatchException("User update with id: " + update.getId() + " does not match with parameterID: " + id);
        }

        UserUpdate savedUpdate = repository.save(update);

        return ResponseEntity.ok(savedUpdate);

    }

    @DeleteMapping("/user-updates/{id}")
    public ResponseEntity<UserUpdate> deleteUser(@PathVariable long id) {

        UserUpdate update = repository.findById(id);

        repository.deleteById(id);

        if (update == null) {
            throw new NotFoundException("Update with ID: " + id + " does not exist!");
        }

        return ResponseEntity.ok(update);
    }

    @DeleteMapping("/user-updates")
    public ResponseEntity<List<UserUpdate>> deleteMultipleUpdates(@RequestBody List<UserUpdate> updates) {

        if (updates.size() < 1) {
            throw new NotFoundException("No updates were given as a request body");
        }

        for (UserUpdate update : updates) {
            repository.deleteById(update.getId());
        }
        return ResponseEntity.ok(updates);
    }

}
