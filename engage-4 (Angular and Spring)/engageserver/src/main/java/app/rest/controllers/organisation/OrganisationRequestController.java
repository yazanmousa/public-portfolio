package app.rest.controllers.organisation;

import app.models.organisation.OrganisationMember;
import app.models.organisation.PendingOrganisationRequest;
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
public class OrganisationRequestController {

    @Autowired
    private Repository<PendingOrganisationRequest> repository;

    @GetMapping("/organisation-requests")
    public List<PendingOrganisationRequest> findAll() {
        return repository.findAll();
    }

    @GetMapping("/organisation-requests/{id}")
    public PendingOrganisationRequest findById(@PathVariable long id) {

        PendingOrganisationRequest request = repository.findById(id);

        if (request == null) {
            throw new NotFoundException("Organisation Member with ID: " + id + " does not exist!");
        }

        return request;
    }


    @PostMapping("/organisation-requests")
    public ResponseEntity<PendingOrganisationRequest> addOrganisationMember(@RequestBody PendingOrganisationRequest request) {

        int previousRequestsLength = repository.findAll().size();

        PendingOrganisationRequest savedRequest = repository.save(request);

        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(request.getId()).toUri();
        if (repository.findAll().size() > previousRequestsLength) {
            return ResponseEntity.created(location).body(savedRequest);
        } else {
            return ResponseEntity.ok(savedRequest);
        }
    }


    @PutMapping("/organisation-requests/{id}")
    public ResponseEntity<PendingOrganisationRequest> updateOrganisationMember(@RequestBody PendingOrganisationRequest request, @PathVariable long id) {

        if (request.getId() != id) {
            throw new IdDoesNotMatchException("Organisation-request id: " + request.getId() + " does not match with paramaterID: " + id);
        }

        PendingOrganisationRequest savedRequest = repository.save(request);

        return ResponseEntity.ok(savedRequest);

    }

    @DeleteMapping("/organisation-requests/{id}")
    public ResponseEntity<PendingOrganisationRequest> deleteOrganisationMember(@PathVariable long id) {

        PendingOrganisationRequest request = repository.findById(id);

        repository.deleteById(id);

        if (request == null) {
            throw new NotFoundException("Organisation Request with ID: " + id + " does not exist!");
        }

        return ResponseEntity.ok(request);
    }

    @DeleteMapping("/organisation-requests")
    public ResponseEntity<List<PendingOrganisationRequest>> deleteMultipleRequests(@RequestBody List<PendingOrganisationRequest> requests) {

        if (requests.size() < 1) {
            throw new NotFoundException("No requests were given as a request body");
        }

        for (PendingOrganisationRequest request : requests) {
            repository.deleteById(request.getId());
        }
        return ResponseEntity.ok(requests);
    }

}
