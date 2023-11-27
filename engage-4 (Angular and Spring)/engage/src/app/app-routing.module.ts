import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {AboutComponent} from './components/about/about.component';
import {MyProjectsOverviewComponent} from './components/my-projects-overview/my-projects-overview.component';
import {RegisterComponent} from './components/register/register.component';
import {ProfileComponent} from './components/dashboard/profile.component';
import {ErrorComponent} from './components/not-found/error/error.component';
import {ProjectInformationComponent} from './components/project/project-information/project-information.component';
import {CompanyInformationComponent} from './components/company/company-information/company-information.component';
import {CreateCompanyComponent} from './components/company/create-company/create-company.component';
import {CreateProjectComponent} from './components/project/create-project/create-project.component';
import {ProjectSearchComponent} from './components/project/project-search/project-search.component';
import {ProfileInformationComponent} from './components/dashboard/profile-information/profile-information.component';
import {ProfileProjectsComponent} from './components/dashboard/profile-projects/profile-projects.component';
import {ProfileEditComponent} from './components/dashboard/profile-edit/profile-edit.component';
import {CreateOrganisationPromptComponent} from './components/dashboard/create-organisation-prompt/create-organisation-prompt.component';
import {LatestUpdatesComponent} from './components/dashboard/latest-updates/latest-updates.component';
import {CompanySearchComponent} from './components/company/company-search/company-search.component';
import {FaqComponent} from './components/faq/faq.component';
import {ProjectInviteComponent} from './components/project/project-invite/project-invite.component';
import {ViewInvitesComponent} from './components/dashboard/view-invites/view-invites.component';
import {UserSearchComponent} from './components/user-search/user-search.component';
import {FaqProfileComponent} from './components/faq/faq-profile/faq-profile.component';
import {FaqProjectsComponent} from './components/faq/faq-projects/faq-projects.component';
import {FaqOrganisationsComponent} from './components/faq/faq-organisations/faq-organisations.component';
import {FaqDiagramComponent} from './components/faq/faq-diagram/faq-diagram.component';

const routes: Routes = [
  {path: '', component: AboutComponent, pathMatch: 'full'},
  {path: 'home', component: AboutComponent},
  {
    path: 'profile', component: ProfileComponent, children: [
      {path: 'latest-updates/:id', component: LatestUpdatesComponent},
      {path: 'my-information/:id', component: ProfileInformationComponent},
      {path: 'edit-information/:id', component: ProfileEditComponent},
      {path: 'my-projects/:id', component: ProfileProjectsComponent},
      {path: 'my-organisation/:id', component: CompanyInformationComponent},
      {path: 'my-project/:id', component: ProjectInformationComponent},
      {path: 'create-organisation-prompt', component: CreateOrganisationPromptComponent},
      {path: 'view-invites', component: ViewInvitesComponent},
      {path: 'search-organisation', component: CompanySearchComponent},
      {path: 'create-company', component: CreateCompanyComponent},
      {path: 'update-company/:id', component: CreateCompanyComponent},
      {path: 'create-project', component: CreateProjectComponent},
      {path: 'update-project/:id', component: CreateProjectComponent},
      {path: 'project-invite/:id', component: ProjectInviteComponent},
      {path: 'profile-information', component: ProfileInformationComponent}
    ]
  },
  {path: 'profile-information/:id', component: ProfileInformationComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'my-projects-overview', component: MyProjectsOverviewComponent},
  {path: 'project-information/:id', component: ProjectInformationComponent},
  {path: 'company-information/:id', component: CompanyInformationComponent},
  {path: 'search-projects', component: ProjectSearchComponent},
  {path: 'search-user', component: UserSearchComponent},

  {
    path: 'faq', component: FaqComponent, children: [
      {path: 'profile', component: FaqProfileComponent},
      {path: 'projects', component: FaqProjectsComponent},
      {path: 'organisations', component: FaqOrganisationsComponent},
      {path: 'diagram', component: FaqDiagramComponent}
    ]
  },
  {path: 'not-found', component: ErrorComponent, data: {message: 'Page was not found!'}},
  {path: '**', redirectTo: '/not-found'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {relativeLinkResolution: 'legacy'})],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
