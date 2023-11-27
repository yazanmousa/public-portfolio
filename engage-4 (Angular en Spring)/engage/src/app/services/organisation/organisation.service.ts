import {Organisation} from '../../models/organisation/organisation';
import {EventEmitter, Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {User} from '../../models/user/user.model';
import {UserService} from "../user/user.service";
import {environment} from "../../../environments/environment";
import {OrganisationMemberService} from './organisation-member.service';

@Injectable({
  providedIn: 'root'
})
export class OrganisationService {
  organisationsChanged = new EventEmitter();
  organisations: Organisation[];

  //photo data
  organisationHasPhoto: boolean;
  selectedFile: File;
  retrievedImage: any;
  base64Data: any;
  retrieveResonse: any;
  message: string;
  imageName: any;

  constructor(private httpClient: HttpClient, private userService: UserService, private organisationMemberService: OrganisationMemberService) {
    this.organisations = [];
    this.restGetOrganisations().subscribe(organisations => {
      this.organisations = organisations;
      this.organisationsChanged.emit();
    }, error => {
      console.log(error.message);
    })
  }

  findAll(): Organisation[] {
    return this.organisations;
  }

  findById(oId: number): Organisation {
    for (let i = 0; i < this.organisations.length; i++) {
      if (this.organisations[i].id === oId) {
        return this.organisations[i];
      }
    }
    return null;
  }

  findByEmail(email: String): Organisation {
    for (let i = 0; i < this.organisations.length; i++) {
      if (this.organisations[i].email === email) {
        return this.organisations[i];
      }
    }
    return null;
  }

  findByUserId(uId: number): Organisation {
    const member = this.organisationMemberService.getMemberForUser(uId);

    if (member !== null) {
      return member.organisation;
    }

    return null;
  }

  /**
   * Takes in an company to be saved and returns the old replaced offer
   * @param organisation
   * @param member The organisationmember that created the organisation
   */

  save(organisation: Organisation) {

    this.restPostOrganisation(organisation).subscribe(responseOrganisation => {
      this.organisations.push(responseOrganisation);
      this.organisationsChanged.emit();
    }, error => {
      console.log(error.message);
    })

  }

  update(organisation: Organisation) {
    this.restPutOrganisation(organisation).subscribe(() => {

      for (let i = 0; i < this.organisations.length; i++) {
        if (organisation.id === this.organisations[i].id) {
          this.organisations[i] = organisation;
          this.organisationsChanged.emit();
        }
      }
    }, error => {
      console.log(error.message);
    })

  }

  deleteById(oId: number) {
    this.restDeleteOrganisation(oId).subscribe(() => {

      for (let i = 0; i < this.organisations.length; i++) {
        if (this.organisations[i].id === oId) {
          this.organisations.splice(i, 1);
          this.organisationsChanged.emit();
        }
      }
    })
  }

  getOwnerForOrganisation(organisationId: number): User {
    let members = this.organisationMemberService.getAllForOrganisation(organisationId);

    for (let i = 0; i < members.length; i++) {
      if (members[i].owner === true) {
        return members[i].user;
      }
    }
    return null;
  }

  restGetOrganisations(): Observable<Organisation[]> {
    return this.httpClient.get<Organisation[]>(`${environment.apiUrl}/organisations`);
  }

  restPostOrganisation(organisation: Organisation): Observable<Organisation> {
    return this.httpClient.post<Organisation>(`${environment.apiUrl}/organisations`, organisation);
  }

  restPutOrganisation(organisation: Organisation): Observable<Organisation> {
    const url = `${environment.apiUrl}/organisations/` + organisation.id;
    return this.httpClient.put<Organisation>(url, organisation);
  }

  restDeleteOrganisation(organisationId: number): Observable<Organisation> {
    const url = `${environment.apiUrl}/organisations/` + organisationId;
    return this.httpClient.delete<Organisation>(url);
  }

  organisationHasUploadedPhoto(organisationId: number) {
    this.httpClient.get('http://localhost:8080/image/get/checkIfOrgansationPhotoExist/' + organisationId )
      .subscribe(
        res => {

          if (res === true){
            this.organisationHasPhoto = true;
            this.getImageForOrganisation(organisationId);
          }else {
            this.organisationHasPhoto = false;
          }


        }
      );

    return false;
  }

  getImageForOrganisation(organisationId: number) {
    this.httpClient.get('http://localhost:8080/image/get/organisationImage/' + organisationId)
      .subscribe(
        res => {
          this.retrieveResonse = res;
          this.base64Data = this.retrieveResonse.picByte;
          this.retrievedImage = 'data:image/jpeg;base64,' + this.base64Data;

          if (this.retrieveResonse.picByte === null){
            this.organisationHasPhoto = false;
          }else {

            this.organisationHasPhoto = true;
          }
          return;
        }
      );
  }
}
