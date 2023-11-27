import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {environment} from '../../../environments/environment';
import {UserReview} from '../../models/user/user-review';
import {User} from '../../models/user/user.model';

@Injectable({
  providedIn: 'root'
})
export class UserReviewsService {
  reviews: UserReview[];
  reviewsChanged = new EventEmitter();

  constructor(private httpClient: HttpClient) {
    this.reviews = [];
    this.restGetUserReviews().subscribe(response => {
      this.reviews = response;
    }, error => {
      console.log(error.message);
    })
  }

  findAll(): UserReview[] {
    return this.reviews;
  }

  findById(id: number): UserReview {
    for (let i = 0; i < this.reviews.length; i++) {
      if (this.reviews[i].id === id) {
        return this.reviews[i];
      }
    }
  }

  save(review: UserReview): UserReview {
    let returnReview: UserReview = null;

    this.restPostUserReview(review).subscribe(response => {
      this.reviews.push(response);
      returnReview = response;
      this.reviewsChanged.emit();
    })
    return returnReview;
  }

  saveMultipleReviews(reviews: UserReview[]) {
    this.restPostMultipleReviews(reviews).subscribe(response => {
      for (let i = 0; i < response.length; i++) {
        this.reviews.push(response[i]);
      }
      this.reviewsChanged.emit();
    })
  }

  update(review: UserReview) {
    this.restPutUserReview(review).subscribe(response => {
      for (let i = 0; i < this.reviews.length; i++) {
        if (response.id === this.reviews[i].id) {
          this.reviews[i] = response;
          this.reviewsChanged.emit();
        }
      }
    })
  }

  deleteById(id: number) {
    this.restDeleteUserReview(id).subscribe(() => {
      for (let i = 0; i < this.reviews.length; i++) {
        if (this.reviews[i].id === id) {
          this.reviews.splice(i, 1);
          this.reviewsChanged.emit();
        }
      }
    })
  }

  deleteMultipleReviews(reviews: UserReview[]) {
    this.restDeleteMultipleReviews(reviews).subscribe(response => {
      for (let i = 0; i < reviews.length; i++) {
        let index = this.reviews.indexOf(reviews[i]);
        this.reviews.splice(index, 1);
      }
      this.reviewsChanged.emit();
    })
  }

  deleteAllReviewsForSpecificEvaluator(evaluatedId: number, evaluatorId: number) {
    let reviewsToDelete = [];
    const reviews = this.getAllForUser(evaluatedId);

    // looping only through the reviews that belong to the specified evaluated user
    // and delete only the reviews that have been given by the specified evaluator.
    for (let i = 0; i < reviews.length; i++) {
      if (reviews[i].evaluator.id === evaluatorId) {
        reviewsToDelete.push(reviews[i]);
      }
    }

    if (reviewsToDelete.length >= 1) {
      this.deleteMultipleReviews(reviewsToDelete);
    }

  }

  getAllForAttribute(userAttributeId: number): UserReview[] {
    let tempReviews = [];
    for (let i = 0; i < this.reviews.length; i++) {
      if (this.reviews[i].evaluated.id === userAttributeId) {
        tempReviews.push(this.reviews[i]);
      }
    }
    return tempReviews;
  }

  getAllForUser(userId: number): UserReview[] {
    let tempReviews = [];
    for (let i = 0; i < this.reviews.length; i++) {
      if (this.reviews[i].evaluated.user.id === userId) {
        tempReviews.push(this.reviews[i]);
      }
    }
    return tempReviews;
  }

  /**
   * This method will retrieve a list of reviews for every single user that has reviewed this person before.
   * @param userId of the user that has received the reviews
   */
  getListOfReviewsForEveryUser(userId: number): Array<Array<UserReview>> {
    let listOfReviewLists = [];
    let tempReviewList = [];
    let reviewers = this.getAllReviewersForUser(userId);

    for (let i = 0; i < reviewers.length; i++) {
      for (let j = 0; j < this.reviews.length; j++) {
        if (this.reviews[j].evaluator.id === reviewers[i].id && this.reviews[j].evaluated.user.id === userId) {
          tempReviewList.push(this.reviews[j]);
        }
      }
      listOfReviewLists.push(tempReviewList);
      tempReviewList = [];
    }

    console.log("List of review lists method:" + listOfReviewLists);

    return listOfReviewLists;
  }

  // Retrieve all users that have rated this person before.
  getAllReviewersForUser(userId: number): User[] {
    let reviewers: User[] = [];
    for (let i = 0; i < this.reviews.length; i++) {

      if (this.reviews[i].evaluated.user.id === userId) {
        let containsUser: boolean = false;

        for (let j = 0; j < reviewers.length; j++) {

          if (this.reviews[i].evaluator.id === reviewers[j].id) {
            containsUser = true;
          }

        }
        if (!containsUser) {
          reviewers.push(this.reviews[i].evaluator);
        }

      }
    }
    return reviewers;
  }


  getStarCountsForUser(userId: number): number[] {
    let starcounts = [];
    const reviews = this.getAllForUser(userId);
    for (let i = 1; i < 6; i++) {
      let starCount = 0;
      for (let j = 0; j < reviews.length; j++) {
        // only increment the starCount if the value equals i (1, 2, 3, 4, 5)
        if (reviews[j].rating === i) {
          starCount++
        }
      }
      starcounts.push(starCount);
    }
    return starcounts
  }

  restGetUserReviews(): Observable<UserReview[]> {
    return this.httpClient.get<UserReview[]>(`${environment.apiUrl}/user-reviews`);
  }

  restPostUserReview(review: UserReview): Observable<UserReview> {
    return this.httpClient.post<UserReview>(`${environment.apiUrl}/user-reviews`, review);
  }

  restPostMultipleReviews(reviews: UserReview[]): Observable<UserReview[]> {
    return this.httpClient.post<UserReview[]>(`${environment.apiUrl}/user-reviews/multiple`, reviews);
  }

  restPutUserReview(review: UserReview): Observable<UserReview> {
    const url = `${environment.apiUrl}/user-reviews/` + review.id;
    return this.httpClient.put<UserReview>(url, review);
  }

  restDeleteUserReview(id: number): Observable<UserReview> {
    const url = `${environment.apiUrl}/user-reviews/` + id;
    return this.httpClient.delete<UserReview>(url);
  }

  restDeleteMultipleReviews(reviews: UserReview[]): Observable<UserReview[]> {
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      }),
      body: reviews
    };

    return this.httpClient.delete<UserReview[]>(`${environment.apiUrl}/user-reviews`, options);
  }
}
