import {User} from '../user/user.model';
import {Project} from './project';

export class ProjectInvite {
  id: number;
  sendByUser: User;
  receivedByUser: User;
  project: Project;
  date: Date;

  constructor(sendByUser: User, receivedByUser: User, project: Project, time: Date) {
    this.sendByUser = sendByUser;
    this.receivedByUser = receivedByUser;
    this.project = project;
    this.date = time;
  }
}
