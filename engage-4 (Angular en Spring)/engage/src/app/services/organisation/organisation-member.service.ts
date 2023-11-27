import { Injectable, EventEmitter } from '@angular/core';
import {Observable} from 'rxjs';
import {environment} from '../../../environments/environment';
import {HttpClient, HttpEvent, HttpHeaders, HttpRequest} from '@angular/common/http';
import {OrganisationMember} from '../../models/organisation/organisation-member';

@Injectable({
  providedIn: 'root'
})
export class OrganisationMemberService {
  members: OrganisationMember[];
  membersChanged = new EventEmitter();

  constructor(private httpClient: HttpClient) {
    this.members = [];
    this.restGetOrganisationMembers().subscribe(response => {
      this.members = response;
    }, error => {
      console.log(error.message);
    })
  }

  findAll(): OrganisationMember[] {
    return this.members;
  }

  findById(id: number): OrganisationMember {
    for (let i = 0; i < this.members.length; i++) {
      if (this.members[i].id === id) {
        return this.members[i];
      }
    }
  }

  save(member: OrganisationMember) {

    this.restPostOrganisationMember(member).subscribe(response => {
      this.members.push(response);
      this.membersChanged.emit();
    })

  }

  update(member: OrganisationMember) {
    this.restPutOrganisationMember(member).subscribe(response => {
      for (let i = 0; i < this.members.length; i++) {
        if (response.id === this.members[i].id) {
          this.members[i] = response;
          this.membersChanged.emit();
        }
      }
    })
  }

  updateWithoutEmit(member: OrganisationMember) {
    this.restPutOrganisationMember(member).subscribe(response => {
      for (let i = 0; i < this.members.length; i++) {
        if (response.id === this.members[i].id) {
          this.members[i] = response;
        }
      }
    })
  }

  deleteById(id: number) {
    this.restDeleteOrganisationMember(id).subscribe(() => {
      for (let i = 0; i < this.members.length; i++) {
        if (this.members[i].id === id) {
          this.members.splice(i, 1);
          this.membersChanged.emit();
        }
      }
    })
  }

  deleteMultipleMembers(members: OrganisationMember[]) {
    this.restDeleteMultipleMembers(members).subscribe(response => {
      for (let i = 0; i < members.length; i++) {
        let index = this.members.indexOf(members[i]);
        this.members.splice(index, 1);
      }
      this.membersChanged.emit();
    })
  }

  getAllForOrganisation(organisationId: number): OrganisationMember[] {
    let tempMembers = [];
    for (let i = 0; i < this.members.length; i++) {
      if (this.members[i].organisation.id === organisationId) {
        tempMembers.push(this.members[i]);
      }
    }
    return tempMembers;
  }

  getMemberForUser(userId: number): OrganisationMember {
    for (let i = 0; i < this.members.length; i++) {
      if (this.members[i].user.id === userId) {
        return this.members[i];
      }
    }
    return null;
  }

  // back-end http requests
  restGetOrganisationMembers(): Observable<OrganisationMember[]> {
    return this.httpClient.get<OrganisationMember[]>(`${environment.apiUrl}/organisation-members`);
  }

  restPostOrganisationMember(member: OrganisationMember): Observable<OrganisationMember> {
    return this.httpClient.post<OrganisationMember>(`${environment.apiUrl}/organisation-members`, member);
  }

  restPutOrganisationMember(member: OrganisationMember): Observable<OrganisationMember> {
    const url = `${environment.apiUrl}/organisation-members/` + member.id;
    return this.httpClient.put<OrganisationMember>(url, member);
  }

  restDeleteOrganisationMember(memberId: number): Observable<OrganisationMember> {
    const url = `${environment.apiUrl}/organisation-members/` + memberId;
    return this.httpClient.delete<OrganisationMember>(url);
  }

  restDeleteMultipleMembers(members: OrganisationMember[]): Observable<OrganisationMember[]> {
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }),
      body: members
    };

    return this.httpClient.delete<OrganisationMember[]>(`${environment.apiUrl}/organisation-members`, options);
  }

}
