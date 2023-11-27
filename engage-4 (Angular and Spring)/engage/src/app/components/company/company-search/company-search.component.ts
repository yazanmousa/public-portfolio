import { Component, OnInit } from '@angular/core';
import {Organisation} from '../../../models/organisation/organisation';
import {OrganisationService} from '../../../services/organisation/organisation.service';
import {ProjectsService} from '../../../services/project/projects.service';
import {ActivatedRoute, Router} from '@angular/router';


@Component({
  selector: 'app-company-search',
  templateUrl: './company-search.component.html',
  styleUrls: ['./company-search.component.css']
})
export class CompanySearchComponent implements OnInit {
  companies: Organisation[];
  searchText = '';
  view: boolean;

  constructor(private organisationService: OrganisationService,
              private projectsService: ProjectsService,
              private route: ActivatedRoute,
              private router: Router) {
  }

  ngOnInit(): void {
    this.companies = this.organisationService.findAll();

    this.organisationService.organisationsChanged.subscribe(() => {
      this.companies = this.organisationService.findAll();
      }
    )
    this.view = true;
  }

  onClickToProject(id) {
    this.router.navigate(['company-information', id])
  }

  switchView(): void{
    this.view = this.view != true;
  }

  getCorrectPath(path: string, organisation: Organisation) {
    for (let i = 0; i < this.companies.length; i++) {
      if (this.companies[i] === organisation) {
        path = "assets/images/" + this.companies[i].imagePath.split("\\")[2];
        return path;
      }
    }

  }

  isFakePath(path: string): boolean {
    const pathArray = path.split("\\");
    if (pathArray[0] === 'C:') {
      return true;
    }
    return false;
  }
}
