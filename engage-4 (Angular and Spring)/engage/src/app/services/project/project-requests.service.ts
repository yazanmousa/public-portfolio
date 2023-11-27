import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from "rxjs";
import {environment} from "../../../environments/environment";
import {PendingRequest} from "../../models/project/pending-request";
import {ProjectMember} from '../../models/project/project-member';

@Injectable({
  providedIn: 'root'
})
export class ProjectRequestsService {
  pendingRequests: PendingRequest[];
  pendingRequestsChanged = new EventEmitter();

  constructor(private httpClient: HttpClient) {
    this.pendingRequests = [];
    this.restGetPendingRequests().subscribe(response => {
      this.pendingRequests = response;
    }, error => {
      console.log(error.message);
    })
  }

  findAll(): PendingRequest[] {
    return this.pendingRequests;
  }

  findById(id: number): PendingRequest {
    for (let i = 0; i < this.pendingRequests.length; i++) {
      if (this.pendingRequests[i].id === id) {
        return this.pendingRequests[i];
      }
    }
  }

  save(pendingRequest: PendingRequest) {

    this.restPostPendingRequests(pendingRequest).subscribe(response => {
      this.pendingRequests.push(response);
      this.pendingRequestsChanged.emit();
    })

  }

  update(pendingRequest: PendingRequest) {
    this.restPutPendingRequests(pendingRequest).subscribe(response => {
      for (let i = 0; i < this.pendingRequests.length; i++) {
        if (response.id === this.pendingRequests[i].id) {
          this.pendingRequests[i] = response;
          this.pendingRequestsChanged.emit();
        }
      }
    })
  }

  deleteById(id: number) {
    this.restDeletePendingRequests(id).subscribe(() => {
      for (let i = 0; i < this.pendingRequests.length; i++) {
        if (this.pendingRequests[i].id === id) {
          this.pendingRequests.splice(i, 1);
          this.pendingRequestsChanged.emit();
        }
      }
    })
  }

  deleteMultipleRequests(requests: PendingRequest[]) {
    this.restDeleteMultipleRequests(requests).subscribe(response => {
      for (let i = 0; i < requests.length; i++) {
        let index = this.pendingRequests.indexOf(requests[i]);
        this.pendingRequests.splice(index, 1);
      }
      this.pendingRequestsChanged.emit();
    })
  }

  getAllForProject(projectId: number): PendingRequest[] {
    let tempRequests = [];
    for (let i = 0; i < this.pendingRequests.length; i++) {
      if (this.pendingRequests[i].project.id === projectId) {
        tempRequests.push(this.pendingRequests[i]);
      }
    }
    return tempRequests;
  }

  getAllForUser(userId: number): PendingRequest[] {
    let tempRequests = [];
    for (let i = 0; i < this.pendingRequests.length; i++) {
      if (this.pendingRequests[i].sendByUser.id === userId) {
        tempRequests.push(this.pendingRequests[i]);
      }
    }
    return tempRequests;
  }

  restGetPendingRequests(): Observable<PendingRequest[]> {
    return this.httpClient.get<PendingRequest[]>(`${environment.apiUrl}/project-requests`);
  }

  restPostPendingRequests(pendingRequest: PendingRequest): Observable<PendingRequest> {
    return this.httpClient.post<PendingRequest>(`${environment.apiUrl}/project-requests`, pendingRequest);
  }

  restPutPendingRequests(pendingRequest: PendingRequest): Observable<PendingRequest> {
    const url = `${environment.apiUrl}/project-requests/` + pendingRequest.id;
    return this.httpClient.put<PendingRequest>(url, pendingRequest);
  }

  restDeletePendingRequests(pendingRequestId: number): Observable<PendingRequest> {
    const url = `${environment.apiUrl}/project-requests/` + pendingRequestId;
    return this.httpClient.delete<PendingRequest>(url);
  }

  restDeleteMultipleRequests(requests: PendingRequest[]): Observable<PendingRequest[]> {
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }),
      body: requests
    };

    return this.httpClient.delete<PendingRequest[]>(`${environment.apiUrl}/project-requests`, options);
  }
}
