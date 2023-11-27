import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable, Subject} from 'rxjs';
import {environment} from '../../../environments/environment';
import {UserAttribute} from '../../models/user/user-attribute';
import {UserReviewsService} from './user-reviews.service';

@Injectable({
  providedIn: 'root'
})
export class UserAttributesService {
  userAttributes: UserAttribute[];
  userAttributesChanged = new EventEmitter();
  savedAttributesSubject = new Subject<UserAttribute[]>();

  constructor(private httpClient: HttpClient, private userReviewsService: UserReviewsService) {
    this.userAttributes = [];
    this.restGetUserAttributes().subscribe(response => {
      this.userAttributes = response;
    }, error => {
      console.log(error.message);
    })
  }

  findAll(): UserAttribute[] {
    return this.userAttributes;
  }

  findById(id: number): UserAttribute {
    for (let i = 0; i < this.userAttributes.length; i++) {
      if (this.userAttributes[i].id === id) {
        return this.userAttributes[i];
      }
    }
  }

  save(attribute: UserAttribute) {

    this.restPostUserAttribute(attribute).subscribe(response => {
      this.userAttributes.push(response);
      this.userAttributesChanged.emit();
    })

  }

  saveMultipleAttributes(attributes: UserAttribute[]) {
    this.restPostMultipleAttributes(attributes).subscribe(response => {
      for (let i = 0; i < response.length; i++) {
        let alreadyExists: boolean = false;
        for (let j = 0; j < this.userAttributes.length; j++) {
          if (response[i].id === this.userAttributes[j].id) {
            this.userAttributes[j] = response[i];
            alreadyExists = true;
          }
        }

        if (!alreadyExists) {
          this.userAttributes.push(response[i]);
        }


        this.savedAttributesSubject.next(response);
        this.userAttributesChanged.emit();
      }
    })
  }

  update(attribute: UserAttribute) {
    this.restPutUserAttribute(attribute).subscribe(response => {
      for (let i = 0; i < this.userAttributes.length; i++) {
        if (response.id === this.userAttributes[i].id) {
          this.userAttributes[i] = response;
          this.userAttributesChanged.emit();
        }
      }
    })
  }

  deleteById(id: number) {
    this.restDeleteUserAttribute(id).subscribe(() => {
      for (let i = 0; i < this.userAttributes.length; i++) {
        if (this.userAttributes[i].id === id) {
          this.userAttributes.splice(i, 1);
          this.userAttributesChanged.emit();
        }
      }
    })
  }

  deleteMultipleAttributes(attributes: UserAttribute[]) {
    this.restDeleteMultipleAttributes(attributes).subscribe(response => {
      for (let i = 0; i < attributes.length; i++) {
        let index = this.userAttributes.indexOf(attributes[i]);
        this.userAttributes.splice(index, 1);
      }
      this.userAttributesChanged.emit();
    })
  }

  getAllForUser(userId: number): UserAttribute[] {
    let tempAttributes = [];
    for (let i = 0; i < this.userAttributes.length; i++) {
      if (this.userAttributes[i].user.id === userId) {
        tempAttributes.push(this.userAttributes[i]);
      }
    }
    return tempAttributes;
  }

  getAttributeForUser(userId: number, attribute: string): UserAttribute {
    for (let i = 0; i < this.userAttributes.length; i++) {
      if (this.userAttributes[i].user.id === userId && this.userAttributes[i].attribute === attribute) {
        return this.userAttributes[i];
      }
    }
    return null;
  }

  /**
   * Removes all the attributes that have 0 reviews, belonging to specified user.
   * @param userId of the user of whom the attributes need to be checked.
   */
  removeAttributesWithoutReviews(userId: number) {
    const attributes = this.getAllForUser(userId);
    const reviews = this.userReviewsService.getAllForUser(userId);
    let attributesToRemove = [];

    for (let i = 0; i < attributes.length; i++) {
      let reviewCount = 0;
      for (let j = 0; j < reviews.length; j++) {
        if (reviews[j].evaluated.id === attributes[i].id) {
          reviewCount++;
        }
      }

      if (reviewCount === 0) {
        attributesToRemove.push(attributes[i]);
      }

    }

    if (attributesToRemove.length >= 1) {
      this.deleteMultipleAttributes(attributesToRemove);
    }
  }

  // Will update all the average ratings for all attributes belonging to one user.
  updateAveragesForUser(userId: number) {
    let attributes = this.getAllForUser(userId);
    let updatedAttributes: UserAttribute[] = [];

    for (let i = 0; i < attributes.length; i++) {
      let reviews = this.userReviewsService.getAllForAttribute(attributes[i].id);
      let total = 0;
      for (let j = 0; j < reviews.length; j++) {
        total += reviews[j].rating;
      }

      if (total !== null) {
        attributes[i].average = total / reviews.length;
        updatedAttributes.push(attributes[i]);
      }

    }

    for (let i = 0; i < updatedAttributes.length; i++) {
      let index = this.userAttributes.indexOf(updatedAttributes[i]);
       this.userAttributes[index] = updatedAttributes[i];
    }

    this.restPostMultipleAttributes(updatedAttributes).subscribe(response => {

    }, error => {
      console.log(error.message);
    })

  }


  restGetUserAttributes(): Observable<UserAttribute[]> {
    return this.httpClient.get<UserAttribute[]>(`${environment.apiUrl}/user-attributes`);
  }

  restPostUserAttribute(attribute: UserAttribute): Observable<UserAttribute> {
    return this.httpClient.post<UserAttribute>(`${environment.apiUrl}/user-attributes`, attribute);
  }

  restPostMultipleAttributes(attributes: UserAttribute[]): Observable<UserAttribute[]> {
    return this.httpClient.post<UserAttribute[]>(`${environment.apiUrl}/user-attributes/multiple`, attributes);
  }

  restPutUserAttribute(attribute: UserAttribute): Observable<UserAttribute> {
    const url = `${environment.apiUrl}/user-attributes/` + attribute.id;
    return this.httpClient.put<UserAttribute>(url, attribute);
  }

  restDeleteUserAttribute(id: number): Observable<UserAttribute> {
    const url = `${environment.apiUrl}/user-attributes/` + id;
    return this.httpClient.delete<UserAttribute>(url);
  }

  restDeleteMultipleAttributes(attributes: UserAttribute[]): Observable<UserAttribute[]> {
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }),
      body: attributes
    };

    return this.httpClient.delete<UserAttribute[]>(`${environment.apiUrl}/user-attributes`, options)

  }

}
