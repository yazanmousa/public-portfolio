import {Component, Input, OnInit} from '@angular/core';
import {Router} from '@angular/router';

@Component({
  selector: 'app-my-projects-overview',
  templateUrl: './my-projects-overview.component.html',
  styleUrls: ['./my-projects-overview.component.css']
})
export class MyProjectsOverviewComponent implements OnInit {
  hasMultipleCompanies: boolean;
  hasMultipleProjects: boolean;

  constructor(private router: Router) {
  }

  ngOnInit(): void {
  }
}
