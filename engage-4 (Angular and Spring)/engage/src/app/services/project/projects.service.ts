import {EventEmitter, Injectable} from '@angular/core';
import {Project} from '../../models/project/project';
import {Observable, Subject} from 'rxjs';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";
import {User} from "../../models/user/user.model";
import {UserService} from "../user/user.service";
import {PendingRequest} from "../../models/project/pending-request";
import {ProjectInvite} from "../../models/project/project-invite";
import {EngagedOrganisation} from '../../models/project/engaged-organisation';
import {ProjectMemberService} from './project-member.service';

@Injectable({
  providedIn: 'root'
})
export class ProjectsService {
  projectsChanged = new EventEmitter();
  savedProjectSubject = new Subject<Project>();
  projects: Project[];


  //photo data
  projectHasPhoto: boolean;
  selectedFile: File;
  retrievedImage: any;
  base64Data: any;
  retrieveResonse: any;
  message: string;
  imageName: any;
  constructor(private userService: UserService, private projectMemberService: ProjectMemberService, private httpClient: HttpClient) {
    this.projects = [];
    this.restGetProjects().subscribe(projects => {
      this.projects = projects;
      this.projectsChanged.emit();
    }, error => {
      console.log(error.message);
    })
  }

  findAll(): Project[] {
    return this.projects; // returns a copy of the projects list
  }

  findAllForUser(id: number): Project[] {
    let projectList = [];
    const projectMembers = this.projectMemberService.getAllForUser(id);
    for (let i = 0; i < projectMembers.length; i++) {
      projectList.push(projectMembers[i].project);
    }
    return projectList;
  }

  findById(oId: number): Project {
    for (let i = 0; i < this.projects.length; i++) {
      if (this.projects[i].id === oId) {
        return this.projects[i];
      }
    }
    return null;
  }

  /**
   * Takes in an project to be saved and returns the old replaced project
   * @param project
   */

  save(project: Project) {
    this.restPostProject(project).subscribe(responseProject => {
      this.projects.push(responseProject);
      this.savedProjectSubject.next(responseProject);
      this.projectsChanged.emit();
    })
  }

  update(project: Project) {
    this.restPutProject(project).subscribe(() => {

      for (let i = 0; i < this.projects.length; i++) {
        if (project.id === this.projects[i].id) {
          this.projects[i] = project;
          this.projectsChanged.emit();
        }
      }
    })
  }

  deleteById(pId: number): boolean {
    this.restDeleteProject(pId).subscribe(() => {

      for (let i = 0; i < this.projects.length; i++) {
        if (this.projects[i].id === pId) {
          this.projects.splice(i, 1);
          this.projectsChanged.emit();
          return true;
        }
      }
    })
    return false;
  }

  getProjectOwner(project: Project): User {
    if (project !== null) {
      const members = this.projectMemberService.getAllForProject(project.id)
      for (let i = 0; i < members.length; i++) {
        if (members[i].owner) {
          return members[i].user;
        }
      }
    }

    return null;
  }

  restGetProjects(): Observable<Project[]> {
    return this.httpClient.get<Project[]>(`${environment.apiUrl}/projects`);
  }

  restPostProject(project: Project): Observable<Project> {
    return this.httpClient.post<Project>(`${environment.apiUrl}/projects`, project);
  }

  restPutProject(project: Project): Observable<Project> {
    const url = (`${environment.apiUrl}/projects/ + ${project.id}`);
    return this.httpClient.put<Project>(url, project);
  }

  restDeleteProject(projectId: number): Observable<Project> {
    const url = (`${environment.apiUrl}/projects/ + ${projectId}`);
    return this.httpClient.delete<Project>(url);
  }

  projectHasUploadedPhoto(projectId: number) {
    this.httpClient.get('http://localhost:8080/image/get/checkIfProjectPhotoExist/' + projectId )
      .subscribe(
        res => {

          if (res === true){
            this.projectHasPhoto = true;
            this.getImageForProject(projectId);
          }else {
            this.projectHasPhoto = false;
          }


        }
      );

    return false;
  }

  getImageForProject(projectId: number) {
    this.httpClient.get('http://localhost:8080/image/get/projectImage/' + projectId)
      .subscribe(
        res => {
          this.retrieveResonse = res;
          this.base64Data = this.retrieveResonse.picByte;
          this.retrievedImage = 'data:image/jpeg;base64,' + this.base64Data;

          if (this.retrieveResonse.picByte === null){
            this.projectHasPhoto = false;
          }else {

            this.projectHasPhoto = true;
          }
          return;
        }
      );
  }


}
