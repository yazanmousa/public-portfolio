import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {UserService} from './services/user/user.service';
import {ProjectsService} from './services/project/projects.service';
import {OrganisationService} from './services/organisation/organisation.service';
import {UserAttributesService} from './services/user/user-attributes.service';
import {UserReviewsService} from './services/user/user-reviews.service';
import {UserUpdatesService} from './services/user/user-updates.service';
import {EngagedOrganisationsService} from './services/project/engaged-organisations.service';
import {ProjectMemberService} from './services/project/project-member.service';
import {ProjectRequestsService} from './services/project/project-requests.service';
import {OrganisationMemberService} from './services/organisation/organisation-member.service';
import {OrganisationRequestService} from './services/organisation/organisation-request.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'engage';
  loggedInUser = null;

  constructor(
    private router: Router,
    private userService: UserService,
    private userAttributesService: UserAttributesService,
    private userReviewsService: UserReviewsService,
    private userUpdatesService: UserUpdatesService,
    private projectsService: ProjectsService,
    private engagedOrganisationsService: EngagedOrganisationsService,
    private projectMemberService: ProjectMemberService,
    private projectRequestsService: ProjectRequestsService,
    private organisationService: OrganisationService,
    private organisationMemberService: OrganisationMemberService,
    private organisationRequestService: OrganisationRequestService,
    private route: ActivatedRoute,
  ) {
  }

  ngOnInit() {
    this.router.navigate(["/home"]);

    this.userService.userChanged.subscribe(
      () => {
        this.loggedInUser = this.userService.loggedInUser;
      }
    )

  }

}
