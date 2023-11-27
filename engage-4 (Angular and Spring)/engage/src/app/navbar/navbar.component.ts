import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {UserService} from '../services/user/user.service';
import {FormControl, FormGroup, Validators} from '@angular/forms';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  loginForm: FormGroup;
  loggedInUser = null;
  error = false;
  errorMessage = 'This user does not exist!';

  constructor(
    private router: Router,
    private userService: UserService
  ) {
  }

  ngOnInit(): void {
    this.loginForm = new FormGroup({
      'email': new FormControl(null, [Validators.email, Validators.required]),
      'password': new FormControl(null, [Validators.required])
    })

    this.userService.userChanged.subscribe(() => {
      this.loggedInUser = this.userService.loggedInUser;
    })

  }

  toRegister() {
    this.router.navigate(['/register'])

  }

  onSubmit(): boolean {

    // getting email and password from the form
    const email = this.loginForm.get('email').value;
    const password = this.loginForm.get('password').value;


    if (this.userService.getByEmailAndPassword(email, password) === null) {
      this.error = true;
      alert(this.errorMessage)


      return false;
    }

    // getting the user to be logged in from the service
    const userToLogin = this.userService.getByEmailAndPassword(email, password);

    // set the loggedInUser in the service to the right user.
    this.userService.loginUser(userToLogin);

    this.loggedInUser = userToLogin;

    this.userService.userChanged.emit();

    this.router.navigate(['/profile']);
  }

  onClickLogout() {
    this.userService.signOutUser();
    this.loggedInUser = this.userService.loggedInUser;
    this.userService.userChanged.emit();
    this.router.navigate(["/home"])
  }

}
