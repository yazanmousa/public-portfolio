package app.models.project;

import app.models.user.User;

import javax.persistence.*;

@Entity
public class ProjectMember {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;
    @ManyToOne
    private Project project;
    @OneToOne
    private User user;
    private boolean owner;
    private String role;

    public ProjectMember() {

    }

    public ProjectMember(Project project, User user, boolean owner, String role) {
        this.project = project;
        this.user = user;
        this.owner = owner;
        this.role = role;
    }

    public long getId() {
        return id;
    }

    public Project getProject() {
        return project;
    }

    public User getUser() {
        return user;
    }

    public boolean isOwner() {
        return owner;
    }

    public String getRole() {
        return role;
    }

    @Override
    public String toString() {
        return "ProjectMember{" +
                "id=" + id +
                ", project=" + project +
                ", owner=" + owner +
                ", role=" + role +
                '}';
    }
}
