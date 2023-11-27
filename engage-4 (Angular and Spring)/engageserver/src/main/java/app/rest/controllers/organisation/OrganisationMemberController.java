package app.rest.controllers.organisation;

import app.models.organisation.OrganisationMember;
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
public class OrganisationMemberController {

    @Autowired
    private Repository<OrganisationMember> repository;

    @GetMapping("/organisation-members")
    public List<OrganisationMember> findAll() {
        return repository.findAll();
    }

    @GetMapping("/organisation-members/{id}")
    public OrganisationMember findById(@PathVariable long id) {

        OrganisationMember organisationMember = repository.findById(id);

        if (organisationMember == null) {
            throw new NotFoundException("Organisation Member with ID: " + id + " does not exist!");
        }

        return organisationMember;

    }

    @PostMapping("/organisation-members")
    public ResponseEntity<OrganisationMember> addOrganisationMember(@RequestBody OrganisationMember organisationMember) {

        try {
        int previousOrganisationsMembersLength = repository.findAll().size();

        OrganisationMember savedOrganisation = repository.save(organisationMember);

        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(organisationMember.getId()).toUri();
        if (repository.findAll().size() > previousOrganisationsMembersLength) {
            return ResponseEntity.created(location).body(savedOrganisation);
        } else {
            return ResponseEntity.ok(savedOrganisation);
        }} catch (Exception e) {
            System.out.println(e);
            return null;
        }
    }


    @PutMapping("/organisation-members/{id}")
    public ResponseEntity<OrganisationMember> updateOrganisationMember(@RequestBody OrganisationMember organisationMember, @PathVariable long id) {

        if (organisationMember.getId() != id) {
            throw new IdDoesNotMatchException("Organisation-member id: " + organisationMember.getId() + " does not match with paramaterID: " + id);
        }

        OrganisationMember savedOrganisationMember = repository.save(organisationMember);

        return ResponseEntity.ok(savedOrganisationMember);

    }

    @DeleteMapping("/organisation-members/{id}")
    public ResponseEntity<OrganisationMember> deleteOrganisationMember(@PathVariable long id) {

        OrganisationMember organisationMember = repository.findById(id);

        repository.deleteById(id);

        if (organisationMember == null) {
            throw new NotFoundException("Organisation Member with ID: " + id + " does not exist!");
        }

        return ResponseEntity.ok(organisationMember);
    }

    @DeleteMapping("/organisation-members")
    public ResponseEntity<List<OrganisationMember>> deleteMultipleMembers(@RequestBody List<OrganisationMember> members) {

        if (members.size() < 1) {
            throw new NotFoundException("No members were given as a request body");
        }

        for (OrganisationMember member : members) {
            repository.deleteById(member.getId());
        }
        return ResponseEntity.ok(members);
    }

}
