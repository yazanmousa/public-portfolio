import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {DiagramComponent} from './diagram.component';
import {AppRoutingModule} from '../../../../app-routing.module';
import {HttpClientModule} from '@angular/common/http';
import {ProjectsService} from '../../../../services/project/projects.service';
import {Organisation} from '../../../../models/organisation/organisation';
import {Project} from '../../../../models/project/project';
import {EngagedOrganisation} from '../../../../models/project/engaged-organisation';
import {ActivatedRoute} from '@angular/router';
import {of} from 'rxjs';

describe('DiagramComponent', () => {
  let component: DiagramComponent;
  let componentHtml: HTMLElement;
  let fixture: ComponentFixture<DiagramComponent>


  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [],
      imports: [AppRoutingModule, HttpClientModule],
      providers: [{provide: ActivatedRoute, useValue: {params: of({id: 6969})}}]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DiagramComponent);
    component = fixture.componentInstance;
    componentHtml = fixture.debugElement.nativeElement;
    fixture.detectChanges();
  })

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  // Niek Boon
  it('should add engaged organisations to the \'members\' array upon initialization', () => {
    let organisation = new Organisation("test", "test", "test@test", "test", null, "test");
    organisation.id = 69;
    let project = new Project("Test", "Test", "Test", 69, "Test", null);
    project.id = 6969
    let engagedOrganisation = new EngagedOrganisation(organisation, project, 3, "Business");
    engagedOrganisation.id = 696969

    component.project = project;
    component.engagedOrganisations.push(engagedOrganisation);
    component.addMembers();
    fixture.detectChanges();

    expect(component.members.length).toBeGreaterThan(0);
    expect(component.members[0].name).not.toEqual(null);
    expect(component.members[0].level).not.toEqual(0);
    expect(component.members[0].category).not.toEqual(null);
  })

  // Niek Boon
  it('Should fetch project from the projectsService correctly', () => {
    let project = new Project("Test", "Test", "Test", 69, "Test", null);
    project.id = 6969

    const projectsService = fixture.debugElement.injector.get(ProjectsService)
    const spy = spyOn(projectsService, 'findById').and.returnValue(project);
    component.project = projectsService.findById(6969);
    fixture.detectChanges();

    expect(spy.calls.first().returnValue.id).toBe(6969);
    expect(component.project.id).toBe(6969);
  })

});
