import {User} from '../user/user.model';
import {Project} from './project';

export class PendingRequest {
  id: number;
  sendByUser: User;
  project: Project;


  constructor(sendByUser: User, project: Project) {
    this.sendByUser = sendByUser;
    this.project = project;
  }
}
