import {Component, OnInit} from '@angular/core';
import {Attribute} from '../../../../models/user/user-attributes-enum';
import {NgbRatingConfig} from '@ng-bootstrap/ng-bootstrap';
import {UserReview} from '../../../../models/user/user-review';
import {User} from '../../../../models/user/user.model';
import {UserService} from '../../../../services/user/user.service';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {UserAttribute} from '../../../../models/user/user-attribute';
import {animate, state, style, transition, trigger} from '@angular/animations';
import {UserAttributesService} from '../../../../services/user/user-attributes.service';
import {UserReviewsService} from '../../../../services/user/user-reviews.service';
import {UserUpdate} from '../../../../models/user/user-update';
import {UserUpdatesService} from '../../../../services/user/user-updates.service';
import {ProjectMemberService} from '../../../../services/project/project-member.service';
import {ProjectMember} from '../../../../models/project/project-member';

@Component({
  selector: 'app-profile-reviews',
  templateUrl: './profile-reviews.component.html',
  styleUrls: ['./profile-reviews.component.css'],
  animations: [
    trigger('showContent', [
      state('in', style({opacity: 0, transform: 'translateY(0)'})),
      transition('void => *', [
        style({opacity: 0, transform: 'translateY(-100px)'}), animate(300)
      ])
    ])
  ]
})
export class ProfileReviewsComponent implements OnInit {
  user: User;
  loggedInUser: User;
  currentRate = 0;
  selectedAttribute: string = '';
  tempReviewsList: UserReview[] = [];
  tempAttributesList: UserAttribute[] = [];
  listOfReviewLists: Array<Array<UserReview>> = [];
  attributesEnum: string[] = Object.values(Attribute);
  ratedAttributes: UserAttribute[] = [];
  savedAttributes: UserAttribute[] = [];
  toggle = false;
  starCounts: number[] = [];
  oneStarCount: number = 0;
  twoStarCount: number = 0;
  threeStarCount: number = 0;
  fourStarCount: number = 0;
  fiveStarCount: number = 0;
  totalReviewCount: number = 0;
  totalAverageRating: number = 0;
  date: number = Date.now();
  loading: boolean = false;

  constructor(
      config: NgbRatingConfig,
      private userService: UserService,
      private userAttributesService: UserAttributesService,
      private userReviewsService: UserReviewsService,
      private userUpdatesService: UserUpdatesService,
      private projectMemberService: ProjectMemberService,
      private route: ActivatedRoute
  ) {
    config.max = 5;
  }

  ngOnInit(): void {
    this.initReviews();

    this.userReviewsService.reviewsChanged.subscribe(() => {
      this.initReviews();
    })

    this.userAttributesService.userAttributesChanged.subscribe(() => {
      this.initReviews();
    })

    this.userAttributesService.savedAttributesSubject.subscribe(attributes => {
      this.savedAttributes = attributes;
    })

  }

  initReviews() {
    this.loggedInUser = this.userService.loggedInUser;

    this.route.params.subscribe(
        (params: Params) => {
          this.user = this.userService.findUserById(+params['id'])
        }
    )

    // Retrieving all the reviews that have been given to this user via the service
    if (this.userAttributesService.getAllForUser(this.user.id).length >= 1) {
      this.listOfReviewLists = this.userReviewsService.getListOfReviewsForEveryUser(this.user.id);
    }

    this.starCounts = this.userReviewsService.getStarCountsForUser(this.user.id);

    this.oneStarCount = this.starCounts[0];
    this.twoStarCount = this.starCounts[1];
    this.threeStarCount = this.starCounts[2];
    this.fourStarCount = this.starCounts[3];
    this.fiveStarCount = this.starCounts[4];

    // Adding up all values of the starCounts list to get the total amount of reviews.
    this.totalReviewCount = this.starCounts.reduce((a, b) => a + b, 0);

    this.totalAverageRating = this.calculateAverageRating();

    this.ratedAttributes = this.userAttributesService.getAllForUser(this.user.id);

  }

  onClickReview() {
    this.toggle = true;
  }

  onClickCancel() {
    this.tempReviewsList = [];
    this.currentRate = 0;
    this.selectedAttribute = '';
    this.toggle = false;
  }

  onClickRateAttribute() {
    if (this.currentRate === 0) {
      alert("Please give a rating of at least 1!");
      return;
    }

    if (this.selectedAttribute === '') {
      alert("Please select an attribute to review!");
      return;
    }

    if (this.attributeHasAlreadyBeenReviewed()) {
      alert("This attribute has already been reviewed!");
      return;
    }

    // If the user already has the attribute assigned no new attribute will be made. If the attribute doesn't yet exist for the user
    // a new UserAttribute object will be created
    if (this.userAttributesService.getAttributeForUser(this.user.id, this.selectedAttribute) !== null) {
      let userAttribute = this.userAttributesService.getAttributeForUser(this.user.id, this.selectedAttribute);
      let userReview = new UserReview(this.loggedInUser, userAttribute, this.currentRate, Date.now());
      this.tempReviewsList.push(userReview);
    } else {
      let userAttribute = new UserAttribute(this.user, this.selectedAttribute, 0);
      let userReview = new UserReview(this.loggedInUser, userAttribute, this.currentRate, Date.now());
      this.tempReviewsList.push(userReview);
      this.tempAttributesList.push(userAttribute);
    }
    this.selectedAttribute = '';
    this.currentRate = 0;
  }

  getAttributeNameForReview(review: UserReview): string {
    return review.evaluated.attribute;
  }

  attributeHasAlreadyBeenReviewed(): boolean {
    for (let i = 0; i < this.tempReviewsList.length; i++) {
      if (this.tempReviewsList[i].evaluated.attribute === this.selectedAttribute) {
        return true;
      }
    }
    return false;
  }

  onDeleteReview(review: UserReview) {
    for (let i = 0; i < this.tempReviewsList.length; i++) {
      if (this.tempReviewsList[i] === review) {
        this.tempReviewsList.splice(i, 1);
      }
    }
  }

  onSubmitReview() {
    this.loading = true;

    if (this.userAlreadyGaveReview(this.loggedInUser)) {
      this.userReviewsService.deleteAllReviewsForSpecificEvaluator(this.user.id, this.loggedInUser.id);
      this.listOfReviewLists = this.userReviewsService.getListOfReviewsForEveryUser(this.user.id);
    }

    if (this.tempAttributesList.length >= 1) {
      this.userAttributesService.saveMultipleAttributes(this.tempAttributesList);
    }

    setTimeout(() => {
      for (let i = 0; i < this.tempReviewsList.length; i++) {
        for (let j = 0; j < this.savedAttributes.length; j++) {
          if (this.tempReviewsList[i].evaluated.attribute === this.savedAttributes[j].attribute) {
            this.tempReviewsList[i].evaluated = this.savedAttributes[j];
          }
        }
      }

      this.userReviewsService.saveMultipleReviews(this.tempReviewsList);
    }, 1000)

    setTimeout(() => {
      this.userAttributesService.removeAttributesWithoutReviews(this.user.id);

      let update: UserUpdate;

      if (this.tempReviewsList.length > 1) {
        update = new UserUpdate(this.user,'You have received ratings for multiple attributes!', Date.now());
      } else {
        update = new UserUpdate(this.user,'You have received ratings for one attribute!', Date.now());
      }

      this.userUpdatesService.save(update);
    }, 2500)

    setTimeout(() => {
      this.userAttributesService.updateAveragesForUser(this.user.id);

      this.tempReviewsList = [];
      this.tempAttributesList = [];
      this.selectedAttribute = '';
      this.toggle = false;
      this.loading = false;
    }, 3500)

  }

  getReviewerName(reviewList: UserReview[]): string {
    return reviewList[0].evaluator.firstName + ' ' + reviewList[0].evaluator.lastName
  }

  getReviewerImage(reviewList: UserReview[]): string {

    return "assets/images/" + reviewList[0].evaluator.imagePath.split("\\")[2];
  }

  getReviewTime(reviewList: UserReview[]): number {
    return reviewList[0].time;
  }

  userAlreadyGaveReview(user: User): boolean {
    for (let i = 0; i < this.listOfReviewLists.length; i++) {
      if (this.listOfReviewLists[i][0].evaluator.id === user.id) {
        return true;
      }
    }
    return false;
  }

  calculateAverageRating(): number {
    let numberOfReviews = this.userReviewsService.getAllForUser(this.user.id).length;
    let totalScore = 0;
    let reviews = this.userReviewsService.getAllForUser(this.user.id);

    for (let i = 0; i < reviews.length; i++) {
      totalScore += reviews[i].rating;
    }

    if (totalScore === 0 && numberOfReviews === 0) {
      return 0;
    }

    return totalScore / numberOfReviews;

  }

  // This method will check if the loggedInUser and the profile user are working together in at least 1 project
  userIsPartOfSameProject(): boolean {
    let loggedInUserMembers: ProjectMember[] = this.projectMemberService.getAllForUser(this.loggedInUser.id);
    let profileUserMembers: ProjectMember[] = this.projectMemberService.getAllForUser(this.user.id);

    for (let i = 0; i < loggedInUserMembers.length; i++) {
      for (let j = 0; j < profileUserMembers.length; j++) {
        if (loggedInUserMembers[i].project.id === profileUserMembers[j].project.id) {
          return true;
        }
      }
    }
    return false;
  }
}
