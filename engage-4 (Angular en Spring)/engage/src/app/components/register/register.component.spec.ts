import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {HttpClientModule} from '@angular/common/http';
import {RegisterComponent} from './register.component';
import {AppRoutingModule} from '../../app-routing.module';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {UserService} from "../../services/user/user.service";
import {User} from "../../models/user/user.model";

describe('RegisterComponent', () => {
  let component: RegisterComponent;
  let componentHtml: HTMLElement;
  let fixture: ComponentFixture<RegisterComponent>
  let userService: UserService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [RegisterComponent],
      imports: [AppRoutingModule, HttpClientModule, FormsModule, ReactiveFormsModule],
      providers: [UserService]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterComponent);
    component = fixture.componentInstance;
    componentHtml = fixture.debugElement.nativeElement;
    fixture.detectChanges();
  })

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  // Niek Boon
  // Testing retrieving data from input fields and checking if onSubmit will work.
  it('Should be able to create a new user (account)', () => {
    let firstNameInput: HTMLInputElement = componentHtml.querySelector('#firstName');
    let lastNameInput: HTMLInputElement = componentHtml.querySelector('#lastName');
    let birthDateInput: HTMLInputElement = componentHtml.querySelector('#birthDate');
    let emailAdressInput: HTMLInputElement = componentHtml.querySelector('#emailAddress');
    let passwordInput: HTMLInputElement = componentHtml.querySelector('#password');
    let passwordRepeatInput: HTMLInputElement = componentHtml.querySelector('#passwordRepeat');
    let countryInput: HTMLInputElement = componentHtml.querySelector('#country');

    firstNameInput.value = 'Niek';
    lastNameInput.value = 'Boon';
    birthDateInput.value = "1998-10-28";
    emailAdressInput.value = 'niek@niek.com';
    passwordInput.value = 'password';
    passwordRepeatInput.value = 'password';
    countryInput.value = 'The Netherlands';

    component.registerForm.get('firstName').setValue(firstNameInput.value);
    component.registerForm.get('lastName').setValue(lastNameInput.value);
    component.registerForm.get('birthDate').setValue(birthDateInput.value);
    component.registerForm.get('emailAddress').setValue(emailAdressInput.value);
    component.registerForm.get('password').setValue(passwordInput.value);
    component.registerForm.get('passwordRepeat').setValue(passwordRepeatInput.value);
    component.registerForm.get('country').setValue(countryInput.value);
    fixture.detectChanges();

    let result: boolean = component.onSubmit();

    expect(result).toBe(true);
  });

  it('should add user in service', function () {
    userService = TestBed.inject(UserService);
    let testUser = new User('Lars', 'test', 'lars@test', 'testtt', new Date(1999, 3, 3), 'netherlands', 'test', 'engage/src/assets/images/ananas.png');
    userService.add(testUser)
    expect(testUser).not.toBeNull();
    expect(testUser.firstName).toEqual('Lars')
  });

  it('should check if form input name is valid', function () {
    let firstName = component.registerForm.controls['firstName'];
    let lastName = component.registerForm.controls['lastName'];
    let errors = {};
    expect(firstName.valid && lastName).toBeFalsy();
    errors = firstName.errors;
    expect(errors['required']).toBeTruthy();
    firstName.setValue("Lars");
    errors = firstName.errors || {};
    expect(errors['required']).toBeFalsy();

  });
});
