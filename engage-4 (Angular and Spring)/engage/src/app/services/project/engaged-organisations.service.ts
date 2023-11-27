import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from "rxjs";
import {environment} from "../../../environments/environment";
import {EngagedOrganisation} from "../../models/project/engaged-organisation";

@Injectable({
  providedIn: 'root'
})
export class EngagedOrganisationsService {
  engagedOrganisations: EngagedOrganisation[];
  engagedOrganisationsChanged = new EventEmitter();

  constructor(private httpClient: HttpClient) {
    this.engagedOrganisations = [];
    this.restGetEngagedOrganisations().subscribe(response => {
      this.engagedOrganisations = response;
    }, error => {
      console.log(error.message);
    })
  }

  findAll(): EngagedOrganisation[] {
    return this.engagedOrganisations;
  }

  findById(id: number): EngagedOrganisation {
    for (let i = 0; i < this.engagedOrganisations.length; i++) {
      if (this.engagedOrganisations[i].id === id) {
        return this.engagedOrganisations[i];
      }
    }
  }

  save(engagedOrganisation: EngagedOrganisation) {

    this.restPostEngagedOrganisations(engagedOrganisation).subscribe(response => {
      let isAlreadyInList: boolean = false;


      for (let i = 0; i < this.engagedOrganisations.length; i++) {
        if (response.id === this.engagedOrganisations[i].id) {
          isAlreadyInList = true;
        }
      }

      if (!isAlreadyInList) {
        this.engagedOrganisations.push(response);
      }

      this.engagedOrganisationsChanged.emit();
    })

  }

  saveMultipleEngagedOrganisations(engagedOrganisations: EngagedOrganisation[]) {
    this.restPostMultipleEngagedOrganisations(engagedOrganisations).subscribe(response => {
      for (let i = 0; i < response.length; i++) {
        let alreadyExists: boolean = false;
        for (let j = 0; j < this.engagedOrganisations.length; j++) {
          if (response[i].id === this.engagedOrganisations[j].id) {
            alreadyExists = true;
          }
        }

        if (!alreadyExists) {
          this.engagedOrganisations.push(response[i]);
        }

      }
      this.engagedOrganisationsChanged.emit();
    })
  }

  update(engagedOrganisation: EngagedOrganisation) {
    this.restPutEngagedOrganisations(engagedOrganisation).subscribe(response => {
      for (let i = 0; i < this.engagedOrganisations.length; i++) {
        if (response.id === this.engagedOrganisations[i].id) {
          this.engagedOrganisations[i] = response;
          this.engagedOrganisationsChanged.emit();
        }
      }
    })
  }

  deleteById(id: number) {
    this.restDeleteEngagedOrganisations(id).subscribe(() => {
      for (let i = 0; i < this.engagedOrganisations.length; i++) {
        if (this.engagedOrganisations[i].id === id) {
          this.engagedOrganisations.splice(i, 1);
          this.engagedOrganisationsChanged.emit();
        }
      }
    })
  }

  deleteMultipleEngagedOrganisations(engagedOrganisations: EngagedOrganisation[]) {
    this.restDeleteMultipleEngagedOrganisations(engagedOrganisations).subscribe(response => {
      for (let i = 0; i < engagedOrganisations.length; i++) {
        let index = this.engagedOrganisations.indexOf(engagedOrganisations[i]);
        this.engagedOrganisations.splice(index, 1);
      }
      this.engagedOrganisationsChanged.emit();
    })
  }

  getAllForProject(projectId: number): EngagedOrganisation[] {
    let tempEngagedOrganisations = [];
    for (let i = 0; i < this.engagedOrganisations.length; i++) {
      if (this.engagedOrganisations[i].project.id === projectId) {
        tempEngagedOrganisations.push(this.engagedOrganisations[i]);
      }
    }
    return tempEngagedOrganisations;
  }

  getAllForOrganisation(organisationId: number): EngagedOrganisation[] {
    let tempEngagedOrganisations = [];
    for (let i = 0; i < this.engagedOrganisations.length; i++) {
      if (this.engagedOrganisations[i].organisation.id === organisationId) {
        tempEngagedOrganisations.push(this.engagedOrganisations[i]);
      }
    }
    return tempEngagedOrganisations;
  }

  // back-end http requests
  restGetEngagedOrganisations(): Observable<EngagedOrganisation[]> {
    return this.httpClient.get<EngagedOrganisation[]>(`${environment.apiUrl}/engaged-organisations`);
  }

  restPostEngagedOrganisations(member: EngagedOrganisation): Observable<EngagedOrganisation> {
    return this.httpClient.post<EngagedOrganisation>(`${environment.apiUrl}/engaged-organisations`, member);
  }

  restPostMultipleEngagedOrganisations(engagedOrganisations: EngagedOrganisation[]): Observable<EngagedOrganisation[]> {
    return this.httpClient.post<EngagedOrganisation[]>(`${environment.apiUrl}/engaged-organisations/multiple`, engagedOrganisations);
  }

  restPutEngagedOrganisations(member: EngagedOrganisation): Observable<EngagedOrganisation> {
    const url = `${environment.apiUrl}/engaged-organisations/` + member.id;
    return this.httpClient.put<EngagedOrganisation>(url, member);
  }

  restDeleteEngagedOrganisations(engagedOrganisationId: number): Observable<EngagedOrganisation> {
    const url = `${environment.apiUrl}/engaged-organisations/` + engagedOrganisationId;
    return this.httpClient.delete<EngagedOrganisation>(url);
  }

  restDeleteMultipleEngagedOrganisations(engagedOrganisations: EngagedOrganisation[]): Observable<EngagedOrganisation[]> {
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }),
      body: engagedOrganisations
    };

    return this.httpClient.delete<EngagedOrganisation[]>(`${environment.apiUrl}/engaged-organisations`, options);
  }
}
