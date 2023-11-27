export class User {
  public id: number;
  public firstName: string;
  public lastName: string;
  public email: string;
  public password: string;
  public birthDate: Date;
  public country: string;
  public description: string;
  public imagePath: string;

  constructor(firstName: string, lastName: string, email: string, password: string, birthDate: Date, country: string, description: string, imagePath: string) {
    this.firstName = firstName;
    this.lastName = lastName;
    this.email = email;
    this.password = password;
    this.birthDate = birthDate;
    this.country = country;
    this.description = description;
    if(imagePath == null){
      this.imagePath = 'assets/images/generic-profile-icon-23.png';
    }else{
      this.imagePath = imagePath;
    }
  }

}
