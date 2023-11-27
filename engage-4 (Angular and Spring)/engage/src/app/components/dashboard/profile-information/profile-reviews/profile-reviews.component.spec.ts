import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {AppRoutingModule} from '../../../../app-routing.module';
import {HttpClientModule} from '@angular/common/http';
import {ProfileReviewsComponent} from './profile-reviews.component';
import {CommonModule} from '@angular/common';
import {DecimalPipe} from '@angular/common';

describe('ProfileReviewsComponent', () => {
  let component: ProfileReviewsComponent;
  let componentHtml: HTMLElement;
  let fixture: ComponentFixture<ProfileReviewsComponent>

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [DecimalPipe],
      providers: [],
      imports: [AppRoutingModule, HttpClientModule, CommonModule],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfileReviewsComponent);
    component = fixture.componentInstance;
    componentHtml = fixture.debugElement.nativeElement;
    fixture.detectChanges();
  })

  // Niek Boon
  // it('\'Review this user\' button should not exist if the loggedInUser is not part of the same project', () => {
  //   component.loggedInUser = new User("Niek", "Boon", "niek_boon@hotmail.com", "password", new Date(1998, 10, 28), "Netherlands", "Cool user", "assets/images/hello.png");
  //   component.loggedInUser.id = 1;
  //   component.user = new User("Test", "Test", "test@test", "test", new Date(1998, 10, 28), "test", "test", "test");
  //   component.user.id = 2;
  //
  //   fixture.detectChanges();
  //
  //   const reviewButton: HTMLButtonElement = componentHtml.querySelector('.review-button');
  //   expect(reviewButton).toEqual(null);
  // })

});