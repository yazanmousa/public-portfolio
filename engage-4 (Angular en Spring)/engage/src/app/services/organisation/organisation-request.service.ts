import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from '../../../environments/environment';
import {PendingOrganisationRequest} from '../../models/organisation/pending-organisation-request';

@Injectable({
  providedIn: 'root'
})
export class OrganisationRequestService {
  requests: PendingOrganisationRequest[];
  requestsChanged = new EventEmitter();

  constructor(private httpClient: HttpClient) {
    this.requests = [];
    this.restGetOrganisationRequests().subscribe(response => {
      this.requests = response;
    }, error => {
      console.log(error.message);
    })
  }

  findAll(): PendingOrganisationRequest[] {
    return this.requests;
  }

  findById(id: number): PendingOrganisationRequest {
    for (let i = 0; i < this.requests.length; i++) {
      if (this.requests[i].id === id) {
        return this.requests[i];
      }
    }
  }

  save(request: PendingOrganisationRequest) {
    let returnRequest: PendingOrganisationRequest = null;

    this.restPostOrganisationRequest(request).subscribe(response => {
      this.requests.push(response);
      returnRequest = response;
      this.requestsChanged.emit();
    })
    return returnRequest;
  }

  update(request: PendingOrganisationRequest) {
    this.restPutOrganisationRequest(request).subscribe(response => {
      for (let i = 0; i < this.requests.length; i++) {
        if (response.id === this.requests[i].id) {
          this.requests[i] = response;
          this.requestsChanged.emit();
        }
      }
    })
  }

  deleteById(id: number) {
    this.restDeleteOrganisationRequest(id).subscribe(() => {
      for (let i = 0; i < this.requests.length; i++) {
        if (this.requests[i].id === id) {
          this.requests.splice(i, 1);
          this.requestsChanged.emit();
        }
      }
    })
  }

  deleteMultipleRequests(requests: PendingOrganisationRequest[]) {
    this.restDeleteMultipleRequests(requests).subscribe(response => {
      for (let i = 0; i < requests.length; i++) {
        let index = this.requests.indexOf(requests[i]);
        this.requests.splice(index, 1);
      }
      this.requestsChanged.emit();
    })
  }

  getAllForOrganisation(organisationId: number): PendingOrganisationRequest[] {
    let tempRequests = [];
    for (let i = 0; i < this.requests.length; i++) {
      if (this.requests[i].organisation.id === organisationId) {
        tempRequests.push(this.requests[i]);
      }
    }
    return tempRequests;
  }

  getAllForUser(userId: number): PendingOrganisationRequest[] {
    let tempRequests = [];
    for (let i = 0; i < this.requests.length; i++) {
      if (this.requests[i].sendByUser.id === userId) {
        tempRequests.push(this.requests[i]);
      }
    }
    return tempRequests;
  }

  // back-end http requests
  restGetOrganisationRequests(): Observable<PendingOrganisationRequest[]> {
    return this.httpClient.get<PendingOrganisationRequest[]>(`${environment.apiUrl}/organisation-requests`);
  }

  restPostOrganisationRequest(request: PendingOrganisationRequest): Observable<PendingOrganisationRequest> {
    return this.httpClient.post<PendingOrganisationRequest>(`${environment.apiUrl}/organisation-requests`, request);
  }

  restPutOrganisationRequest(request: PendingOrganisationRequest): Observable<PendingOrganisationRequest> {
    const url = `${environment.apiUrl}/organisation-requests/` + request.id;
    return this.httpClient.put<PendingOrganisationRequest>(url, request);
  }

  restDeleteOrganisationRequest(id: number): Observable<PendingOrganisationRequest> {
    const url = `${environment.apiUrl}/organisation-requests/` + id;
    return this.httpClient.delete<PendingOrganisationRequest>(url);
  }

  restDeleteMultipleRequests(requests: PendingOrganisationRequest[]): Observable<PendingOrganisationRequest[]> {
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }),
      body: requests
    };

    return this.httpClient.delete<PendingOrganisationRequest[]>(`${environment.apiUrl}/organisation-requests`, options)
  }
}
