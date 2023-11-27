package app.models.organisation;

import javax.persistence.*;
import java.time.LocalDate;

@Entity
public class Organisation {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;
    private String name;
    private String country;
    private String email;
    private String description;
    private LocalDate dateCreated;
    private String imagePath;

    public Organisation() {

    }

    public Organisation(String name, String email, String description, LocalDate dateCreated, String imagePath, String country) {
        this.name = name;
        this.email = email;
        this.description = description;
        this.country = country;
        this.dateCreated = dateCreated;
        this.imagePath = imagePath;
    }


    public void setId(long id) {
        this.id = id;
    }

    public long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getCountry() {
        return country;
    }

    public String getEmail() {
        return email;
    }

    public String getDescription() {
        return description;
    }

    public LocalDate getDateCreated() {
        return dateCreated;
    }

    public String getImagePath() {
        return imagePath;
    }

    @Override
    public String toString() {
        return "Organisation{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", country='" + country + '\'' +
                ", email='" + email + '\'' +
                ", description='" + description + '\'' +
                ", dateCreated=" + dateCreated +
                ", imagePath='" + imagePath + '\'' +
                '}';
    }
}
