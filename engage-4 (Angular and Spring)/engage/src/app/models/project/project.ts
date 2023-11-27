export class Project {
  id: number;
  name: string;
  description: string;
  country: string;
  requiredParticipants: number;
  imageSource: string;
  dateCreated: Date;

  constructor(name: string, description: string, country: string, requiredParticipants: number, imageSource: string, dateCreated: Date) {
    this.name = name;
    this.description = description;
    this.country = country;
    this.requiredParticipants = requiredParticipants;
    this.imageSource = imageSource;
    this.dateCreated = dateCreated;
  }
}
