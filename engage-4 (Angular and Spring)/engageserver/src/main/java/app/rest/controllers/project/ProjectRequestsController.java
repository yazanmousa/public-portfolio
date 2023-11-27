package app.rest.controllers.project;

import app.models.project.PendingRequest;
import app.models.project.ProjectMember;
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
public class ProjectRequestsController {

    @Autowired
    private Repository<PendingRequest> projectRequestsRepository;

    @GetMapping("/project-requests")
    public List<PendingRequest> findAll() {
        return projectRequestsRepository.findAll();
    }

    @GetMapping("/project-requests/{id}")
    public PendingRequest findById(@PathVariable long id) {
        PendingRequest projectRequest = projectRequestsRepository.findById(id);

        if (projectRequest == null) {
            throw new NotFoundException("No project request with id: " + id + " does not exist");
        }
        return projectRequest;
    }

    @PostMapping("/project-requests")
    public ResponseEntity<PendingRequest> addProject(@RequestBody PendingRequest projectRequest) {
        int previousRequestsLenght = projectRequestsRepository.findAll().size();
        PendingRequest savedProjectRequest = projectRequestsRepository.save(projectRequest);
        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(projectRequest.getId()).toUri();

        if (projectRequestsRepository.findAll().size() > previousRequestsLenght) {
            return ResponseEntity.created(location).body(savedProjectRequest);
        } else {
            return ResponseEntity.ok(savedProjectRequest);
        }
    }

    @PutMapping("/project-requests/{id}")
    public ResponseEntity<PendingRequest> updateProject(@RequestBody PendingRequest projectRequest, @PathVariable long id) {
        if (projectRequest.getId() != id) {
            throw new IdDoesNotMatchException("Project request: " + projectRequest.getId() + " does not match with paramaterID: " + id);
        }

        PendingRequest savedProjectRequest = projectRequestsRepository.save(projectRequest);

        return ResponseEntity.ok(savedProjectRequest);

    }

    @DeleteMapping("/project-requests/{id}")
    public ResponseEntity<PendingRequest> deleteProject(@PathVariable long id) {
        PendingRequest projectRequest = projectRequestsRepository.findById(id);

        projectRequestsRepository.deleteById(id);

        if (projectRequest == null) {
            throw new NotFoundException("Project with ID: " + id + " does not exist!");
        }

        return ResponseEntity.ok(projectRequest);
    }

    @DeleteMapping("/project-requests")
    public ResponseEntity<List<PendingRequest>> deleteMultipleRequests(@RequestBody List<PendingRequest> requests) {

        if (requests.size() < 1) {
            throw new NotFoundException("No project members were given as a request body");
        }

        for (PendingRequest request : requests) {
            projectRequestsRepository.deleteById(request.getId());
        }
        return ResponseEntity.ok(requests);
    }

}
