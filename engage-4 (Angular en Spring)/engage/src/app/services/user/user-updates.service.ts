import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from '../../../environments/environment';
import {UserUpdate} from '../../models/user/user-update';
import {UserAttribute} from '../../models/user/user-attribute';
import {UserReview} from '../../models/user/user-review';

@Injectable({
  providedIn: 'root'
})
export class UserUpdatesService {
  updates: UserUpdate[];
  updatesChanged = new EventEmitter();

  constructor(private httpClient: HttpClient) {
    this.updates = [];
    this.restGetUserUpdates().subscribe(response => {
      this.updates = response;
    }, error => {
      console.log(error.message);
    })
  }

  findAll(): UserUpdate[] {
    return this.updates;
  }

  findById(id: number): UserUpdate {
    for (let i = 0; i < this.updates.length; i++) {
      if (this.updates[i].id === id) {
        return this.updates[i];
      }
    }
  }

  save(update: UserUpdate) {

    this.restPostUserUpdate(update).subscribe(response => {
      this.updates.push(response);
      this.updatesChanged.emit();
    })

  }

  saveMultipleUpdates(updates: UserUpdate[]) {

    if (updates.length < 1) {
      return;
    }

    this.restPostMultipleUpdates(updates).subscribe(response => {
      for (let i = 0; i < response.length; i++) {
        this.updates.push(response[i]);
      }
      this.updatesChanged.emit();
    }, error => {
      console.log(error.message);
    })
  }

  update(update: UserUpdate) {
    this.restPutUserUpdate(update).subscribe(response => {
      for (let i = 0; i < this.updates.length; i++) {
        if (response.id === this.updates[i].id) {
          this.updates[i] = response;
          this.updatesChanged.emit();
        }
      }
    })
  }

  deleteById(id: number) {
    this.restDeleteUserUpdate(id).subscribe(() => {
      for (let i = 0; i < this.updates.length; i++) {
        if (this.updates[i].id === id) {
          this.updates.splice(i, 1);
          this.updatesChanged.emit();
        }
      }
    })
  }

  deleteMultipleUpdates(updates: UserUpdate[]) {
    this.restDeleteMultipleUpdates(updates).subscribe(response => {
      for (let i = 0; i < updates.length; i++) {
        let index = this.updates.indexOf(updates[i]);
        this.updates.splice(index, 1);
      }
      this.updatesChanged.emit();
    })
  }

  getAllForUser(userId: number): UserUpdate[] {
    let tempUpdates = [];
    for (let i = 0; i < this.updates.length; i++) {
      if (this.updates[i].user.id === userId) {
        tempUpdates.push(this.updates[i]);
      }
    }
    return tempUpdates;
  }

  restGetUserUpdates(): Observable<UserUpdate[]> {
    return this.httpClient.get<UserUpdate[]>(`${environment.apiUrl}/user-updates`);
  }

  restPostUserUpdate(update: UserUpdate): Observable<UserUpdate> {
    return this.httpClient.post<UserUpdate>(`${environment.apiUrl}/user-updates`, update);
  }

  restPostMultipleUpdates(updates: UserUpdate[]): Observable<UserUpdate[]> {
    return this.httpClient.post<UserUpdate[]>(`${environment.apiUrl}/user-updates/multiple`, updates);
  }

  restPutUserUpdate(update: UserUpdate): Observable<UserUpdate> {
    const url = `${environment.apiUrl}/user-updates/` + update.id;
    return this.httpClient.put<UserUpdate>(url, update);
  }

  restDeleteUserUpdate(id: number): Observable<UserUpdate> {
    const url = `${environment.apiUrl}/user-updates/` + id;
    return this.httpClient.delete<UserUpdate>(url);
  }

  restDeleteMultipleUpdates(updates: UserUpdate[]): Observable<UserUpdate[]> {
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }),
      body: updates
    };

    return this.httpClient.delete<UserUpdate[]>(`${environment.apiUrl}/user-updates`, options);
  }

}
