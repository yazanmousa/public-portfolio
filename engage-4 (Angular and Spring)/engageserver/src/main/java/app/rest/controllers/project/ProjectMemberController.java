package app.rest.controllers.project;

import app.models.project.EngagedOrganisation;
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
public class ProjectMemberController {

    @Autowired
    private Repository<ProjectMember> projectMemberRepository;

    @GetMapping("/project-members")
    public List<ProjectMember> findAll() {
        return projectMemberRepository.findAll();
    }

    @GetMapping("project-members/{id}")
    public ProjectMember findById(@PathVariable long id) {
        ProjectMember projectMember = projectMemberRepository.findById(id);

        if (projectMember == null) {
            throw new NotFoundException("No projectMember with id: " + id + " does not exist");
        }
        return projectMember;
    }

    @PostMapping("/project-members")
    public ResponseEntity<ProjectMember> addProject(@RequestBody ProjectMember projectRequest) {
        int previousProjectMembersLenght = projectMemberRepository.findAll().size();
        ProjectMember savedProjectMember = projectMemberRepository.save(projectRequest);
        URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(projectRequest.getId()).toUri();

        if (projectMemberRepository.findAll().size() > previousProjectMembersLenght) {
            return ResponseEntity.created(location).body(savedProjectMember);
        } else {
            return ResponseEntity.ok(savedProjectMember);
        }
    }

    @PutMapping("/project-members/{id}")
    public ResponseEntity<ProjectMember> updateProject(@RequestBody ProjectMember projectMember, @PathVariable long id) {
        if (projectMember.getId() != id) {
            throw new IdDoesNotMatchException("ProjectMember: " + projectMember.getId() + " does not match with paramaterID: " + id);
        }

        ProjectMember savedProjectRequest = projectMemberRepository.save(projectMember);

        return ResponseEntity.ok(savedProjectRequest);

    }

    @DeleteMapping("/project-members/{id}")
    public ResponseEntity<ProjectMember> deleteProject(@PathVariable long id) {
        ProjectMember projectMember = projectMemberRepository.findById(id);

        projectMemberRepository.deleteById(id);

        if (projectMember == null) {
            throw new NotFoundException("ProjectMember with ID: " + id + " does not exist!");
        }

        return ResponseEntity.ok(projectMember);
    }

    @DeleteMapping("/project-members")
    public ResponseEntity<List<ProjectMember>> deleteMultipleProjectMembers(@RequestBody List<ProjectMember> members) {

        if (members.size() < 1) {
            throw new NotFoundException("No project members were given as a request body");
        }

        for (ProjectMember member : members) {
            projectMemberRepository.deleteById(member.getId());
        }
        return ResponseEntity.ok(members);
    }
}
