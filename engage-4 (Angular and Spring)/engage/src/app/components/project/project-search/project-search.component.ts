import {Component, OnInit} from '@angular/core';
import {ProjectsService} from '../../../services/project/projects.service';
import {Project} from '../../../models/project/project';
import {Router} from '@angular/router';
import {User} from '../../../models/user/user.model';
import {UserService} from '../../../services/user/user.service';
import {OrganisationMemberService} from '../../../services/organisation/organisation-member.service';
import {ProjectMemberService} from '../../../services/project/project-member.service';

@Component({
  selector: 'app-project-search',
  templateUrl: './project-search.component.html',
  styleUrls: ['./project-search.component.css']
})
export class ProjectSearchComponent implements OnInit {
  projects: Project[];
  searchText = '';
  view: boolean;
  loggedInUser: User;

  constructor(
    private projectService: ProjectsService,
    private router: Router,
    private userService: UserService,
    private organisationMemberService: OrganisationMemberService,
    private projectMemberService: ProjectMemberService,
  ) {
  }

  ngOnInit(): void {
    this.view = true;
    this.projects = this.projectService.findAll();
    this.loggedInUser = this.userService.loggedInUser;
  }

  onClickToProject(id) {
    this.router.navigate(['project-information', id])
  }

  onClickToInvite(id) {
    this.router.navigate(['project-invite', id])
  }

  getCorrectPath(project: Project) {
    return "assets/images/" + project.imageSource.split("\\")[2];
  }

  switchView(): void{
    this.view = this.view != true;
  }

  hasFakePath(project: Project): boolean {
    const pathArray = project.imageSource.split("\\");
    return pathArray[0] === 'C:';
  }

  userIsAlreadyPartOfOrganisation(): boolean {
    let members = this.organisationMemberService.findAll();

    for (let i = 0; i < members.length; i++) {
      if (members[i].user.id === this.loggedInUser.id) {
        return true;
      }
    }
    return false;
  }

  getMemberCountForProject(projectId: number): number {
    return this.projectMemberService.getAllForProject(projectId).length;
  }


}
