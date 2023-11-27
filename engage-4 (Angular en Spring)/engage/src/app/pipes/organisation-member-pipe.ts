import {Pipe, PipeTransform} from '@angular/core';
import {OrganisationMember} from '../models/organisation/organisation-member';
import {UserService} from '../services/user/user.service';

@Pipe({
  name: 'organisationMemberPipe'
})
export class OrganisationMemberPipe implements PipeTransform {

  constructor(private userService: UserService) {
  }

  transform(items: OrganisationMember[], searchText: string): OrganisationMember[] {
    if (!items) {
      return [];
    }
    if (!searchText) {
      return items;
    }

    return items.filter(it => {
      let user = this.userService.findUserById(it.user.id);

      return user.firstName.toLocaleLowerCase().includes(searchText.toLocaleLowerCase());
    });
  }

}