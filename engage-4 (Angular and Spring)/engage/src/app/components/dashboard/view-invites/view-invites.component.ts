import {Component, OnInit} from '@angular/core';
import {UserService} from "../../../services/user/user.service";
import {ActivatedRoute, Router} from "@angular/router";
import {ProjectInvite} from "../../../models/project/project-invite";
import {ProjectMember} from "../../../models/project/project-member";
import {Project} from "../../../models/project/project";
import {ProjectsService} from "../../../services/project/projects.service";
import {ProjectRolesEnum} from '../../../models/project/project-roles-enum';
import {ProjectInviteService} from '../../../services/project/project-invite-service';
import {ProjectMemberService} from '../../../services/project/project-member.service';

@Component({
  selector: 'app-view-invites',
  templateUrl: './view-invites.component.html',
  styleUrls: ['./view-invites.component.css']
})
export class ViewInvitesComponent implements OnInit {
  invites: ProjectInvite[];
  loggedInUser;
  project: Project;
  constructor(private userService: UserService,
              private projectInviteService: ProjectInviteService,
              private projectMemberService: ProjectMemberService,
              private projectService: ProjectsService,
              private route: ActivatedRoute,
              private router: Router) { }

  ngOnInit(): void {
    this.loggedInUser = this.userService.loggedInUser;
    this.invites = this.projectInviteService.findInvitesFor(this.loggedInUser.id);
    console.log(this.invites);
  }

  onClickToProject(id) {
    this.router.navigate(['project-information', id])
  }

  onSelect(id: number) {
    this.router.navigate(['project-information', id]);
  }

  getMemberFirstName(member: ProjectMember): string {
    return this.userService.findUserById(member.user.id).firstName
  }

  onAccept(invite: ProjectInvite): void{
    console.log("invite id: " + invite.id);
    let check = this.loggedInUser.organisationMember !== null;
    if(!check){
      alert("You must first join an organisation before you can accept invites for projects");
      return;
    }else{
      let project  = this.projectService.findById(invite.project.id);
      let projectMember = new ProjectMember(project, invite.receivedByUser, false, ProjectRolesEnum.Project_Staff);
      this.projectMemberService.save(projectMember);
      this.projectInviteService.deleteProjectInvite(invite.id);
      this.invites.splice(this.invites.indexOf(invite), 1);
    }
  }

  getCorrectPath(id: number) {
    let x = this.projectService.findById(id);
    return "assets/images/" + x.imageSource.split("\\")[2];
  }

  hasFakePath(id: number): boolean {
    let x = this.projectService.findById(id)
    const pathArray = x.imageSource.split("\\");
    return pathArray[0] === 'C:';

  }

  onDecline(invite: ProjectInvite): void {
    this.projectInviteService.deleteProjectInvite(invite.id);
    this.invites.splice(this.invites.indexOf(invite), 1)
  }

  onDeny(invite: ProjectInvite): void{
    if(!this.invites.length){
      alert("You have no invites to deny");
    }else{
      alert("You have denied the invite for " + invite.project.id);
      this.projectInviteService.deleteProjectInvite(invite.id);
    }
  }

  getPhoto(path: string): string {
    if (path === null) {
      return;
    }
    let pathArray = path.split("\\");
    if (pathArray[0] === 'C:') {
      return "assets/images/" + path.split("\\")[2];
    } else {
      return path;
    }
  }

  getProjectDate(projectInvite: ProjectInvite): Date {
    return this.projectService.findById(projectInvite.project.id).dateCreated;
  }

  getProjectName(invite: ProjectInvite): string{
    return this.projectService.findById(invite.project.id).name;
  }

}
