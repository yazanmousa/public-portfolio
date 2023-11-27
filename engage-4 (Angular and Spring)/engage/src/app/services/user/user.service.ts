import {EventEmitter, Injectable} from '@angular/core';
import {User} from '../../models/user/user.model';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {environment} from "../../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class UserService {
  userChanged = new EventEmitter<User>();
  users: User[];
  loggedInUser: User = null;

  selectedFile: File;
  retrievedImage: any;
  base64Data: any;
  retrieveResonse: any;
  message: string;
  imageName: any;
  userHasPhoto: boolean;
  chooseFile: boolean;

  constructor(private httpClient: HttpClient) {
    this.users = [];

    this.restGetUsers().subscribe(users => {
      this.users = users;
      this.userChanged.emit();
    }, error => {
      console.log(error.message);
    })
  }

  add(user: User): User {
    let returnUser: User = null;

    this.restPostUser(user).subscribe(response => {
      this.users.push(response);
      returnUser = response;
      this.userChanged.emit();
    })
    return returnUser;
  }

  findAll(): User[] {
    return this.users.slice();
  }

  findUserById(uId: number): User {
    for (let i = 0; i < this.users.length; i++) {
      if (this.users[i].id === uId) {
        return this.users[i];
      }
    }
    return null;
  }

  update(user: User): boolean {
    this.restPutUser(user).subscribe(() => {

      for (let i = 0; i < this.users.length; i++) {
        if (user.id === this.users[i].id) {
          this.users[i] = user;
          this.userChanged.emit();
          return true;
        }
      }

    })
    return false
  }

  deleteById(uId: number): void {
    this.restDeleteUser(uId).subscribe(() => {

      for (let i = 0; i < this.users.length; i++) {
        if (this.users[i].id === uId) {
          this.users.splice(i, 1);
          this.userChanged.emit();
        }
      }
    })
  }

  getByEmailAndPassword(email: string, password: string): User {
    for (let i = 0; i < this.users.length; i++) {
      if (this.users[i].email === email && this.users[i].password === password) {
        return this.users[i];
      }
    }
    return null;
  }

  loginUser(user: User): boolean {
    for (let i = 0; i < this.users.length; i++) {
      if (user.email === this.users[i].email && user.password === this.users[i].password) {
        this.loggedInUser = user;
        return true;
      }
    }
    return false;
  }

  signOutUser() {
    this.loggedInUser = null;
  }

  private restGetUsers(): Observable<User[]> {
    return this.httpClient.get<User[]>(`${environment.apiUrl}/users`);
  }

  private restPostUser(user: User): Observable<User> {


    return this.httpClient.post<User>(`${environment.apiUrl}/users`, user);
  }

  private restPutUser(user: User): Observable<User> {
    const url = `${environment.apiUrl}/users/` + user.id;
    return this.httpClient.put<User>(url, user);
  }

  private restDeleteUser(userId: number) {
    const url = `${environment.apiUrl}/users/` + userId;
    return this.httpClient.delete(url);
  }

  getImageForUser(userID: number) {
    //Make a call to Sprinf Boot to get the Image Bytes.
    this.httpClient.get('http://localhost:8080/image/get/' + userID)
      .subscribe(
        res => {
          this.retrieveResonse = res;
          this.base64Data = this.retrieveResonse.picByte;
          this.retrievedImage = 'data:image/jpeg;base64,' + this.base64Data;

          if (this.retrieveResonse.picByte === null){
            this.userHasPhoto = false;
          }else {

            this.userHasPhoto = true;
          }
          return;
        }
      );
  }

  userHasUploadedPhoto(userId: number): boolean{
    // console.log("userHasUploadedPhoto");
    // this.getImageForUser(userId);
    // return this.userHasPhoto;

    this.httpClient.get('http://localhost:8080/image/get/checkIfPhotoExist/' + userId )
      .subscribe(
        res => {

          if (res === true){
            this.userHasPhoto = true;
            this.getImageForUser(userId);
          }else {
            this.userHasPhoto = false;
          }


        }
      );

    return false;

  }


}
