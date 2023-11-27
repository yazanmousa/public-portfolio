package app.rest.controllers.organisation;

import app.models.organisation.Organisation;

import app.models.user.UserUpdate;
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
public class OrganisationController {

    @Autowired
    private Repository<Organisation> organisationsRepository;

    @GetMapping("/organisations")
    public List<Organisation> findAll() {
        return organisationsRepository.findAll();
    }

    @GetMapping("/organisations/{id}")
    public Organisation findById(@PathVariable long id) {

        Organisation organisation = organisationsRepository.findById(id);

        if (organisation == null) {
            throw new NotFoundException("Organisation with ID: " + id + " does not exist!");
        }

        return organisation;

    }
    

    @PostMapping("/organisations")
    public ResponseEntity<Organisation> addOrganisation(@RequestBody Organisation organisation) {

        int previousOrganisationsLength = organisationsRepository.findAll().size();

        Organisation savedOrganisation = organisationsRepository.save(organisation);

        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(organisation.getId()).toUri();
        if (organisationsRepository.findAll().size() > previousOrganisationsLength) {
            return ResponseEntity.created(location).body(savedOrganisation);
        } else {
            return ResponseEntity.ok(savedOrganisation);
        }
    }

    @PutMapping("/organisations/{id}")
    public ResponseEntity<Organisation> updateOrganisation(@RequestBody Organisation organisation, @PathVariable long id) {

        if (organisation.getId() != id) {
            throw new IdDoesNotMatchException("OrganisationID: " + organisation.getId() + " does not match with paramaterID: " + id);
        }

        Organisation savedOrganisation = organisationsRepository.save(organisation);

        return ResponseEntity.ok(savedOrganisation);

    }

    @DeleteMapping("/organisations/{id}")
    public ResponseEntity<Organisation> deleteOrganisation(@PathVariable long id) {

        Organisation organisation = organisationsRepository.findById(id);

        organisationsRepository.deleteById(id);

        if (organisation == null) {
            throw new NotFoundException("Organisation with ID: " + id + " does not exist!");
        }

        return ResponseEntity.ok(organisation);
    }


}
