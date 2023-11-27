import {Component, OnInit} from '@angular/core';
import {UserService} from '../../../services/user/user.service';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {User} from '../../../models/user/user.model';
import {ProjectsService} from '../../../services/project/projects.service';
import {Project} from '../../../models/project/project';
import {ProjectInviteService} from '../../../services/project/project-invite-service';
import {ProjectMember} from "../../../models/project/project-member";
import {UserUpdate} from '../../../models/user/user-update';
import {ProjectRolesEnum} from '../../../models/project/project-roles-enum';
import {PendingRequest} from '../../../models/project/pending-request';
import {ProjectMemberService} from '../../../services/project/project-member.service';
import {ProjectRequestsService} from '../../../services/project/project-requests.service';
import {OrganisationMemberService} from '../../../services/organisation/organisation-member.service';
import {UserUpdatesService} from '../../../services/user/user-updates.service';
import {EngagedOrganisationsService} from '../../../services/project/engaged-organisations.service';

@Component({
  selector: 'app-project-information',
  templateUrl: './project-information.component.html',
  styleUrls: ['./project-information.component.css']
})
export class ProjectInformationComponent implements OnInit {
  project: Project;
  projectMembers: ProjectMember[] = [];
  projectOwner: User;
  loggedInUser: User = null;
  projectId: number;
  pendingRequests: PendingRequest[] = [];
  leaveLoading: boolean = false;

  projectHasPhoto: boolean;

  constructor(
    private inviteRequestService: ProjectInviteService,
    private userService: UserService,
    public projectsService: ProjectsService,
    private projectMemberService: ProjectMemberService,
    private projectRequestsService: ProjectRequestsService,
    private organisationMemberService: OrganisationMemberService,
    private userUpdatesService: UserUpdatesService,
    private engagedOrganisationService: EngagedOrganisationsService,
    private route: ActivatedRoute,
    private router: Router,
  ) {
  }

  ngOnInit(): void {
    this.loggedInUser = this.userService.loggedInUser;
    this.route.params.subscribe(
      (params: Params) => {
        this.projectId = +params['id'];
        this.project = this.projectsService.findById(this.projectId);
        this.projectMembers = this.projectMemberService.getAllForProject(this.projectId);
      }
    );
    this.projectOwner = this.projectsService.getProjectOwner(this.project);
    this.pendingRequests = this.projectRequestsService.getAllForProject(this.projectId);

    this.projectsService.projectsChanged.subscribe(
      () => {
        this.project = this.projectsService.findById(this.projectId);
        this.projectOwner = this.projectsService.getProjectOwner(this.project);
      }
    )

    this.projectMemberService.membersChanged.subscribe(() => {
      this.projectMembers = this.projectMemberService.getAllForProject(this.projectId);
    })

    this.projectRequestsService.pendingRequestsChanged.subscribe(() => {
      this.pendingRequests = this.projectRequestsService.getAllForProject(this.projectId);
    })

    this.userService.userChanged.subscribe(
      () => {
        for (let i = 0; i < this.pendingRequests.length; i++) {
          this.pendingRequests[i].sendByUser = this.userService.findUserById(this.pendingRequests[i].sendByUser.id);
          this.projectOwner = this.projectsService.getProjectOwner(this.project);
        }
      }
    )

    this.projectHasPhoto = this.projectsService.projectHasUploadedPhoto(this.projectId);
    if (this.projectHasPhoto === true){
      this.projectsService.getImageForProject(this.projectId);
    }

  }

  getCorrectPath(path: string) {
    path = "assets/images/" + this.project.imageSource.split("\\")[2];
    return path;
  }

  isFakePath(path: string): boolean {

    if (this.project.imageSource === null) {
      return false;
    }

    const pathArray = this.project.imageSource.split("\\");
    if (pathArray[0] === 'C:') {
      return true;
    }
    return false;
  }

  onClickEditProject(id: number) {
    this.router.navigate(['/profile/update-project', id]);
  }

  onClickInvite(id: number) {
    this.router.navigate(['/profile/project-invite/', id]);
  }

  onSelectProjectMember(member: ProjectMember) {
    if (this.loggedInUser.id === member.user.id) {
      this.router.navigate(['profile/my-information', member.user.id]);
    } else {
      this.router.navigate(['profile-information', member.user.id]);
    }
  }

  onClickJoinProject() {
    let pendingRequest = new PendingRequest(this.loggedInUser, this.project);
    this.projectRequestsService.save(pendingRequest);
    alert('Request has been sent!')
  }

  userAlreadySentRequest(): boolean {
    for (let i = 0; i < this.pendingRequests.length; i++) {
      if (this.pendingRequests[i].sendByUser.id === this.loggedInUser.id ) {
        return true;
      }
    }
    return false;
  }

  userIsPartOfProject(): boolean {
    for (let i = 0; i < this.projectMembers.length; i++) {
      if (this.projectMembers[i].user.id === this.loggedInUser.id) {
        return true;
      }
    }
    return false;
  }

  userHasOrganisation(): boolean {
    return this.organisationMemberService.getMemberForUser(this.loggedInUser.id) !== null;
  }

  getPhoto(path: string): string {
    let pathArray = path.split("\\");

    if (pathArray[0] === 'C:') {
      return "assets/images/" + path.split("\\")[2];
    } else {
      return path;
    }
  }

  onAcceptPendingRequest(pendingRequest: PendingRequest) {
    let projectMember = new ProjectMember(this.project, pendingRequest.sendByUser, false, ProjectRolesEnum.Project_Staff);
    this.projectMemberService.save(projectMember);
    let userUpdate = new UserUpdate(pendingRequest.sendByUser, 'Your request to join project ' + '"' + this.project.name + '"' + ' has been accepted', Date.now());
    this.userUpdatesService.save(userUpdate);
    this.projectRequestsService.deleteById(pendingRequest.id);
  }

  onDeclinePendingRequest(pendingRequest: PendingRequest) {
    this.projectRequestsService.deleteById(pendingRequest.id);
  }

  isProjectManager(user: User): boolean {
    for (let i = 0; i < this.projectMembers.length; i++) {
      if (this.projectMembers[i].user.id === user.id) {
        return this.projectMembers[i].role === 'PROJECT_MANAGER';
      }
    }
  }

  leaveProject() {
    this.leaveLoading = true;

    const member = this.projectMemberService.getMemberForUser(this.loggedInUser.id, this.projectId);
    this.projectMemberService.deleteById(member.id);
    let userUpdate = new UserUpdate(this.loggedInUser, "You have left project: " + this.project.name, Date.now());
    this.userUpdatesService.save(userUpdate);

    setTimeout(() => {
      this.leaveLoading = false;
      this.router.navigate(['/profile/my-projects/', this.loggedInUser.id]);
    }, 1000)

  }

  isOwner(): boolean {
    if (this.projectMembers.length < 1) {
      return false;
    } else {
      for (let i = 0; i < this.projectMembers.length; i++) {
        if (this.loggedInUser.id === this.projectMembers[i].user.id) {
          return this.projectMembers[i].owner === true;
        }
      }
      return false;
    }
  }
  ngOnDestroy() {
    this.projectsService.projectHasPhoto = false;
    this.projectsService.retrievedImage = null;
  }

  getEngagedOrganisationCount(projectId: number): number {
    return this.engagedOrganisationService.getAllForProject(projectId).length;
  }
}
