import { Injectable, EventEmitter } from '@angular/core';
import {ProjectInvite} from "../../models/project/project-invite";
import {environment} from "../../../environments/environment";
import {Observable} from 'rxjs';
import {HttpClient, HttpHeaders} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ProjectInviteService {
  pendingInvitesChanged = new EventEmitter();
  invites: ProjectInvite[];

  constructor(private httpClient: HttpClient) {
    this.invites = [];
    this.restGetInvites().subscribe(invites => {
      this.invites = invites;
    })
  }

  findAll() {
    return this.invites;
  }

  findInvitesFor(userId: number): ProjectInvite[] {
    let pendingInvites = [];
    for (let i = 0; i < this.invites.length; i++) {
      if (this.invites[i].receivedByUser.id === userId) {
        pendingInvites.push(this.invites[i])
      }
    }
    return pendingInvites;
  }

  save(invite: ProjectInvite) {
    this.restPostInvite(invite).subscribe(response => {
      this.invites.push(response);
      this.pendingInvitesChanged.emit();
    })
  }

  deleteProjectInvite(id: number) {
    this.restDeleteInvite(id).subscribe(() => {
      for (let i = 0; i < this.invites.length; i++) {
        if(this.invites[i].id === id){
          this.invites.splice(i, 1);
          this.pendingInvitesChanged.emit();
        }
      }
    })

  }

  deleteMultipleInvites(invites: ProjectInvite[]) {
    this.restDeleteMultipleInvites(invites).subscribe(response => {
      for (let i = 0; i < invites.length; i++) {
        let index = this.invites.indexOf(invites[i]);
        this.invites.splice(index, 1);
      }
      this.pendingInvitesChanged.emit();
    })
  }

  restGetInvites(): Observable<ProjectInvite[]> {
    return this.httpClient.get<ProjectInvite[]>(`${environment.apiUrl}/project-invites`);
  }

  restPostInvite(projectInvite: ProjectInvite): Observable<ProjectInvite> {
    return this.httpClient.post<ProjectInvite>(`${environment.apiUrl}/project-invites`, projectInvite);
  }

  restDeleteInvite(id: number){
    const url = (`${environment.apiUrl}/project-invites/ + ${id}`)
    return this.httpClient.delete(url);
  }

  restDeleteMultipleInvites(invites: ProjectInvite[]): Observable<ProjectInvite[]> {
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }),
      body: invites
    };

    return this.httpClient.delete<ProjectInvite[]>(`${environment.apiUrl}/project-invites`, options);
  }

}
