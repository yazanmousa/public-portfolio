import {Organisation} from '../organisation/organisation';
import {Project} from './project';

export class EngagedOrganisation {
  id: number;
  organisation: Organisation;
  project: Project;
  engagementLevel: number;
  category: string;


  constructor(organisation: Organisation, project: Project, engagementLevel: number, category: string) {
    this.organisation = organisation;
    this.engagementLevel = engagementLevel;
    this.category = category;
    this.project = project;
  }
}
