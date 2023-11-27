import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'userPipe'
})
export class UserPipePipe implements PipeTransform {

  transform(items: any[], searchText: string): any[] {
    if (!items) {
      return [];
    }
    if (!searchText) {
      return items;
    }

    return items.filter(it => {
      return it.firstName.toLocaleLowerCase().includes(searchText.toLocaleLowerCase());
    });
  }

}
