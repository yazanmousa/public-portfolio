import {Component, OnInit} from '@angular/core';
import {FormArray, FormControl, FormGroup, Validators} from '@angular/forms';
import {ProjectsService} from '../../../services/project/projects.service';
import {Project} from '../../../models/project/project';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {UserService} from '../../../services/user/user.service';
import {OrganisationService} from "../../../services/organisation/organisation.service";
import {Organisation} from "../../../models/organisation/organisation";
import {EngagedOrganisation} from '../../../models/project/engaged-organisation';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {ProjectMember} from '../../../models/project/project-member';
import {User} from "../../../models/user/user.model";
import {UserUpdate} from '../../../models/user/user-update';
import {ProjectRolesEnum} from '../../../models/project/project-roles-enum';
import {CategoryEnum} from '../../../models/project/category-enum';
import {UserUpdatesService} from '../../../services/user/user-updates.service';
import {ProjectMemberService} from '../../../services/project/project-member.service';
import {EngagedOrganisationsService} from '../../../services/project/engaged-organisations.service';
import {ProjectRequestsService} from '../../../services/project/project-requests.service';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-create-project',
  templateUrl: './create-project.component.html',
  styleUrls: ['./create-project.component.css'],
  animations: [
    trigger('showContent', [
      state('in', style({opacity: 0, transform: 'translateY(0)'})),
      transition('void => *', [
        style({opacity: 0, transform: 'translateY(-100px)'}), animate(300)
      ])
    ]),
    trigger('delete', [
      state('in', style({opacity: 0.5, transform: 'translateX(0)'})),
      transition('* => void', [
        animate(400, style({opacity: 0, transform: 'translateX(200px)'}))
      ])
    ])
  ]
})
export class CreateProjectComponent implements OnInit {
  form: FormGroup;
  organisationForm: FormGroup;
  roleForm: FormGroup;
  projectToEdit: Project = null;
  projectToEditMembers: ProjectMember[] = [];
  organisations: Organisation[] = [];
  engagedOrganisations: EngagedOrganisation[] = [];
  selectedEngagedOrganisation: EngagedOrganisation = null;
  selectedNewOrganisation: Organisation = null;
  selectedMember: ProjectMember = null;
  addEngagedOrganisation = false;
  organisationWindowOpened = false;
  searchText = '';
  loggedInUser: User;
  editMembers = false;
  projectOwner: User;
  categoriesEnum: string[] = Object.values(CategoryEnum);
  selectedCategory: string = '';
  savedProject: Project = null;
  loading: boolean = false;
  engagedOrganisationsCopy: EngagedOrganisation[] = [];
  engagedOrganisationsToDelete: EngagedOrganisation[] = [];

  //photo data
  selectedFile: File;
  retrievedImage: any;
  base64Data: any;
  retrieveResonse: any;
  message: string;
  imageName: any;
  chooseFile: boolean;

  constructor(
    private projectsService: ProjectsService,
    private organisationService: OrganisationService,
    private projectMemberService: ProjectMemberService,
    private userUpdatesService: UserUpdatesService,
    private engagedOrganisationService: EngagedOrganisationsService,
    private projectRequestsService: ProjectRequestsService,
    private router: Router,
    private route: ActivatedRoute,
    private userService: UserService,
    private httpClient: HttpClient

  ) {
  }

  ngOnInit(): void {
    this.loggedInUser = this.userService.loggedInUser;

    this.route.params.subscribe(
        (params: Params) => {
          this.projectToEdit = this.projectsService.findById(+params['id']);

          if (this.projectToEdit !== null) {
            this.engagedOrganisations = this.engagedOrganisationService.getAllForProject(this.projectToEdit.id);
            this.engagedOrganisationsCopy = this.engagedOrganisations;
            this.projectToEditMembers = this.projectMemberService.getAllForProject(this.projectToEdit.id);
          }
        });

    this.organisations = this.organisationService.findAll();
    if (this.projectToEdit !== null) {
      this.projectOwner = this.projectsService.getProjectOwner(this.projectToEdit);
    }

    this.organisationService.organisationsChanged.subscribe(
        () => {
          this.organisations = this.organisationService.findAll();
        }
    );

    this.engagedOrganisationService.engagedOrganisationsChanged.subscribe(() => {
      if (this.projectToEdit !== null) {
        this.engagedOrganisations = this.engagedOrganisationService.getAllForProject(this.projectToEdit.id);
      }
    });

    this.projectMemberService.membersChanged.subscribe(() => {
      if (this.projectToEdit !== null) {
        this.projectToEditMembers = this.projectMemberService.getAllForProject(this.projectToEdit.id);
      }

    })

    this.projectsService.savedProjectSubject.subscribe(project => {
      this.savedProject = project;
    })


    this.form = new FormGroup({
      'inputName': new FormControl(null, [Validators.required]),
      'country': new FormControl(null, [Validators.required]),
      'description': new FormControl(null, [Validators.required]),
      'picture': new FormControl(null),
      'membersRequired': new FormControl(null, [Validators.required]),
      'organisationInvolved': new FormArray([])
    })

    this.organisationForm = new FormGroup({
      'engagementLevel': new FormControl(null, [Validators.required]),
    })

    this.roleForm = new FormGroup({
      'role': new FormControl(null)
    })

    if (this.projectToEdit !== null) {
      this.form.get('inputName').setValue(this.projectToEdit.name)
      this.form.get('country').setValue(this.projectToEdit.country)
      this.form.get('description').setValue(this.projectToEdit.description)
      this.form.get('membersRequired').setValue(this.projectToEdit.requiredParticipants)
    }

  }

  onSubmit() {
    this.loading = true;

    if (this.projectToEdit === null) {

      const projectName = this.form.get('inputName').value;
      const country = this.form.get('country').value;
      const description = this.form.get('description').value;
      const picture = this.form.get('picture').value;
      const membersRequired = this.form.get('membersRequired').value;

      if(membersRequired < 0){
        alert("You cannot have a negative value for required members!");
        return;
      }else {

        let date = new Date();
        date.setMonth(date.getMonth() + 1);

        let project = new Project(projectName, description, country, membersRequired, picture, date);
        this.projectsService.save(project);


        setTimeout(() => {
          let projectMember = new ProjectMember(this.savedProject, this.loggedInUser, true, ProjectRolesEnum.Project_Manager);
          this.projectMemberService.save(projectMember);
          console.log(this.savedProject.id);
          if (this.chooseFile){
            this.onUpload(this.savedProject.id);
            this.chooseFile = false;
          }

          // Make sure the project including the ID is added to the engagedOrganisations.
          for (let i = 0; i < this.engagedOrganisations.length; i++) {
            this.engagedOrganisations[i].project = this.savedProject;
          }

          if (this.engagedOrganisations.length >= 1) {
            this.engagedOrganisationService.saveMultipleEngagedOrganisations(this.engagedOrganisations);
          }

          if (this.engagedOrganisationsToDelete.length >= 1) {
            this.engagedOrganisationService.deleteMultipleEngagedOrganisations(this.engagedOrganisationsToDelete);
          }


          let update = new UserUpdate(this.loggedInUser,'You have created a new project called: ' + '"' + projectName + '"', Date.now())
          this.userUpdatesService.save(update);
        },1000)


        setTimeout(() => {
          this.loading = false;
          this.savedProject = null;
          this.router.navigate(['profile/my-projects', this.loggedInUser.id]);
        }, 2000);

      }

    } else {
      const projectName = this.form.get('inputName').value;
      const membersRequired = this.form.get('membersRequired').value;
      const country = this.form.get('country').value;
      const description = this.form.get('description').value;

      if (membersRequired < 0) {
        alert("You cannot have a negative value for required members!");
        return;
      } else {

        var picture: string;
        if (this.form.get('picture').value === null) {
          picture = this.projectToEdit.imageSource;
        } else {
          picture = this.form.get('picture').value;
        }

        let updateProject = new Project(projectName, description, country, membersRequired, picture, this.projectToEdit.dateCreated);
        updateProject.id = this.projectToEdit.id;
        this.projectsService.update(updateProject);


        if (this.engagedOrganisationsToDelete.length >= 1) {
          this.engagedOrganisationService.deleteMultipleEngagedOrganisations(this.engagedOrganisationsToDelete);
        }
        if (this.chooseFile){
          this.onUpload(this.projectToEdit.id);
          this.chooseFile = false;
        }

        setTimeout(() => {

          for (let i = 0; i < this.engagedOrganisations.length; i++) {
            this.engagedOrganisations[i].project = updateProject;
          }

          if (this.engagedOrganisations.length >= 1) {
            this.engagedOrganisationService.saveMultipleEngagedOrganisations(this.engagedOrganisations);
          }

          let update = new UserUpdate(this.loggedInUser,'You have edited project: ' + '"' + projectName + '"', Date.now());
          this.userUpdatesService.save(update);

        }, 1000)


        setTimeout(() => {

          this.loading = false;
          this.router.navigate(['/profile/my-project', updateProject.id]);
        }, 2000);

      }
    }

  }

  deleteProject() {
    if (confirm('Are you sure you want to delete ' + this.projectToEdit.name + '?') == true) {
      this.loading = true;

      const membersCopy = this.projectToEditMembers;
      this.projectMemberService.deleteMultipleMembers(this.projectToEditMembers);

      let pendingRequests = this.projectRequestsService.getAllForProject(this.projectToEdit.id);
      if (pendingRequests.length >= 1) {
        this.projectRequestsService.deleteMultipleRequests(pendingRequests);
      }

      let engagedOrganisations = this.engagedOrganisationService.getAllForProject(this.projectToEdit.id);
      if (engagedOrganisations.length >= 1) {
        this.engagedOrganisationService.deleteMultipleEngagedOrganisations(this.engagedOrganisations);
      }

      let updatesToSave = [];
      for (let i = 0; i < membersCopy.length; i++) {
        if (membersCopy[i].owner === false) {
          let update = new UserUpdate(membersCopy[i].user, "The project: " + this.projectToEdit.name + " you were previously part of, has been deleted", Date.now());
          updatesToSave.push(update);
        }
      }
      let ownerUpdate = new UserUpdate(this.loggedInUser, "You have deleted project: " + this.projectToEdit.name, Date.now());

      this.userUpdatesService.saveMultipleUpdates(updatesToSave);
      this.userUpdatesService.save(ownerUpdate);

        this.deleteImage(this.projectToEdit.id);




      // All data connected to projects needs to be deleted first, that's why deleting the project will be delayed a little bit
      setTimeout(() => {
        this.projectsService.deleteById(this.projectToEdit.id);
      }, 1000)

      setTimeout(() => {
        this.loading = false;
        this.router.navigate(['/profile/my-projects/', this.loggedInUser.id]);
      }, 2000)

    }
  }

  onAddOrganisation(): boolean {

    let organisation = this.selectedNewOrganisation;
    let engagementLevel = +this.organisationForm.get('engagementLevel').value;
    let category = this.selectedCategory;
    let engagedOrganisation = new EngagedOrganisation(organisation, null, engagementLevel, category);

    if (this.organisationAlreadyEngaged(organisation)) {
      this.updateEngagedOrganisation(engagedOrganisation);
    } else {
      this.engagedOrganisations.push(engagedOrganisation);
    }

    this.organisationForm.get('engagementLevel').setValue(0);
    this.organisationForm.get('engagementLevel').markAsUntouched();
    this.selectedNewOrganisation = null;
    this.selectedEngagedOrganisation = null;
    this.selectedCategory = '';
    return true;
  }

  engagedOrganisationAlreadyEngaged(engagedOrganisation: EngagedOrganisation): boolean {
    for (let i = 0; i < this.engagedOrganisations.length; i++) {
      if (engagedOrganisation.id === this.engagedOrganisations[i].id) {
        return true;
      }
    }
    return false;
  }

  updateEngagedOrganisation(engagedOrganisation: EngagedOrganisation) {
    for (let i = 0; i < this.engagedOrganisations.length; i++) {
      if (this.engagedOrganisations[i].organisation.id === engagedOrganisation.organisation.id) {
        this.engagedOrganisations[i].engagementLevel = engagedOrganisation.engagementLevel;
        this.engagedOrganisations[i].category = engagedOrganisation.category;
      }
    }
  }

  organisationAlreadyEngaged(organisation: Organisation): boolean {
    for (let i = 0; i < this.engagedOrganisations.length; i++) {
      if (this.engagedOrganisations[i].organisation.id === organisation.id) {
        return true;
      }
    }
    return false;
  }

  onClickAddOrganisations() {
    this.addEngagedOrganisation = true;
  }

  onCloseOrganisation() {
    this.addEngagedOrganisation = false;
  }

  onSelectEngagedOrganisation(engagedOrganisation: EngagedOrganisation) {
    if(confirm("Are you sure you want to remove this engaged organisation?")) {

      // Only add the engagedOrganisation to be deleted if it already exists in the database.
      let engagedOrganisations = this.engagedOrganisationService.getAllForProject(this.projectToEdit.id);

      if (engagedOrganisations.includes(engagedOrganisation)) {
        this.engagedOrganisationsToDelete.push(engagedOrganisation);
      }

       this.engagedOrganisations.splice(this.engagedOrganisations.indexOf(engagedOrganisation), 1);

      this.selectedEngagedOrganisation = null;
      this.selectedNewOrganisation = null;
    }
  }

  onClickCancel() {
    this.selectedEngagedOrganisation = null;
    this.selectedNewOrganisation = null;
    this.selectedMember = null;
  }

  onClickDone() {
    this.addEngagedOrganisation = false;
    this.editMembers = false;
  }

  onSelectNewOrganisation(organisation: Organisation) {
    if (this.organisationAlreadyEngaged(organisation)) {
      this.organisationForm.get('engagementLevel').setValue(this.getEngagedOrganisationById(organisation.id).engagementLevel);
      this.selectedCategory = this.getEngagedOrganisationById(organisation.id).category;
    } else {
      this.selectedCategory = '';
      this.organisationForm.get('engagementLevel').setValue(0);
    }
    this.selectedNewOrganisation = organisation;
  }

  onCancelAddOrganisation() {
    this.selectedNewOrganisation = null;
    this.selectedEngagedOrganisation = null;
  }

  onClickEditMembers() {
    this.editMembers = true;
  }

  onSelectMember(member: ProjectMember) {
    this.selectedMember = member;
    if (this.selectedMember.role === ProjectRolesEnum.Project_Manager) {
      this.roleForm.get('role').setValue('1');
    } else {
      this.roleForm.get('role').setValue('2');
    }
  }

  onClickRemoveMember() {
    this.projectMemberService.deleteById(this.selectedMember.id);
    this.selectedMember = null;
  }

  onClickConfirm() {
    if (this.roleForm.get('role').value === '1') {
      this.selectedMember.role = ProjectRolesEnum.Project_Manager;
      this.projectMemberService.updateWithoutEmit(this.selectedMember);
      this.selectedMember = null;
    } else if (this.roleForm.get('role').value === '2') {
      this.selectedMember.role = ProjectRolesEnum.Project_Staff;
      this.projectMemberService.updateWithoutEmit(this.selectedMember);
      this.selectedMember = null;
    } else {
      this.selectedMember = null;
    }
  }

  isOwner(): boolean {
    if (this.projectToEdit === null) {
      return false;
    }

    let owner = this.projectsService.getProjectOwner(this.projectToEdit);

    if (owner !== null) {
      return owner.id === this.loggedInUser.id;
    }

    return false;

  }

  getEngagedOrganisationById(id: number): EngagedOrganisation {
    for (let i = 0; i < this.engagedOrganisations.length; i++) {
      if (this.engagedOrganisations[i].organisation.id === id) {
        return this.engagedOrganisations[i];
      }
    }
    return null;
  }
  onFileChanged(event) {
    //Select File
    this.selectedFile = event.target.files[0];
    this.chooseFile = true;

  }

  onUpload(projectId: number) {


    //FormData API provides methods and properties to allow us easily prepare form data to be sent with POST HTTP requests.
    const uploadImageData = new FormData();
    uploadImageData.append('imageFile', this.selectedFile, this.selectedFile.name);

    //Make a call to the Spring Boot Application to save the image
    this.httpClient.post('http://localhost:8080/image/upload/project/' +  projectId, uploadImageData, { observe: 'response' })
      .subscribe((response) => {
          if (response.status === 200) {
            this.message = 'Image uploaded successfully';
          } else {
            this.message = 'Image not uploaded successfully';
          }
        }
      );

  }

  deleteImage(id: number){
    this.httpClient.delete('http://localhost:8080/image/projectImage/' + id).subscribe();
    this.projectsService.retrievedImage = null;
    this.projectsService.projectHasPhoto = false;
  }

}
