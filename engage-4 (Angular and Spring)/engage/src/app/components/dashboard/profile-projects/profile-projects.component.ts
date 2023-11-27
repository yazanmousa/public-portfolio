import { Component, OnInit } from '@angular/core';
import {Project} from '../../../models/project/project';
import {ProjectsService} from '../../../services/project/projects.service';
import {UserService} from '../../../services/user/user.service';
import {Router} from '@angular/router';
import {User} from '../../../models/user/user.model';
import {ProjectMemberService} from '../../../services/project/project-member.service';

@Component({
  selector: 'app-profile-projects',
  templateUrl: './profile-projects.component.html',
  styleUrls: ['./profile-projects.component.css']
})
export class ProfileProjectsComponent implements OnInit {
  projects: Project[];
  loggedInUser: User;
   projectHasPhoto: boolean;

  constructor(
    public projectsService: ProjectsService,
    private userService: UserService,
    private projectMemberService: ProjectMemberService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.projects = this.projectsService.findAllForUser(this.userService.loggedInUser.id);
    this.loggedInUser = this.userService.loggedInUser;

    this.projectsService.projectsChanged.subscribe(() => {
      this.projects = this.projectsService.findAllForUser(this.userService.loggedInUser.id);
    })

    this.userService.userChanged.subscribe(() => {
      this.loggedInUser = this.userService.loggedInUser;
    })


  }

  getCorrectPath(project: Project) {
    return "assets/images/" + project.imageSource.split("\\")[2];
  }

  hasFakePath(project: Project): boolean {

    if (project.imageSource === null) {
      return false;
    }

    const pathArray = project.imageSource.split("\\");
    return pathArray[0] === 'C:';
  }

  onClickToProject(id: number) {
    this.router.navigate(['/profile/my-project', id]);
  }

  getProjectRoleForUser(userId: number, projectId: number): string {
    let role = '';
    role = this.projectMemberService.getMemberForUser(userId, projectId).role.toLowerCase();
    return role;
  }

  getOwnerForProject(project: Project): User {
    return this.projectsService.getProjectOwner(project);
  }

  doesProjectHavePhoto(projectId: number): boolean{
    this.projectHasPhoto = this.projectsService.projectHasUploadedPhoto(projectId);
    setTimeout(() => {

    }, 100)

    if (this.projectHasPhoto === true){
      this.projectsService.getImageForProject(projectId);
    }
    return this.projectHasPhoto;
  }
}
