import {UserAttribute} from './user-attribute';
import {User} from './user.model';

export class UserReview {
  id: number;
  evaluator: User;
  evaluated: UserAttribute;
  rating: number;
  time: number;

  constructor(evaluator: User, evaluated: UserAttribute, rating: number, time: number) {
    this.evaluator = evaluator;
    this.evaluated = evaluated;
    this.rating = rating;
    this.time = time;
  }
}