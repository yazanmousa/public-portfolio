import {Component, OnChanges, OnInit} from '@angular/core';
import {User} from '../../../models/user/user.model';
import {UserService} from '../../../services/user/user.service';
import {ActivatedRoute, Params, Router} from '@angular/router';

@Component({
  selector: 'app-profile-information',
  templateUrl: './profile-information.component.html',
  styleUrls: ['./profile-information.component.css'],
})
export class ProfileInformationComponent implements OnInit {
  user: User;
  isLoggedInUser = false;
  reviewDisplay: boolean = false;
  userHasUploadedPhoto: boolean;



  constructor(
    public userService: UserService,
    private router: Router,
    private route: ActivatedRoute
  ) {
  }

  ngOnInit(): void {

    this.route.params.subscribe(
        (params: Params) => {
          this.user = this.userService.findUserById(+params['id'])
        }
    )

    if (this.user.id === this.userService.loggedInUser.id) {
      this.isLoggedInUser = true;
    } else {
      this.isLoggedInUser = false;
    }

    this.userService.userChanged.subscribe(() => {

      this.route.params.subscribe(
          (params: Params) => {
            this.user = this.userService.findUserById(+params['id'])
          }
      )

    })

    this.userHasUploadedPhoto = this.userService.userHasUploadedPhoto(this.user.id);
    // setTimeout(function(){ alert("Hello"); }, 3000);
    // this.userHasUploadedPhoto = this.userService.userHasUploadedPhoto(this.user.id);
    if (this.userHasUploadedPhoto === true){
      this.userService.getImageForUser(this.user.id);
    }else {


    }

  }

  toEditProfile() {
    this.router.navigate(['profile/edit-information', this.user.id]);
  }

  toReviewProfile(){
    this.reviewDisplay = true;
  }
  // getCorrectPath(path: string) {
  //   path = "assets/images/" + this.user.imagePath.split("\\")[2];
  //   return path;
  // }

  // isFakePath(path: string): boolean {
  //   const pathArray = path.split("\\");
  //   if (pathArray[0] === 'C:') {
  //     return true;
  //   }
  //   return false;
  //
  // }

  reviewDone(done: any) {
    if (done){
      this.reviewDisplay = false;
    }
  }
  ngOnDestroy() {
    this.userService.userHasPhoto = false;
    this.userService.retrievedImage = null;
  }

}
