import {async, ComponentFixture, TestBed} from '@angular/core/testing';
import {CreateProjectComponent} from './create-project.component';
import {HttpClientModule} from '@angular/common/http';
import {AppRoutingModule} from '../../../app-routing.module';

describe('CreateProjectComponent', () => {
  let component: CreateProjectComponent;
  let componentHtml: HTMLElement;
  let fixture: ComponentFixture<CreateProjectComponent>

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [],
      imports: [HttpClientModule, AppRoutingModule],
      providers: []
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateProjectComponent);
    component = fixture.componentInstance;
    componentHtml = fixture.debugElement.nativeElement;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

});