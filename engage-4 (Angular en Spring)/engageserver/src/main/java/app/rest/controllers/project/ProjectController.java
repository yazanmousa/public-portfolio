package app.rest.controllers.project;

import app.models.project.Project;
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
public class ProjectController {

  @Autowired
  private Repository<Project> projectRepository;

  @GetMapping("/projects")
  public List<Project> findAll() {
    return projectRepository.findAll();
  }

  @GetMapping("projects/{id}")
  public Project findById(@PathVariable long id) {
    Project project = projectRepository.findById(id);

    if (project == null) {
      throw new NotFoundException("No project with id: " + id + " does not exist");
    }
    return project;
  }

  @PostMapping("/projects")
  public ResponseEntity<Project> addProject(@RequestBody Project project) {
    int previousOrganisationsLength = projectRepository.findAll().size();
    Project savedProject = projectRepository.save(project);
    URI location = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(project.getId()).toUri();

    if (projectRepository.findAll().size() > previousOrganisationsLength) {
      return ResponseEntity.created(location).body(savedProject);
    } else {
      return ResponseEntity.ok(savedProject);
    }
  }

  @PutMapping("/projects/{id}")
  public ResponseEntity<Project> updateProject(@RequestBody Project project, @PathVariable long id) {
    if (project.getId() != id) {
      throw new IdDoesNotMatchException("Project: " + project.getId() + " does not match with paramaterID: " + id);
    }

    Project savedProject = projectRepository.save(project);

    return ResponseEntity.ok(savedProject);

  }

  @DeleteMapping("/projects/{id}")
  public ResponseEntity<Project> deleteProject(@PathVariable long id) {
    Project project = projectRepository.findById(id);

    projectRepository.deleteById(id);

    if (project == null) {
      throw new NotFoundException("Project with ID: " + id + " does not exist!");
    }

    return ResponseEntity.ok(project);
  }

}
