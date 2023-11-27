import {Component, OnInit} from '@angular/core';
import {User} from "../../../models/user/user.model";
import {UserService} from "../../../services/user/user.service";
import {ActivatedRoute, Params, Router} from '@angular/router';
import {Organisation} from '../../../models/organisation/organisation';
import {OrganisationService} from '../../../services/organisation/organisation.service';
import {PendingOrganisationRequest} from '../../../models/organisation/pending-organisation-request';
import {ProjectInviteService} from '../../../services/project/project-invite-service';
import {OrganisationMember} from '../../../models/organisation/organisation-member';
import {UserUpdate} from '../../../models/user/user-update';
import {OrganisationRequestService} from '../../../services/organisation/organisation-request.service';
import {OrganisationMemberService} from '../../../services/organisation/organisation-member.service';
import {UserUpdatesService} from '../../../services/user/user-updates.service';

@Component({
  selector: 'app-company-information',
  templateUrl: './company-information.component.html',
  styleUrls: ['./company-information.component.css']
})
export class CompanyInformationComponent implements OnInit {
  organisationId: number = 0;
  organisation: Organisation = null;
  members: OrganisationMember[] = [];
  loggedInUser: User = null;
  pendingRequests: PendingOrganisationRequest[] = [];
  organisationOwner: User = null;

  organisationHasPhoto: boolean = false;


  constructor(
    private userService: UserService,
    private route: ActivatedRoute,
    private router: Router,
    public organisationService: OrganisationService,
    private organisationRequestService: OrganisationRequestService,
    private organisationMemberService: OrganisationMemberService,
    private userUpdatesService: UserUpdatesService
  ) {}

  ngOnInit(): void {
    this.loggedInUser = this.userService.loggedInUser;
    this.route.params.subscribe(
        (params: Params) => {
          this.organisationId = +params['id'];
          this.organisation = this.organisationService.findById(this.organisationId);
          this.members = this.organisationMemberService.getAllForOrganisation(this.organisationId);
        }
    )

    setTimeout(() => {
      this.pendingRequests = this.organisationRequestService.getAllForOrganisation(this.organisationId);
      this.organisationOwner = this.organisationService.getOwnerForOrganisation(this.organisationId);
    }, 100)


    this.organisationService.organisationsChanged.subscribe(() => {
          this.organisation = this.organisationService.findById(this.organisationId);
          this.pendingRequests = this.organisationRequestService.getAllForOrganisation(this.organisationId);
          this.organisationOwner = this.organisationService.getOwnerForOrganisation(this.organisationId);
        }
    )

    this.organisationMemberService.membersChanged.subscribe(() => {
      this.members = this.organisationMemberService.getAllForOrganisation(this.organisationId);
    })

    this.organisationRequestService.requestsChanged.subscribe(() => {
      this.pendingRequests = this.organisationRequestService.getAllForOrganisation(this.organisationId);
    })

    this.userService.userChanged.subscribe(() => {
      this.loggedInUser = this.userService.loggedInUser;
      this.organisationOwner = this.organisationService.getOwnerForOrganisation(this.organisationId);
    })

    this.organisationHasPhoto = this.organisationService.organisationHasUploadedPhoto(this.organisationId);
    if (this.organisationHasPhoto === true){
      this.organisationService.getImageForOrganisation(this.organisationId);
    }

  }

  getCorrectPath(path: string) {
    path = "assets/images/" + this.organisation.imagePath.split("\\")[2];
    return path;
  }


  isFakePath(): boolean {
    const pathArray = this.organisation.imagePath.split("\\");
    if (pathArray[0] === 'C:') {
      return true;
    }
    return false;
  }

  onClickEditProject(id: number) {
    this.router.navigate(['profile/update-company', id])
  }

  onSelectMember(member: OrganisationMember) {
    this.router.navigate(['profile-information', member.user.id])
  }

  getPhoto(path: string): string {
    if (path === null) {
      return '';
    }

    let pathArray = path.split("\\");

    if (pathArray[0] === 'C:') {
      return "assets/images/" + path.split("\\")[2];
    } else {
      return path;
    }
  }

  userAlreadyHasOrganisation(): boolean {
    return this.organisationMemberService.getMemberForUser(this.loggedInUser.id) !== null;
  }

  userIsPartOfOrganisation(): boolean {
    for (let i = 0; i < this.members.length; i++) {
      if (this.members[i].user.id === this.loggedInUser.id) {
        return true;
      }
    }
    return false;
  }

  userAlreadySentRequest(): boolean {
    for (let i = 0; i < this.pendingRequests.length; i++) {
      if (this.pendingRequests[i].sendByUser.id === this.loggedInUser.id) {
        return true;
      }
    }
    return false;
  }

  onClickJoinOrganisation() {
    let pendingOrganisationRequest = new PendingOrganisationRequest(this.loggedInUser, this.organisation);
    this.organisationRequestService.save(pendingOrganisationRequest);
    alert('Request has been sent!');
  }

  onAcceptPendingRequest(pendingRequest: PendingOrganisationRequest) {

    // adding a new organisation member to the organisation
    let member = new OrganisationMember(pendingRequest.sendByUser, this.organisation, false, false);
    this.organisationMemberService.save(member);

    // Whenever a user is accepted into an organisation, an update will be send to his/her profile under the 'latest updates' tab.
    let userUpdate = new UserUpdate(pendingRequest.sendByUser, 'Your request to join organisation ' + '"' + this.organisation.name + '"' + ' has been accepted', Date.now());
    this.userUpdatesService.save(userUpdate);

    this.organisationRequestService.deleteById(pendingRequest.id);

  }

  onDeclinePendingRequest(pendingRequest: PendingOrganisationRequest) {
    this.organisationRequestService.deleteById(pendingRequest.id);
  }

  isAdministrator(): boolean {
    if (this.members.length < 1) {
      return false;
    } else {
      for (let i = 0; i < this.members.length; i++) {
        if (this.loggedInUser.id === this.members[i].user.id) {
          return this.members[i].administrator === true;
        }
      }
      return false;
    }
  }

  isOwner(): boolean {
    if (this.members.length < 1) {
      return false;
    } else {
      for (let i = 0; i < this.members.length; i++) {
        if (this.loggedInUser.id === this.members[i].user.id) {
          return this.members[i].owner === true;
        }
      }
      return false;
    }
  }

  leaveOrganisation() {
    const member = this.organisationMemberService.getMemberForUser(this.loggedInUser.id);
    this.organisationMemberService.deleteById(member.id);
    let userUpdate = new UserUpdate(this.loggedInUser, "You have left organisation: " + this.organisation.name, Date.now());
    this.userUpdatesService.save(userUpdate);
    this.router.navigate(['/profile/create-organisation-prompt']);
  }
  ngOnDestroy() {
    this.organisationService.organisationHasPhoto = false;
    this.organisationService.retrievedImage = null;
  }
}
