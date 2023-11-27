import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CompanyInformationComponent } from './company-information.component';
import {HttpClient, HttpClientModule, HttpHandler} from "@angular/common/http";
import {OrganisationMember} from "../../../models/organisation/organisation-member";
import {User} from "../../../models/user/user.model";
import {Organisation} from "../../../models/organisation/organisation";
import {AppRoutingModule} from "../../../app-routing.module";

describe('CompanyComponent', () => {
  let component: CompanyInformationComponent;
  let componentHtml: HTMLElement;
  let fixture: ComponentFixture<CompanyInformationComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CompanyInformationComponent ],
      imports: [AppRoutingModule, HttpClientModule],
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CompanyInformationComponent);
    component = fixture.componentInstance;
    componentHtml = fixture.debugElement.nativeElement;
    fixture.detectChanges();
  })


  //Lars (2 tests)
  it('should add member correctly and if the member is not owner/admin then edit button should not exist', () => {
    component.loggedInUser = new User('Lars', 'test', 'lars@test', 'testtt', new Date(1999, 3, 3), 'netherlands', 'test', 'engage/src/assets/images/ananas.png');
    component.loggedInUser.id = 10000;
    let organisation = new Organisation('lars', 'test', 'test@test', 'test', new Date(2000,3,2), 'engage/src/assets/images/ananas.png');
    organisation.id = 10000;
    let organisationMember = new OrganisationMember(component.loggedInUser, organisation, false, false);
    organisationMember.id = 10000;
    component.members.push(organisationMember);
    const editButton: HTMLButtonElement = componentHtml.querySelector('#edit-button');
    fixture.detectChanges();
    expect(editButton).toEqual(null);
    expect(component.members.length).toBeGreaterThan(0);
    expect(component.members[0]).toEqual(organisationMember);
  })
});
