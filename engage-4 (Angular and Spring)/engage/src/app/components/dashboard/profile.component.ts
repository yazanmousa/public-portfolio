import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {UserService} from '../../services/user/user.service';
import {User} from '../../models/user/user.model';
import {ProjectInviteService} from '../../services/project/project-invite-service';
import {UserUpdatesService} from '../../services/user/user-updates.service';
import {OrganisationMemberService} from '../../services/organisation/organisation-member.service';
import {OrganisationRequestService} from '../../services/organisation/organisation-request.service';
import {OrganisationMember} from '../../models/organisation/organisation-member';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  loggedInUser: User;
  organisationMember: OrganisationMember;
  amountOfUpdates: number = 0;
  amountOfOrganisationRequests: number = 0;
  amountOfInvites: number = 0;

  constructor(
    public router: Router,
    private route: ActivatedRoute,
    private userService: UserService,
    private userUpdatesService: UserUpdatesService,
    private organisationMemberService: OrganisationMemberService,
    private organisationRequestService: OrganisationRequestService,
    private projectInviteService: ProjectInviteService
    ) {}

  ngOnInit() {
    this.loggedInUser = this.userService.loggedInUser;

    for (let i = 0; i < this.organisationMemberService.findAll().length; i++) {
      console.log(this.organisationMemberService.findAll()[i]);
    }

    this.organisationMember = this.organisationMemberService.getMemberForUser(this.loggedInUser.id);
    this.amountOfUpdates = this.userUpdatesService.getAllForUser(this.loggedInUser.id).length;
    this.amountOfInvites = this.projectInviteService.findInvitesFor(this.loggedInUser.id).length;

    if (this.organisationMemberService.getMemberForUser(this.loggedInUser.id) !== null) {
      let organisationMember = this.organisationMemberService.getMemberForUser(this.loggedInUser.id);
      this.amountOfOrganisationRequests = this.organisationRequestService.getAllForOrganisation(organisationMember.organisation.id).length;
    }


    // Making sure all amounts are updated correctly when certain events are fired.
    this.userService.userChanged.subscribe(() => {
      this.loggedInUser = this.userService.loggedInUser;
    })

    this.userUpdatesService.updatesChanged.subscribe(() => {
      this.amountOfUpdates = this.userUpdatesService.getAllForUser(this.loggedInUser.id).length;
    })

    this.organisationMemberService.membersChanged.subscribe(() => {
      this.organisationMember = this.organisationMemberService.getMemberForUser(this.loggedInUser.id);
    })

    this.organisationRequestService.requestsChanged.subscribe(() => {
      let organisationMember = this.organisationMemberService.getMemberForUser(this.loggedInUser.id);

      if (organisationMember !== null) {
        this.amountOfOrganisationRequests = this.organisationRequestService.getAllForOrganisation(organisationMember.organisation.id).length;
      }
    })

    this.projectInviteService.pendingInvitesChanged.subscribe(() => {
      this.amountOfInvites = this.projectInviteService.findInvitesFor(this.loggedInUser.id).length;
    })

  }

  hasOrganisation(): boolean {
    return this.organisationMemberService.getMemberForUser(this.loggedInUser.id) !== null;
  }

}
