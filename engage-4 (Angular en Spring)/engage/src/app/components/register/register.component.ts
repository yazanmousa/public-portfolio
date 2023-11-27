import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {UserService} from '../../services/user/user.service';
import {User} from '../../models/user/user.model';
import {CustomValidationService} from '../../services/custom-validation.service';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  errorText: string = "";
  error: boolean = false;
  registerForm: FormGroup;

  constructor(
      private userService: UserService,
      private customValidator: CustomValidationService,
      public router: Router,
      public activatedRoute: ActivatedRoute
  ) {}

  ngOnInit(): void {

    this.registerForm = new FormGroup({
      'firstName': new FormControl(null, [Validators.required]),
      'lastName': new FormControl(null, [Validators.required]),
      'birthDate': new FormControl(null, [Validators.required]),
      'emailAddress': new FormControl(null, [Validators.required]),
      'country': new FormControl(null, [Validators.required]),
      'password': new FormControl(null, [Validators.required,]),
      'passwordRepeat': new FormControl(null, [Validators.required,]),
    })

  }

  onSubmit(): boolean {
    const firstName = this.registerForm.get('firstName').value;
    const lastName = this.registerForm.get('lastName').value;
    const birthDate = this.registerForm.get('birthDate').value;
    const emailAddress = this.registerForm.get('emailAddress').value;
    const password = this.registerForm.get('password').value;
    const passwordRepeat = this.registerForm.get('passwordRepeat').value;
    const country = this.registerForm.get('country').value;

    if (password.length < 8) {
      alert("Your password should contain at least 8 characters");
      return;
    }

    if (this.emailAlreadyExists(emailAddress)) {
      alert("This email has been used before!");
      return;
    }

    if (password.length < 8) {
      alert("Your password should contain at least 8 characters!");
      return;
    }

    if (password === passwordRepeat) {
      const user = new User(firstName, lastName, emailAddress, password, birthDate, country, '', '');
      this.userService.add(user);
      // long id, String firstName, String lastName, String email, LocalDate birthDate, String password, String country, List<UserAttribute> userAttributes, String description, String imagePath, Organisation organisation
      this.router.navigate(['/home']);
      return true;
    } else {
      this.errorText = "passwords don't match";
      this.error = true;
      return false;
    }
  }

  emailAlreadyExists(email: string): boolean {
    let users = this.userService.findAll();

    for (let i = 0; i < users.length; i++) {
      if (users[i].email === email) {
        return true;
      }
    }
    return false;
  }
}
