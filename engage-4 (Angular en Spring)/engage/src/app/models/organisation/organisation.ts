export class Organisation {
  id: number;
  name: string;
  country: string;
  email: string;
  description: string;
  dateCreated: Date;
  imagePath: string;


  constructor(name: string, country: string, email: string, description: string, dateCreated: Date, imagePath: string) {
    this.name = name;
    this.country = country;
    this.email = email;
    this.description = description;
    this.dateCreated = dateCreated;
    this.imagePath = imagePath;
  }
}
