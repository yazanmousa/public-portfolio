import {User} from '../user/user.model';
import {Organisation} from './organisation';

export class PendingOrganisationRequest {
  id: number;
  sendByUser: User
  organisation: Organisation;

  constructor(sendByUser: User, organisation: Organisation) {
    this.sendByUser = sendByUser;
    this.organisation = organisation;
  }
}
