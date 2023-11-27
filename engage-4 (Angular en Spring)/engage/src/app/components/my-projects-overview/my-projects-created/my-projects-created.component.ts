import {Component, Input, OnInit, Output} from '@angular/core';
import {ProjectsService} from '../../../services/project/projects.service';
import {Project} from '../../../models/project/project';
import {ActivatedRoute, Router} from '@angular/router';
import {UserService} from '../../../services/user/user.service';

@Component({
  selector: 'app-my-projects-created',
  templateUrl: './my-projects-created.component.html',
  styleUrls: ['./my-projects-created.component.css']
})
export class MyProjectsCreatedComponent implements OnInit {
  projects: Project[];
  hasMultipleProjects = false;
  loggedInUser = null;


  constructor(
    private projectsService: ProjectsService,
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService
  ) {
  }

  ngOnInit(): void {
    this.projects = this.projectsService.projects;
    this.loggedInUser = this.userService.loggedInUser;
    this.hasMoreProjects();
    this.projectsService.projectsChanged.subscribe(
      () => {
        this.projects = this.projectsService.findAll();
        this.hasMoreProjects();
      }
    )
  }

  onSelect(id: number) {
    this.router.navigate(['project-information', id])
  }

  hasMoreProjects() {
    if (this.projectsService.findAll().length > 1) {
      return this.hasMultipleProjects = true;
    } else this.hasMultipleProjects = false;
  }

}
