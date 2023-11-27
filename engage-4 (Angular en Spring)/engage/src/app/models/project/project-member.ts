import {Project} from './project';
import {User} from '../user/user.model';

export class ProjectMember {
  id: number;
  project: Project;
  user: User;
  owner: boolean;
  role: string;

  constructor(project: Project, user: User, owner: boolean, role: string) {
    this.project = project;
    this.user = user;
    this.owner = owner;
    this.role = role;
  }

}
