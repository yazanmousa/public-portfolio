import {Component, OnInit} from '@angular/core';
import {UserService} from "../../../services/user/user.service";
import {ProjectsService} from "../../../services/project/projects.service";
import {ActivatedRoute, Params, Router} from "@angular/router";
import {User} from "../../../models/user/user.model";
import {Project} from "../../../models/project/project";
import {ProjectInviteService} from "../../../services/project/project-invite-service";
import {ProjectInvite} from "../../../models/project/project-invite";
import {OrganisationMemberService} from '../../../services/organisation/organisation-member.service';
import {ProjectMemberService} from '../../../services/project/project-member.service';
import {ProjectMember} from '../../../models/project/project-member';

@Component({
  selector: 'app-project-invite',
  templateUrl: './project-invite.component.html',
  styleUrls: ['./project-invite.component.css']
})
export class ProjectInviteComponent implements OnInit {
  users: User[];
  loggedInUser: User;
  userView: User[] = [];
  project: Project;
  projectMembers: ProjectMember[] = [];
  pendingInvites: ProjectInvite[] = [];
  selectedUser: User;
  searchText: string = '';
  showAlert: boolean;

  constructor(private userService: UserService,
              public projectsService: ProjectsService,
              private projectMemberService: ProjectMemberService,
              private route: ActivatedRoute,
              private inviteService: ProjectInviteService,
              private organisationMemberService: OrganisationMemberService,
              private router: Router) {
  }

  ngOnInit(): void {
    this.loggedInUser = this.userService.loggedInUser;
    this.pendingInvites = this.inviteService.findAll();
    this.users = this.userService.findAll();
    console.log(this.users)

    this.route.params.subscribe(
      (params: Params) => {
        this.project = this.projectsService.findById(+params['id']);
        this.projectMembers = this.projectMemberService.getAllForProject(this.project.id);
      }
    )

    this.userService.userChanged.subscribe(() => {
      this.users = this.userService.findAll();
    })

    this.projectsService.projectsChanged.subscribe(
      () => {
        this.project = this.projectsService.findById(this.project.id);
      }
    )
    this.checkOrganisation();
    this.users = this.userView;
    console.log(this.users)
  }


  onSelectUser(id: number, x: User) {
    this.router.navigate(['profile-information', id]);
    this.selectedUser = x;
  }

  getCorrectPath(path: string) {
    path = "assets/images/" + this.project.imageSource.split("\\")[2];
    return path;
  }

  isFakePath(): boolean {
    const pathArray = this.project.imageSource.split("\\");
    return pathArray[0] === 'C:';
  }

  userIsPartOfOrganisation(user: User): boolean {
    let members = this.organisationMemberService.findAll();

    for (let i = 0; i < members.length; i++) {
      if (members[i].user.id === user.id) {
        return true;
      }
    }
    return false;
  }

  checkOrganisation() {
    this.users.forEach(user => {
      if(this.userIsPartOfOrganisation(user)){
        this.userView.push(user);
      }

      if(user.id === this.loggedInUser.id){
        this.userView.splice(this.userView.indexOf(user), 1);
      }

      this.projectMembers.forEach(member => {
              if (user.id === member.user.id) {
                this.userView.splice(this.userView.indexOf(user, 1));
              }
            })
    })

      this.users.forEach((x) => {
        this.pendingInvites.forEach((z) => {
          if (x.id == z.sendByUser.id) {
            this.userView.splice(this.userView.indexOf(x), 1);
          }
        })
      })
  }

  sendInvite(user: User) {
    this.selectedUser = user;
    let sentBy = this.projectsService.getProjectOwner(this.project);
    let receivedBy = user;
    let project = this.project;

    let date = new Date();
    date.setMonth(date.getMonth() + 1);

    let pendingInvite = new ProjectInvite(sentBy, receivedBy, project, date);
    this.inviteService.save(pendingInvite);
    this.showAlert = true;
    this.users.splice(this.users.indexOf(user), 1);
  }

}

