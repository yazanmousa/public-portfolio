import {Component, OnInit} from '@angular/core';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {UserService} from '../../services/user/user.service';
import {User} from '../../models/user/user.model';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.css'],
  animations: [
    trigger('enlargeItem', [
      state('normal', style({transform: 'scale(1)'})),
      state('large', style({transform: 'scale(1.1)'})),
      transition('normal => large', animate(200)),
      transition('large => normal', animate(200))
    ]),
    trigger('showContent', [
      state('in', style({opacity: 1, transform: 'translateY(0)'})),
      transition('void => *', [
        style({opacity: 0, transform: 'translateY(-100px)'}), animate(600)
      ]),
      transition('* => void', [
        style({opacity: 0, transform: 'translateY(100px)'}), animate(600)
      ]),
    ])
  ]
})
export class AboutComponent implements OnInit {
  state = 'normal';
  loggedInUser: User = null;

  constructor(
    private userService: UserService,
  ) {}

  ngOnInit(): void {
    this.loggedInUser = this.userService.loggedInUser;

    this.userService.userChanged.subscribe(
      () => {
        this.loggedInUser = this.userService.loggedInUser;
      }
    )
  }

  onHoverRegister() {
    this.state === 'normal' ? this.state = 'large' : this.state = 'normal';
  }

}
