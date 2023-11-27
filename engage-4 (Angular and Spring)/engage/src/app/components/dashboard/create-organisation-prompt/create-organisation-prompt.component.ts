import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';

@Component({
  selector: 'app-create-organisation-prompt',
  templateUrl: './create-organisation-prompt.component.html',
  styleUrls: ['./create-organisation-prompt.component.css']
})
export class CreateOrganisationPromptComponent implements OnInit {

  constructor(
    private router: Router,
  ) { }

  ngOnInit(): void {

  }

  onClickCreateOrganisation() {
    this.router.navigate(['profile/create-company']);
  }

  onClickFindOrganisation() {
    this.router.navigate(['profile/search-organisation'])
  }


}
