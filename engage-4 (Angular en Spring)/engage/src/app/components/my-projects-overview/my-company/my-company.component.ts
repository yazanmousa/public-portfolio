import {Component, Input, OnInit, Output} from '@angular/core';
import {Organisation} from '../../../models/organisation/organisation';
import {ActivatedRoute, Router} from '@angular/router';
import {OrganisationService} from '../../../services/organisation/organisation.service';
import {UserService} from '../../../services/user/user.service';

@Component({
  selector: 'app-my-company',
  templateUrl: './my-company.component.html',
  styleUrls: ['./my-company.component.css']
})
export class MyCompanyComponent implements OnInit {
  organisations: Organisation[];
  selectedOrganisation: Organisation = null; 
  hasMultipleOrganisations = false;
  loggedInUser = null;


  constructor(
    private organisationService: OrganisationService,
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService
  ) {
  }

  ngOnInit(): void {
    this.organisations = this.organisationService.organisations;
    this.loggedInUser = this.userService.loggedInUser;
    this.hasMoreCompanies();
    this.organisationService.organisationsChanged.subscribe(
      () => {
        this.organisations = this.organisationService.findAll();
        this.hasMoreCompanies();
      }
    )
  }

  hasMoreCompanies() {
    if (this.organisationService.findAll().length > 1) {
      this.hasMultipleOrganisations = true;
    } else this.hasMultipleOrganisations = false;
  }

  onSelect(id: number) {
    this.router.navigate(['company-information', id])
  }

  getSelectedProject() {
    return this.selectedOrganisation;
  }

  cancel() {
    this.selectedOrganisation = null;
  }
}
