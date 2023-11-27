import { Component, OnInit } from '@angular/core';
import {UserUpdate} from '../../../models/user/user-update';
import {UserService} from '../../../services/user/user.service';
import {User} from '../../../models/user/user.model';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {Router} from '@angular/router';
import {UserUpdatesService} from '../../../services/user/user-updates.service';

@Component({
  selector: 'app-latest-updates',
  templateUrl: './latest-updates.component.html',
  styleUrls: ['./latest-updates.component.css'],
  animations: [
    trigger('deleteUpdate', [
      state('in', style({opacity: 0.5, transform: 'translateX(0)'})),
      transition('* => void', [
        animate(400, style({opacity: 0, transform: 'translateX(200px)'}))
      ])
    ])
  ]
})
export class LatestUpdatesComponent implements OnInit {
  userUpdates: UserUpdate[] = [];
  loggedInUser: User;

  constructor(
    private userService: UserService,
    private router: Router,
    private userUpdatesService: UserUpdatesService
  ) {}

  ngOnInit(): void {
    this.loggedInUser = this.userService.loggedInUser;
    this.userUpdates = this.userUpdatesService.getAllForUser(this.loggedInUser.id);

    this.userUpdatesService.updatesChanged.subscribe(() => {
      this.userUpdates = this.userUpdatesService.getAllForUser(this.loggedInUser.id);
    })
  }

  onDeleteUpdate(userUpdate: UserUpdate) {
    this.userUpdatesService.deleteById(userUpdate.id);
  }

  onClickClearAll() {
    if (this.userUpdates.length >= 1) {
      this.userUpdatesService.deleteMultipleUpdates(this.userUpdates);
      this.userUpdates = [];
    }
  }
}
