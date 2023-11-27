import {CompanyInformationComponent} from "../company-information/company-information.component";
import {ComponentFixture, TestBed} from "@angular/core/testing";
import {AppRoutingModule} from "../../../app-routing.module";
import {HttpClientModule} from "@angular/common/http";
import {CreateCompanyComponent} from "./create-company.component";
import {Organisation} from "../../../models/organisation/organisation";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {OrganisationService} from "../../../services/organisation/organisation.service";
import {of} from "rxjs";
import {ProjectsService} from "../../../services/project/projects.service";
import {ActivatedRoute} from "@angular/router";

describe('Create Company', () => {
  let component: CreateCompanyComponent;
  let componentHtml: HTMLElement;
  let fixture: ComponentFixture<CreateCompanyComponent>

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreateCompanyComponent ],
      imports: [AppRoutingModule, HttpClientModule, ReactiveFormsModule, FormsModule],
      providers: [{provide: ActivatedRoute, useValue: {params: of({id: 9999})}}]
    })
      .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateCompanyComponent);
    component = fixture.componentInstance;
    componentHtml = fixture.debugElement.nativeElement;
    fixture.detectChanges();
  })

  //Lars
  it('should add and find organisation 9999', function () {
    let organisation = new Organisation('Test', 'the netherlands', 'test@test', 'test@test', new Date(2000,3,4,), 'engage/src/assets/images/aardbei.png');
    organisation.id = 9999;
      const organisationService = fixture.debugElement.injector.get(OrganisationService);

    organisationService.organisations.push(organisation);
    component.ngOnInit();
    fixture.detectChanges();

    expect(component.editOrganisation.id).toEqual(9999);
    expect(component.editOrganisation).not.toEqual(null);
    expect(component.editOrganisation).not.toEqual(undefined);
  });

});
