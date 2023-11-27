package app.models.project;

import com.fasterxml.jackson.annotation.JsonManagedReference;

import javax.persistence.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
@Entity
public class Project {
  @Id
  @GeneratedValue(strategy = GenerationType.AUTO)
  private long id;
  private String name;
  private String description;
  private String country;
  private int requiredParticipants;
  private String imageSource;
  private LocalDate dateCreated;

  public Project() {

  }

  public Project(long id, String name, String description, String country, int requiredParticipants,
                 String imageSource, LocalDate dateCreated) {
    this.id = id;
    this.name = name;
    this.description = description;
    this.country = country;
    this.requiredParticipants = requiredParticipants;
    this.imageSource = imageSource;
    this.dateCreated = dateCreated;
  }

  public long getId() {
    return id;
  }

  public String getName() {
    return name;
  }

  public String getDescription() {
    return description;
  }

  public String getCountry() {
    return country;
  }

  public int getRequiredParticipants() {
    return requiredParticipants;
  }

  public String getImageSource() {
    return imageSource;
  }

  public LocalDate getDateCreated() {
    return dateCreated;
  }

  public void setId(long id) {
    this.id = id;
  }

  @Override
  public String toString() {
    return "Project{" +
            "id=" + id +
            ", name='" + name + '\'' +
            ", description='" + description + '\'' +
            ", country='" + country + '\'' +
            ", requiredParticipants=" + requiredParticipants +
            ", imageSource='" + imageSource + '\'' +
            ", dateCreated=" + dateCreated +
            '}';
  }
}
