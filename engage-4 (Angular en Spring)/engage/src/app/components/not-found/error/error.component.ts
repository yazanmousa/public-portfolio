import {Component, OnInit} from '@angular/core';
import {Data} from "popper.js";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-error',
  templateUrl: './error.component.html',
  styleUrls: ['./error.component.css']
})
export class ErrorComponent implements OnInit {
  errorMessage: string

  constructor(private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.route.data.subscribe((
      (data: Data) => {
        this.errorMessage = data['message'];
      }
    ))
  }

}
