import {Component, OnInit} from '@angular/core';
import {UserService} from '../../../services/user/user.service';
import {User} from '../../../models/user/user.model';
import {Router} from "@angular/router";
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {ProjectsService} from "../../../services/project/projects.service";
import {OrganisationService} from "../../../services/organisation/organisation.service";
import {HttpClient} from '@angular/common/http';
import {OrganisationMemberService} from '../../../services/organisation/organisation-member.service';
import {ProjectMemberService} from '../../../services/project/project-member.service';
import {UserAttributesService} from '../../../services/user/user-attributes.service';
import {UserReviewsService} from '../../../services/user/user-reviews.service';
import {UserUpdatesService} from '../../../services/user/user-updates.service';
import {OrganisationRequestService} from '../../../services/organisation/organisation-request.service';
import {ProjectRequestsService} from '../../../services/project/project-requests.service';
import {ProjectInviteService} from '../../../services/project/project-invite-service';


@Component({
  selector: 'app-profile-edit',
  templateUrl: './profile-edit.component.html',
  styleUrls: ['./profile-edit.component.css']
})
export class ProfileEditComponent implements OnInit {
  form: FormGroup;
  profileToEdit: User;
  errorText = '';
  error: boolean = false;
  selectedFile: File;
  retrievedImage: any;
  base64Data: any;
  retrieveResonse: any;
  message: string;
  imageName: any;
  loading: boolean = false;

  constructor(private userService: UserService,
              private router: Router,
              private projectService: ProjectsService,
              private organisationService: OrganisationService,
              private organisationMemberService: OrganisationMemberService,
              private projectMemberService: ProjectMemberService,
              private userAttributesService: UserAttributesService,
              private userReviewsService: UserReviewsService,
              private userUpdatesService: UserUpdatesService,
              private organisationRequestsService: OrganisationRequestService,
              private projectRequestsService: ProjectRequestsService,
              private inviteRequestService: ProjectInviteService,
              private httpClient: HttpClient
  ) {}

  ngOnInit(): void {
    this.profileToEdit = this.userService.loggedInUser;

    this.userService.userChanged.subscribe(() => {
      this.profileToEdit = this.userService.loggedInUser;

    })

    this.form = new FormGroup({
        'firstName': new FormControl(null, [Validators.required]),
        'lastName': new FormControl(null, [Validators.required]),
        'dateOfBirth': new FormControl(null, [Validators.required]),
        'country': new FormControl(null, [Validators.required]),
        'aboutMe': new FormControl(null,),
        'email': new FormControl(null, [Validators.required, Validators.email]),
        'photo': new FormControl(null),
        // 'attributes': new FormArray([]),
        'oldPassword': new FormControl(null),
        'newPassword': new FormControl(null),
        'repeatPassword': new FormControl(null)
      },
    );

    this.form.get('firstName').setValue(this.profileToEdit.firstName);
    this.form.get('lastName').setValue(this.profileToEdit.lastName);
    this.form.get('dateOfBirth').setValue(this.profileToEdit.birthDate);
    this.form.get('country').setValue(this.profileToEdit.country);
    this.form.get('aboutMe').setValue(this.profileToEdit.description);
    this.form.get('email').setValue(this.profileToEdit.email);

    console.log("User id: " + this.userService.loggedInUser.id);
  }

  onSubmit() {
    this.loading = true;

    const firstName = this.form.get('firstName').value;
    const lastName = this.form.get('lastName').value;
    const dateOfBirth = this.form.get('dateOfBirth').value;
    const country = this.form.get('country').value;
    const aboutMe = this.form.get('aboutMe').value;
    const email = this.form.get('email').value;
    const oldPassword = this.form.get('oldPassword').value
    const newPassword = this.form.get('newPassword').value;
    const repeatPassword = this.form.get('repeatPassword').value;
    var picture: string;
    if (this.form.get('photo').value === null) {
      picture = this.profileToEdit.imagePath;
    } else {
      picture = this.form.get('photo').value;
    }

    if (this.emailAlreadyExists(email) && email !== this.profileToEdit.email) {
      this.loading = false;
      alert("This email has already been used!");
      return;
    }

    if (oldPassword === this.profileToEdit.password && newPassword === repeatPassword) {

      if (newPassword.length < 8) {
        alert("Password should be at least 8 characters.");
        return;
      }

      const updateProfile = new User(firstName, lastName, email, newPassword, dateOfBirth, country, aboutMe, picture);
      updateProfile.id = this.profileToEdit.id;
      this.userService.update(updateProfile);
      this.userService.loggedInUser = updateProfile;

      setTimeout(() => {
        this.onUpload();
        this.loading = false;
        // this.router.navigate(['profile/my-information', updateProfile.id])
      }, 1000)
      setTimeout(() => {
        this.router.navigateByUrl('/RefreshComponent', { skipLocationChange: true }).then(() => {
          this.router.navigate(['profile/my-information', this.profileToEdit.id])
        });
      }, 3000)

    } else if (oldPassword === null && newPassword === null && repeatPassword === null) {
      const updateProfile = new User(firstName, lastName, email, this.profileToEdit.password, dateOfBirth, country, aboutMe, picture);
      updateProfile.id = this.profileToEdit.id;
      this.userService.update(updateProfile);
      this.userService.loggedInUser = updateProfile;

      setTimeout(() => {
        this.onUpload();
        this.loading = false;
        // this.router.navigate(['profile/my-information', updateProfile.id])
      }, 1000)
      setTimeout(() => {
        this.router.navigateByUrl('/RefreshComponent', { skipLocationChange: true }).then(() => {
          this.router.navigate(['profile/my-information', this.profileToEdit.id])
        });
      }, 3000)

    } else {
      this.errorText = 'Passwords dont match';
      alert(this.errorText)
      this.error = true;
    }






  }


  /**
   * DONT FORGET TO TEST THIS METHOD. A LOT OF UNCERTAINTIES PRESENT HERE
   */
  onDeleteAccount() {
    if (confirm('Are you sure you want to delete your account?') == true) {
      this.loading = true;

      if (this.isOrganisationOwner(this.profileToEdit.id) || this.isProjectOwner(this.profileToEdit.id)) {
        alert("You are still the owner in a project or an organisation. Delete the project/organisation first before deleting your profile");
        this.loading = false;
        return;
      }

      setTimeout(() => {
          this.deleteProfileImage(this.profileToEdit.id);
      }, 1000)

      // creating an array of all the attributes that will need to be deleted
      const attributesToDelete = this.userAttributesService.getAllForUser(this.profileToEdit.id);

      // creating an array that will hold all reviews that need to be deleted in the end
      let reviewsToDelete = [];

      // looping through all the attributes that belong to the user to be deleted
      for (let i = 0; i < attributesToDelete.length; i++) {

        // get all reviews that are connected to the current iteration of the loop
        let reviews = this.userReviewsService.getAllForAttribute(attributesToDelete[i].id);

        // loop through those reviews and add them to the list of reviews to be deleted
        for (let j = 0; j < reviews.length; j++) {
          reviewsToDelete.push(reviews[j]);
        }

      }

      //deleting all reviews and attributes
      if (reviewsToDelete.length >= 1) {
        this.userReviewsService.deleteMultipleReviews(reviewsToDelete);
      }

      // deleting all the latest updates for this user
      const updatesToDelete = this.userUpdatesService.getAllForUser(this.profileToEdit.id);

      if (updatesToDelete.length >= 1) {
        this.userUpdatesService.deleteMultipleUpdates(updatesToDelete);
      }

      // deleting the organisationMember object connected to this user
      const organisationMember = this.organisationMemberService.getMemberForUser(this.profileToEdit.id);

      if (organisationMember !== null) {
        this.organisationMemberService.deleteById(organisationMember.id);
      }

      // deleting all the organisation join requests for this user
      const oRequestsToDelete = this.organisationRequestsService.getAllForUser(this.profileToEdit.id);

      if (oRequestsToDelete.length >= 1) {
        this.organisationRequestsService.deleteMultipleRequests(oRequestsToDelete);
      }

      // deleting all the projectMembers connected to this user
      const projectMembers = this.projectMemberService.getAllForUser(this.profileToEdit.id);

      if (projectMembers.length >= 1) {
        this.projectMemberService.deleteMultipleMembers(projectMembers);
      }

      // deleting all the project join requests for this user
      const pRequestsToDelete = this.projectRequestsService.getAllForUser(this.profileToEdit.id);

      if (pRequestsToDelete.length >= 1) {
        this.projectRequestsService.deleteMultipleRequests(pRequestsToDelete);
      }





      setTimeout(() => {
        if (attributesToDelete.length >= 1) {
          this.userAttributesService.deleteMultipleAttributes(attributesToDelete);
        }

      }, 1000)

      setTimeout(() => {
        // Deleting the user itself
        this.userService.deleteById(this.profileToEdit.id);
        this.loading = false;
        this.userService.signOutUser();
        this.router.navigate(['/home']);
      }, 2000)

    }
  }

  onFileChanged(event) {
    //Select File
    this.selectedFile = event.target.files[0];

  }

  onUpload() {
    console.log(this.selectedFile);
    if (this.selectedFile === null) return;

    //FormData API provides methods and properties to allow us easily prepare form data to be sent with POST HTTP requests.
    const uploadImageData = new FormData();
    uploadImageData.append('imageFile', this.selectedFile, this.selectedFile.name);

    //Make a call to the Spring Boot Application to save the image
    this.httpClient.post('http://localhost:8080/image/upload/' +  this.userService.loggedInUser.id, uploadImageData, { observe: 'response' })
      .subscribe((response) => {
          if (response.status === 200) {
            this.message = 'Image uploaded successfully';
          } else {
            this.message = 'Image not uploaded successfully';
          }
        }
      );


  }

  getImageForUser() {
    //Make a call to Sprinf Boot to get the Image Bytes.
    this.httpClient.get('http://localhost:8080/image/get/' + this.userService.loggedInUser.id)
      .subscribe(
        res => {
          this.retrieveResonse = res;
          this.base64Data = this.retrieveResonse.picByte;
          this.retrievedImage = 'data:image/jpeg;base64,' + this.base64Data;
        }
      );
  }

  emailAlreadyExists(email: string): boolean {
    let users = this.userService.findAll();

    for (let i = 0; i < users.length; i++) {
      if (users[i].email === email) {
        return true;
      }
    }
    return false;
  }

  isOrganisationOwner(userId: number): boolean {
    let organisationMember = this.organisationMemberService.getMemberForUser(userId);
    if (organisationMember !== null) {
      return organisationMember.owner
    }
    return false;
  }

  isProjectOwner(userId: number): boolean {
    let projectMembers = this.projectMemberService.getAllForUser(userId);
    if (projectMembers.length >= 1) {
      for (let member of projectMembers) {
        if (member.owner) {
          return true;
        }
      }
      return false;
    }
    return false;
  }

  deleteProfileImage(id: number){
    this.httpClient.delete('http://localhost:8080/image/userImage/' + id).subscribe();
  }

  ngOnDestroy() {
   this.userService.userHasPhoto= false;
   this.userService.retrievedImage = null;
  }

}
