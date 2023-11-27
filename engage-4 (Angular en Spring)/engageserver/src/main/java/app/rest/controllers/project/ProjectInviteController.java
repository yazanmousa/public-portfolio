package app.rest.controllers.project;

import app.models.project.PendingRequest;
import app.models.project.ProjectInvite;
import app.repositories.Repository;
import app.rest.exceptions.NotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.net.URI;
import java.util.List;

@RestController
public class ProjectInviteController {

    @Autowired
    private Repository<ProjectInvite> inviteRepository;

    @GetMapping("/project-invites")
    public List<ProjectInvite> findAll(){
        return inviteRepository.findAll();
    }

    @GetMapping("/project-invites/{id}")
    public ProjectInvite findById(@PathVariable long id){
        ProjectInvite projectInvite = inviteRepository.findById(id);
        if(projectInvite == null){
            throw new NotFoundException("No invite with id: " + id + " exists");
        }
        return projectInvite;
    }

    @PostMapping("/project-invites")
    public ResponseEntity<ProjectInvite> addInvite(@RequestBody ProjectInvite projectInvite) {

        int previousInvitesLength = inviteRepository.findAll().size();
        ProjectInvite savedInvite = inviteRepository.save(projectInvite);
        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(projectInvite.getId()).toUri();

        if (inviteRepository.findAll().size() > previousInvitesLength) {
            return ResponseEntity.created(location).body(savedInvite);
        } else {
            return ResponseEntity.ok(savedInvite);
        }

    }

    @DeleteMapping("/project-invites/{id}")
    public ResponseEntity<ProjectInvite> deleteInvite(@PathVariable long id){
        ProjectInvite projectInvite = inviteRepository.findById(id);

        inviteRepository.deleteById(id);

        if(projectInvite == null){
            throw new NotFoundException("Invite with ID: " + id + " does not exist!");
        }

        return ResponseEntity.ok(projectInvite);
    }

    @DeleteMapping("/project-invites")
    public ResponseEntity<ProjectInvite[]> deleteMultipleInvites(@RequestBody ProjectInvite[] invites) {

        if (invites.length < 1) {
            throw new NotFoundException("No invites were given as a request body");
        }

        for (ProjectInvite invite : invites) {
            inviteRepository.deleteById(invite.getId());
        }
        return ResponseEntity.ok(invites);
    }

}
