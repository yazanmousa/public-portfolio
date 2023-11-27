import {Component, OnInit} from '@angular/core';
import {FormArray, FormControl, FormGroup, Validators} from '@angular/forms';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {OrganisationService} from '../../../services/organisation/organisation.service';
import {Organisation} from '../../../models/organisation/organisation';
import {UserService} from '../../../services/user/user.service';
import {User} from '../../../models/user/user.model';
import {UserUpdate} from '../../../models/user/user-update';
import {OrganisationMember} from '../../../models/organisation/organisation-member';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {OrganisationMemberService} from '../../../services/organisation/organisation-member.service';
import {UserUpdatesService} from '../../../services/user/user-updates.service';
import {HttpClient} from '@angular/common/http';
import {OrganisationRequestService} from '../../../services/organisation/organisation-request.service';
import {EngagedOrganisationsService} from '../../../services/project/engaged-organisations.service';
import {ProjectMemberService} from '../../../services/project/project-member.service';

@Component({
  selector: 'app-create-company',
  templateUrl: './create-company.component.html',
  styleUrls: ['./create-company.component.css'],
  animations: [
    trigger('showContent', [
      state('in', style({opacity: 0, transform: 'translateY(0)'})),
      transition('void => *', [
        style({opacity: 0, transform: 'translateY(-100px)'}), animate(300)
      ])
    ]),
    trigger('deleteMember', [
      state('in', style({opacity: 0.5, transform: 'translateX(0)'})),
      transition('* => void', [
        animate(400, style({opacity: 0, transform: 'translateX(200px)'}))
      ])
    ])
  ]
})
export class CreateCompanyComponent implements OnInit {
  form: FormGroup;
  editOrganisation: Organisation;
  editOrganisationMembers: OrganisationMember[] = [];
  loggedInUser: User;
  changeRoles = false;
  searchText = '';
  ownerError = false;
  selectedMember: OrganisationMember = null;
  loading: boolean;

  //photo data
  selectedFile: File;
  retrievedImage: any;
  base64Data: any;
  retrieveResonse: any;
  message: string;
  imageName: any;
   chooseFile: boolean;

  constructor(
    private router: Router,
    private organisationService: OrganisationService,
    private organisationMemberService: OrganisationMemberService,
    private organisationRequestsService: OrganisationRequestService,
    private engagedOrganisationService: EngagedOrganisationsService,
    private projectMemberService: ProjectMemberService,
    private userUpdatesService: UserUpdatesService,
    private activatedRoute: ActivatedRoute,
    private userService: UserService,
    private httpClient: HttpClient
  ) {
  }

  ngOnInit(): void {
    this.loggedInUser = this.userService.loggedInUser;

    this.activatedRoute.params.subscribe(
      (params: Params) => {
        this.editOrganisation = this.organisationService.findById(+params['id']);
        if (this.editOrganisation !== null) {
          this.editOrganisationMembers = this.organisationMemberService.getAllForOrganisation(this.editOrganisation.id);
        }
      }
    );

    this.organisationMemberService.membersChanged.subscribe(() => {
      if (this.editOrganisation !== null) {
        this.editOrganisationMembers = this.organisationMemberService.getAllForOrganisation(this.editOrganisation.id);
      }

    })

    this.form = new FormGroup({
      'inputNameOrganisation': new FormControl(null, [Validators.required]),
      'organisationCountry': new FormControl(null, [Validators.required]),
      'description': new FormControl(null, [Validators.required]),
      'email': new FormControl(null, [Validators.required, Validators.email]),
      'photo': new FormControl(null)
    });

    if (this.editOrganisation !== null) {
      this.form.get('inputNameOrganisation').setValue(this.editOrganisation.name);
      this.form.get('organisationCountry').setValue(this.editOrganisation.country);
      this.form.get('description').setValue(this.editOrganisation.description);
      this.form.get('email').setValue(this.editOrganisation.email);

    }

  }

  onSubmit() {
    this.loading = true;



    if (this.editOrganisation === null) {
      let name = this.form.get('inputNameOrganisation').value;
      let email = this.form.get('email').value;
      let about = this.form.get('description').value;
      let photo = this.form.get('photo').value;
      let country = this.form.get('organisationCountry').value;

      let date = new Date();
      date.setMonth(date.getMonth() + 1);

      if (this.emailAlreadyExists(email)) {
        this.loading = false;
        alert("This email has already been used!");
        return;
      }

      let organisation = new Organisation(name, country, email, about, date, photo);
      this.organisationService.save(organisation);



      setTimeout(() => {
        const savedOrganisation = this.organisationService.findByEmail(email);
        alert('the current organisation has id: ' + savedOrganisation.id);

        let member = new OrganisationMember(this.loggedInUser, savedOrganisation, true, true);
        this.organisationMemberService.save(member);

        if (this.chooseFile){
          this.onUpload(savedOrganisation.id);
          this.chooseFile = false;
        }
        // this.onUpload(savedOrganisation.id);
      }, 2000);

      setTimeout(() => {

        const savedOrganisation = this.organisationService.findByEmail(email);

        let update = new UserUpdate(this.loggedInUser,'You have created a new organisation called: ' + '"' + name + '"', Date.now());
        this.userUpdatesService.save(update);

        this.router.navigateByUrl('/RefreshComponent', { skipLocationChange: true }).then(() => {
          this.router.navigate(['profile/my-organisation', savedOrganisation.id]);
        });

        // this.router.navigate(['profile/my-organisation', savedOrganisation.id]);
        this.loading = false;
      }, 4000)

    } else {
      /**
       * this is for updating the company that was subscribed to
       */
      let id = this.editOrganisation.id;
      let name = this.form.get('inputNameOrganisation').value;
      let email = this.form.get('email').value;
      let about = this.form.get('description').value;
      let country = this.form.get('organisationCountry').value;

      if (this.emailAlreadyExists(email) && email !== this.editOrganisation.email) {
        this.loading = false;
        alert("This email has already been used!");
        return;
      }

      /**
       * if there is no photo added in companyEdit then set default picture otherwise set the picture that was added
       */
      var picture: string;
      if (this.form.get('photo').value === null) {
        picture = this.editOrganisation.imagePath;
      } else {
        picture = this.form.get('photo').value;
      }

      let updateCompany = new Organisation(name, country, email, about, this.editOrganisation.dateCreated, picture);
      updateCompany.id = this.editOrganisation.id;

      this.organisationService.update(updateCompany);

      let update = new UserUpdate(this.loggedInUser,'You have edited organisation: ' + '"' + name + '"', Date.now())
      this.userUpdatesService.save(update);

      if (this.chooseFile){
        this.onUpload(id);
        this.chooseFile = false;
      }

      setTimeout(() => {

        this.router.navigateByUrl('/RefreshComponent', { skipLocationChange: true }).then(() => {
          this.router.navigate(['profile/my-organisation', this.editOrganisation.id]);
        });
      }, 2000)

    }
  }

  onClickChangeRoles() {
    this.changeRoles = this.changeRoles === false;
  }

  onClickDone() {
    this.changeRoles = false;
  }

  onClickMember(member: OrganisationMember) {
    for (let i = 0; i < this.editOrganisationMembers.length; i++) {
      if (member.id === this.editOrganisationMembers[i].id) {
        this.editOrganisationMembers[i].administrator = true;
        this.organisationMemberService.updateWithoutEmit(this.editOrganisationMembers[i]);
        let update = new UserUpdate(member.user,'You are now administrator in organisation: ' + this.editOrganisation.name, Date.now())
        this.userUpdatesService.save(update);
      }
    }
    setTimeout(() => {
      this.selectedMember = null;
    }, 5)
  }

  onClickAdministrator(member: OrganisationMember) {
    for (let i = 0; i < this.editOrganisationMembers.length; i++) {
      if (member.id === this.editOrganisationMembers[i].id) {
        if (this.editOrganisationMembers[i].owner) {
          this.ownerError = true;
          setTimeout(() => {
            this.ownerError = false;
          }, 5000)
        } else {
          this.editOrganisationMembers[i].administrator = false;
          this.organisationMemberService.updateWithoutEmit(this.editOrganisationMembers[i]);
          let update = new UserUpdate(member.user,'Your administrator rights have been removed in organisation: ' + this.editOrganisation.name, Date.now())
          this.userUpdatesService.save(update);
          this.selectedMember = null;
        }
      }
    }
    setTimeout(() => {
      this.selectedMember = null;
    }, 5)
  }

  isOwner(): boolean {
    if (this.editOrganisation === null) {
      return false;
    }

    let owner = this.organisationService.getOwnerForOrganisation(this.editOrganisation.id);
    if (owner === null) {
      return false;
    }

    return owner.id === this.loggedInUser.id;
  }

  onClickDismiss() {
    this.ownerError = false;
  }

  onSelectMember(member: OrganisationMember) {
    this.selectedMember = member;
  }

  onClickDeleteMember() {
    this.organisationMemberService.deleteById(this.selectedMember.id);
    this.selectedMember = null;
  }

  onClickCancel() {
    this.selectedMember = null;
  }

  onFileChanged(event) {
    //Select File
    this.selectedFile = event.target.files[0];
    this.chooseFile = true;

  }

  onUpload(organisationId: number) {

    //FormData API provides methods and properties to allow us easily prepare form data to be sent with POST HTTP requests.
    const uploadImageData = new FormData();
    uploadImageData.append('imageFile', this.selectedFile, this.selectedFile.name);

    //Make a call to the Spring Boot Application to save the image
    this.httpClient.post('http://localhost:8080/image/upload/organisation/' +  organisationId, uploadImageData, { observe: 'response' })
      .subscribe((response) => {
          if (response.status === 200) {
            this.message = 'Image uploaded successfully';
          } else {
            this.message = 'Image not uploaded successfully';
          }
        }
      );

  }

  onClickDeleteOrganisation() {
    if (this.isPartOfOneOrMoreProjects(this.loggedInUser.id)) {
      alert("You are still part of one or more projects, so you can not delete your organisation!");
      return;
    }

    if (confirm('Are you sure you want to delete ' + this.editOrganisation.name + '?') == true) {
      this.loading = true;

      const membersCopy = this.editOrganisationMembers;
      this.organisationMemberService.deleteMultipleMembers(this.editOrganisationMembers);

      let pendingRequests = this.organisationRequestsService.getAllForOrganisation(this.editOrganisation.id);
      if (pendingRequests.length >= 1) {
        this.organisationRequestsService.deleteMultipleRequests(pendingRequests);
      }

      let engagedOrganisations = this.engagedOrganisationService.getAllForOrganisation(this.editOrganisation.id);

      if (engagedOrganisations.length >= 1) {
        this.engagedOrganisationService.deleteMultipleEngagedOrganisations(engagedOrganisations);
      }

      let updatesToSave = [];
      for (let i = 0; i < membersCopy.length; i++) {
        if (membersCopy[i].owner === false) {
          let update = new UserUpdate(membersCopy[i].user, "The organisation: " + this.editOrganisation.name + " you were previously part of, has been deleted", Date.now());
          updatesToSave.push(update);
        }
      }
      let ownerUpdate = new UserUpdate(this.loggedInUser, "You have deleted project: " + this.editOrganisation.name, Date.now());

      this.userUpdatesService.saveMultipleUpdates(updatesToSave);
      this.userUpdatesService.save(ownerUpdate);

        this.deleteImage(this.editOrganisation.id);



      setTimeout(() => {
        this.organisationService.deleteById(this.editOrganisation.id);
      }, 1000)


      setTimeout(() => {
        this.loading = false;
        this.router.navigate(['profile/create-organisation-prompt']);
      }, 2000)

    }
  }

  emailAlreadyExists(email: string): boolean {
    let organisations = this.organisationService.findAll();

    for (let i = 0; i < organisations.length; i++) {
      if (organisations[i].email === email) {
        return true;
      }
    }
    return false;
  }

  isPartOfOneOrMoreProjects(userId: number): boolean {
    return this.projectMemberService.getAllForUser(userId).length >= 1;
  }

  deleteImage(id: number){
    this.httpClient.delete('http://localhost:8080/image/organisationImage/' + id).subscribe();

  }

}
