import {User} from './user.model';

export class UserUpdate {
  id: number;
  user: User;
  title: string;
  time: number;

  constructor(user: User, title: string, time: number) {
    this.user = user;
    this.title = title;
    this.time = time;
  }
}
