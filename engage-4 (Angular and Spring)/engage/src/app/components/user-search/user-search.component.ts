import {Component, OnInit} from '@angular/core';
import {User} from '../../models/user/user.model';
import {OrganisationService} from '../../services/organisation/organisation.service';
import {ActivatedRoute, Router} from '@angular/router';
import {UserService} from '../../services/user/user.service';
import {UserPipePipe} from '../../pipes/user-pipe.pipe';
import {Project} from '../../models/project/project';
import {OrganisationMemberService} from '../../services/organisation/organisation-member.service';

@Component({
  selector: 'app-user-search',
  templateUrl: './user-search.component.html',
  styleUrls: ['./user-search.component.css']
})
export class UserSearchComponent implements OnInit {
  users: User[];
  usersView: User[] = [];
  loggedInUser;
  searchText = '';
  view: boolean;

  constructor(private organisationService: OrganisationService,
              private organisationMemberService: OrganisationMemberService,
              private userService: UserService,
              private route: ActivatedRoute,
              private router: Router) {
  }

  ngOnInit(): void {
    this.loggedInUser = this.userService.loggedInUser;
    this.users = this.userService.findAll();
    this.checkOrganisation();
    this.users = this.usersView;
    this.view = true;
  }

  onSelectUser(id: number, x: User) {
    this.router.navigate(['profile-information', id]);
  }


  onClickToUser(id: number) {
    this.router.navigate(['profile-information', id]);
  }


  getCorrectPath(path: String, user: User) {
    return 'assets/images/' + this.userService.findUserById(user.id).imagePath.split('\\')[2];
  }


  isFakePath(string: String, user: User): boolean {
    const pathArray = user.imagePath.split('\\');
    return pathArray[0] === 'C:';
  }

  switchView(): void {
    this.view = this.view != true;
  }

  userIsPartOfOrganisation(user: User): boolean {
    let members = this.organisationMemberService.findAll();

    for (let i = 0; i < members.length; i++) {
      if (members[i].user.id === user.id) {
        return true;
      }
    }
    return false;
  }

  //Checks if user has an origanistion
  checkOrganisation() {
    this.users.forEach((user) => {
      if (this.userIsPartOfOrganisation(user)) {
        this.usersView.push(user);
      }

      if (user.id === this.loggedInUser.id) {
        this.usersView.splice(this.usersView.indexOf(user), 1);
      }
    });

    //Remove project owner
    this.users.splice(this.users.indexOf(this.loggedInUser), 1);
  }

}
