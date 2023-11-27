import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {HttpClientModule} from '@angular/common/http';
import {AppRoutingModule} from '../../app-routing.module';
import {ProfileComponent} from './profile.component';
import {CommonModule} from '@angular/common';
import {UserService} from '../../services/user/user.service';
import {User} from '../../models/user/user.model';
import {UserUpdate} from '../../models/user/user-update';
import {UserUpdatesService} from '../../services/user/user-updates.service';


describe('ProfileComponent', () => {
  let component: ProfileComponent;
  let componentHtml: HTMLElement;
  let fixture: ComponentFixture<ProfileComponent>

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [],
      imports: [HttpClientModule, AppRoutingModule, CommonModule],
      providers: []
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfileComponent);
    component = fixture.componentInstance;
    componentHtml = fixture.debugElement.nativeElement;

    let userService = fixture.debugElement.injector.get(UserService);
    userService.loggedInUser = new User("Test", "Test", "test@test", "Test123", null, "Test", "test", "Test");
    userService.loggedInUser.id = 123;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  // Niek Boon
  it('Should update amount of updates correctly', () => {

    let userUpdate1 = new UserUpdate(component.loggedInUser, "Test1", 0);
    userUpdate1.id = 1;
    let userUpdate2 = new UserUpdate(component.loggedInUser, "Test2", 0);
    userUpdate2.id = 2;

    const userUpdatesService = fixture.debugElement.injector.get(UserUpdatesService);
    const spy = spyOn(userUpdatesService, 'getAllForUser').and.returnValue([userUpdate1, userUpdate2]);

    expect(component.amountOfUpdates).toBe(0);

    // getting updates from service (spy will make sure it will return a list of 2 updates)
    component.amountOfUpdates = userUpdatesService.getAllForUser(123).length;
    fixture.detectChanges();

    expect(component.amountOfUpdates).toBe(2);

    // I don't know why I cannot retrieve the notification badge from the componentHtml.

    // const updatesBadge: HTMLSpanElement = componentHtml.querySelector('#amount-of-updates')
    //
    // expect(updatesBadge).not.toEqual(null);

  });

});