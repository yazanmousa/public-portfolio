import {User} from './user.model';
import {UserReview} from './user-review';

export class UserAttribute {
  id: number;
  user: User;
  attribute: string;
  average: number;

  constructor(user: User, attribute: string, average: number) {
    this.user = user;
    this.attribute = attribute;
    this.average = average;
  }

  // public updateAverage(): void {
  //   let totalScore = 0;
  //   for (let i = 0; i < this.reviews.length; i++) {
  //     totalScore += this.reviews[i].rating;
  //   }
  //   this.average = totalScore / this.reviews.length;
  // }

}


