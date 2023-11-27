import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from "rxjs";
import {environment} from "../../../environments/environment";
import {ProjectMember} from "../../models/project/project-member";

@Injectable({
  providedIn: 'root'
})
export class ProjectMemberService {
  members: ProjectMember[];
  membersChanged = new EventEmitter();

  constructor(private httpClient: HttpClient) {
    this.members = [];
    this.restGetProjectMembers().subscribe(response => {
      this.members = response;
    }, error => {
      console.log(error.message);
    })
  }

  findAll(): ProjectMember[] {
    return this.members;
  }

  findById(id: number): ProjectMember {
    for (let i = 0; i < this.members.length; i++) {
      if (this.members[i].id === id) {
        return this.members[i];
      }
    }
  }

  save(member: ProjectMember): ProjectMember {
    let returnProjectMember: ProjectMember = null;

    this.restPostProjectMember(member).subscribe(response => {
      this.members.push(response);
      returnProjectMember = response;
      this.membersChanged.emit();
    })
    return returnProjectMember;
  }

  update(member: ProjectMember) {
    this.restPutProjectMember(member).subscribe(response => {
      for (let i = 0; i < this.members.length; i++) {
        if (response.id === this.members[i].id) {
          this.members[i] = response;
          this.membersChanged.emit();
        }
      }
    })
  }

  updateWithoutEmit(member: ProjectMember) {
    this.restPutProjectMember(member).subscribe(response => {
      for (let i = 0; i < this.members.length; i++) {
        if (response.id === this.members[i].id) {
          this.members[i] = response;
        }
      }
    })
  }

  deleteById(id: number) {
    this.restDeleteProjectMember(id).subscribe(() => {
      for (let i = 0; i < this.members.length; i++) {
        if (this.members[i].id === id) {
          this.members.splice(i, 1);
          this.membersChanged.emit();
        }
      }
    })
  }

  deleteMultipleMembers(members: ProjectMember[]) {
    this.restDeleteMultipleMembers(members).subscribe(response => {
      for (let i = 0; i < members.length; i++) {
        let index = this.members.indexOf(members[i]);
        this.members.splice(index, 1);
      }
      this.membersChanged.emit();
    })
  }

  getAllForProject(projectId: number): ProjectMember[] {
    let tempMembers = [];
    for (let i = 0; i < this.members.length; i++) {
      if (this.members[i].project.id === projectId) {
        tempMembers.push(this.members[i]);
      }
    }
    return tempMembers;
  }

  getAllForUser(userId: number): ProjectMember[] {
    let tempMembers = [];
    for (let i = 0; i < this.members.length; i++) {
      if (this.members[i].user.id === userId) {
        tempMembers.push(this.members[i]);
      }
    }
    return tempMembers;
  }

  getMemberForUser(userId: number, projectId: number): ProjectMember {
    for (let i = 0; i < this.members.length; i++) {
      if (this.members[i].user.id === userId && this.members[i].project.id === projectId) {
        return this.members[i];
      }
    }
    return null;
  }

  restGetProjectMembers(): Observable<ProjectMember[]> {
    return this.httpClient.get<ProjectMember[]>(`${environment.apiUrl}/project-members`);
  }

  restPostProjectMember(member: ProjectMember): Observable<ProjectMember> {
    return this.httpClient.post<ProjectMember>(`${environment.apiUrl}/project-members`, member);
  }

  restPutProjectMember(member: ProjectMember): Observable<ProjectMember> {
    const url = `${environment.apiUrl}/project-members/` + member.id;
    return this.httpClient.put<ProjectMember>(url, member);
  }

  restDeleteProjectMember(memberId: number): Observable<ProjectMember> {
    const url = `${environment.apiUrl}/project-members/` + memberId;
    return this.httpClient.delete<ProjectMember>(url);
  }

  restDeleteMultipleMembers(members: ProjectMember[]): Observable<ProjectMember[]> {
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }),
      body: members
    };

    return this.httpClient.delete<ProjectMember[]>(`${environment.apiUrl}/project-members`, options);
  }
}
