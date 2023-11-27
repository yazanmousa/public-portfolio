import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {NavbarComponent} from './navbar/navbar.component';
import {RegisterComponent} from './components/register/register.component';
import {AboutComponent} from './components/about/about.component';
import {MyProjectsOverviewComponent} from './components/my-projects-overview/my-projects-overview.component';
import {MyProjectsCreatedComponent} from './components/my-projects-overview/my-projects-created/my-projects-created.component';
import {ProfileComponent} from './components/dashboard/profile.component';
import {ProfileEditComponent} from './components/dashboard/profile-edit/profile-edit.component';
import {ProfileInformationComponent} from './components/dashboard/profile-information/profile-information.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {ErrorComponent} from './components/not-found/error/error.component';
import {NotFoundComponent} from './components/not-found/not-found.component';
import {ProjectSearchComponent} from './components/project/project-search/project-search.component';
import {ProjectFilterPipe} from './pipes/project-filter.pipe';
import {FooterComponent} from './components/footer/footer.component';
import {ProjectInformationComponent} from './components/project/project-information/project-information.component';
import {MyCompanyComponent} from './components/my-projects-overview/my-company/my-company.component';
import {CompanyInformationComponent} from './components/company/company-information/company-information.component';
import {CreateCompanyComponent} from './components/company/create-company/create-company.component';
import {CommonModule} from '@angular/common';
import {CreateProjectComponent} from './components/project/create-project/create-project.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {NgSelectModule} from '@ng-select/ng-select';
import {OrganisationFilterPipe} from './pipes/organisation-filter.pipe';
import { ProfileProjectsComponent } from './components/dashboard/profile-projects/profile-projects.component';
import { LatestUpdatesComponent } from './components/dashboard/latest-updates/latest-updates.component';
import { CreateOrganisationPromptComponent } from './components/dashboard/create-organisation-prompt/create-organisation-prompt.component';
import { CompanySearchComponent } from './components/company/company-search/company-search.component';
import { DragDropModule } from "@angular/cdk/drag-drop";
import {ViewInvitesComponent} from './components/dashboard/view-invites/view-invites.component';
import { FaqComponent } from './components/faq/faq.component';
import {ProjectInviteComponent} from "./components/project/project-invite/project-invite.component";
import { UserSearchComponent } from './components/user-search/user-search.component';
import { UserPipePipe } from './pipes/user-pipe.pipe';
import { FaqProfileComponent } from './components/faq/faq-profile/faq-profile.component';
import { FaqProjectsComponent } from './components/faq/faq-projects/faq-projects.component';
import { FaqOrganisationsComponent } from './components/faq/faq-organisations/faq-organisations.component';
import { FaqDiagramComponent } from './components/faq/faq-diagram/faq-diagram.component';
import {HttpClient, HttpClientModule} from '@angular/common/http';
import {OrganisationMemberPipe} from './pipes/organisation-member-pipe';
import {MatSlideToggleModule} from "@angular/material/slide-toggle";
import { ProfileReviewsComponent } from './components/dashboard/profile-information/profile-reviews/profile-reviews.component';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import {RatingModule} from 'ng-starrating';
import {ChartModule} from '@syncfusion/ej2-angular-charts';
import { DiagramComponent } from './components/project/project-information/diagram/diagram.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    ProfileEditComponent,
    ProfileInformationComponent,
    RegisterComponent,
    AboutComponent,
    MyProjectsOverviewComponent,
    MyProjectsCreatedComponent,
    ProfileComponent,
    ErrorComponent,
    NotFoundComponent,
    ProjectInformationComponent,
    ProjectSearchComponent,
    ProjectFilterPipe,
    OrganisationMemberPipe,
    FooterComponent,
    CompanyInformationComponent,
    CreateCompanyComponent,
    MyCompanyComponent,
    CreateProjectComponent,
    OrganisationFilterPipe,
    ProfileProjectsComponent,
    LatestUpdatesComponent,
    CreateOrganisationPromptComponent,
    ViewInvitesComponent,
    FaqComponent,
    CompanySearchComponent,
    ProjectInviteComponent,
    UserSearchComponent,
    UserPipePipe,
    FaqProfileComponent,
    FaqProjectsComponent,
    FaqOrganisationsComponent,
    FaqDiagramComponent,
    ProfileReviewsComponent,
    DiagramComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    CommonModule,
    BrowserAnimationsModule,
    NgSelectModule,
    DragDropModule,
    HttpClientModule,
    MatSlideToggleModule,
    MatProgressBarModule,
    NgbModule,
    RatingModule,
    ChartModule,
  ],
  providers: [HttpClient],
  bootstrap: [AppComponent]
})

export class AppModule {

}
