import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {AboutComponent} from './about.component';
import {User} from '../../models/user/user.model';
import {HttpClient, HttpClientModule, HttpHandler} from '@angular/common/http';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {By} from '@angular/platform-browser';
import {ProjectsService} from '../../services/project/projects.service';

describe('AboutComponent', () => {
  let component: AboutComponent;
  let componentHtml: HTMLElement;
  let fixture: ComponentFixture<AboutComponent>

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [AboutComponent],
      imports : [BrowserAnimationsModule, HttpClientModule],
      providers: []
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AboutComponent);
    component = fixture.componentInstance;
    componentHtml = fixture.debugElement.nativeElement;
    fixture.detectChanges();
  })

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });


  // Niek Boon
  it('Register button should not exist in html if user is logged in', () => {

    component.loggedInUser = new User("Niek", "Boon", "niek_boon@hotmail.com", "password", new Date(1998, 10, 28), "Netherlands", "Cool user", "assets/images/hello.png");
    fixture.detectChanges();
    const registerButton: HTMLButtonElement = componentHtml.querySelector('#register-button')

    expect(registerButton).toEqual(null);
  });

});
