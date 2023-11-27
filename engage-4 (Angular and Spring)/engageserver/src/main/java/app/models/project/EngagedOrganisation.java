package app.models.project;

import app.models.organisation.Organisation;
import com.fasterxml.jackson.annotation.JsonBackReference;

import javax.persistence.*;

@Entity
public class EngagedOrganisation {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;
    @OneToOne
    private Organisation organisation;
    @ManyToOne
    private Project project;
    private int engagementLevel;
    private String category;

    public EngagedOrganisation() {

    }

    public EngagedOrganisation(Organisation organisation, Project project, int engagementLevel, String category) {
        this.organisation = organisation;
        this.engagementLevel = engagementLevel;
        this.category = category;
    }

    public Organisation getOrganisation() {
        return organisation;
    }

    public int getEngagementLevel() {
        return engagementLevel;
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public void setOrganisation(Organisation organisation) {
        this.organisation = organisation;
    }

    public void setEngagementLevel(int engagementLevel) {
        this.engagementLevel = engagementLevel;
    }

    public String getCategory() {
        return category;
    }

    public Project getProject() {
        return project;
    }

    @Override
    public String toString() {
        return "EngagedOrganisation{" +
                "id=" + id +
                ", organisation=" + organisation +
                ", project=" + project +
                ", engagementLevel=" + engagementLevel +
                ", category='" + category + '\'' +
                '}';
    }
}
