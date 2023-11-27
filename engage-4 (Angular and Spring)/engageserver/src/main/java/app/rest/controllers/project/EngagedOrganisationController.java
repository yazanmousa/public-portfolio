package app.rest.controllers.project;

import app.models.organisation.PendingOrganisationRequest;
import app.models.project.EngagedOrganisation;
import app.models.user.UserUpdate;
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
public class EngagedOrganisationController {

    @Autowired
    private Repository<EngagedOrganisation> repository;

    @GetMapping("/engaged-organisations")
    public List<EngagedOrganisation> findAll() {
        return repository.findAll();
    }

    @GetMapping("engaged-organisations/{id}")
    public EngagedOrganisation findById(@PathVariable long id) {
        EngagedOrganisation engagedOrganisation = repository.findById(id);

        if (engagedOrganisation == null) {
            throw new NotFoundException("No engagedOrganisation with id: " + id + " does not exist");
        }
        return engagedOrganisation;
    }

    @PostMapping("/engaged-organisations")
    public ResponseEntity<EngagedOrganisation> addEngagedOrganisation(@RequestBody EngagedOrganisation engagedOrganisation) {
        int previousEngagedOrganisationsLenght = repository.findAll().size();
        EngagedOrganisation savedEngagedOrganisation = repository.save(engagedOrganisation);
        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(engagedOrganisation.getId()).toUri();

        if (repository.findAll().size() > previousEngagedOrganisationsLenght) {
            return ResponseEntity.created(location).body(savedEngagedOrganisation);
        } else {
            return ResponseEntity.ok(savedEngagedOrganisation);
        }
    }

    @PostMapping("/engaged-organisations/multiple")
    public ResponseEntity<EngagedOrganisation[]> addMultipleEngagedOrganisations(@RequestBody EngagedOrganisation[] engagedOrganisations) {

        if (engagedOrganisations.length < 1) {
            throw new NotFoundException("The list of engaged organisations sent with the request body is empty");
        }

        int previousEngagedOrganisationsLength = repository.findAll().size();
        EngagedOrganisation[] savedEngagedOrganisations = new EngagedOrganisation[engagedOrganisations.length];

        for (int i = 0; i < engagedOrganisations.length; i++) {
            EngagedOrganisation savedOrganisation = repository.save(engagedOrganisations[i]);
            savedEngagedOrganisations[i] = savedOrganisation;
        }

        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(savedEngagedOrganisations[0].getId()).toUri();

        if (repository.findAll().size() > previousEngagedOrganisationsLength) {
            return ResponseEntity.created(location).body(savedEngagedOrganisations);
        } else {
            return ResponseEntity.ok(savedEngagedOrganisations);
        }

    }

    @PutMapping("/engaged-organisations/{id}")
    public ResponseEntity<EngagedOrganisation> updateEngagedOrganisation(@RequestBody EngagedOrganisation engagedOrganisation, @PathVariable long id) {
        if (engagedOrganisation.getId() != id) {
            throw new IdDoesNotMatchException("EngagedOrganisation: " + engagedOrganisation.getId() + " does not match with paramaterID: " + id);
        }

        EngagedOrganisation savedEngagedOrganisation = repository.save(engagedOrganisation);

        return ResponseEntity.ok(savedEngagedOrganisation);

    }

    @DeleteMapping("/engaged-organisations/{id}")
    public ResponseEntity<EngagedOrganisation> deleteEngagedOrganisation(@PathVariable long id) {
        EngagedOrganisation engagedOrganisation = repository.findById(id);

        repository.deleteById(id);

        if (engagedOrganisation == null) {
            throw new NotFoundException("EngagedOrganisation with ID: " + id + " does not exist!");
        }

        return ResponseEntity.ok(engagedOrganisation);
    }

    @DeleteMapping("/engaged-organisations")
    public ResponseEntity<List<EngagedOrganisation>> deleteMultipleEngagedOrganisation(@RequestBody List<EngagedOrganisation> organisations) {

        if (organisations.size() < 1) {
            throw new NotFoundException("No engaged organisations were given as a request body");
        }

        for (EngagedOrganisation organisation : organisations) {
            repository.deleteById(organisation.getId());
        }
        return ResponseEntity.ok(organisations);
    }

}
