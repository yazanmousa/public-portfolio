import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'projectFilter'
})
export class ProjectFilterPipe implements PipeTransform {

  transform(items: any[], searchText: string): any[] {
    if (!items) {
      return [];
    }
    if (!searchText) {
      return items;
    }

    return items.filter(it => {
      return it.name.toLocaleLowerCase().includes(searchText.toLocaleLowerCase());
    });
  }

}
