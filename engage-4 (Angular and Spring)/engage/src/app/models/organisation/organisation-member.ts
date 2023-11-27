import {UserService} from '../../services/user/user.service';
import {Organisation} from './organisation';
import {User} from '../user/user.model';

export class OrganisationMember {
  id: number;
  user: User;
  organisation: Organisation;
  owner: boolean;
  administrator: boolean;

  constructor(user: User, organisation: Organisation, administrator: boolean, owner: boolean) {
    this.user = user;
    this.organisation = organisation;
    this.administrator = administrator;
    this.owner = owner;
  }
}


