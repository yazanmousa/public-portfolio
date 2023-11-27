package app.models.project;

import app.models.user.User;

import javax.persistence.*;
import java.time.LocalDate;

@Entity
public class ProjectInvite {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;
    @ManyToOne
    private User sendByUser;
    @ManyToOne
    private User receivedByUser;
    @ManyToOne
    private Project project;
    private LocalDate date;

    public ProjectInvite() {

    }

    public ProjectInvite(User sendByUser, User receivedByUser, Project project, LocalDate date) {
        this.sendByUser = sendByUser;
        this.receivedByUser = receivedByUser;
        this.project = project;
        this.date = date;
    }

    public long getId() {
        return id;
    }

    public User getSendByUser() {
        return sendByUser;
    }

    public User getReceivedByUser() {
        return receivedByUser;
    }

    public Project getProject() {
        return project;
    }

    public LocalDate getDate() {
        return date;
    }

    @Override
    public String toString() {
        return "PendingInvite{" +
                "id=" + id +
                ", sendByUser=" + sendByUser +
                ", receivedByUser=" + receivedByUser +
                ", project=" + project +
                '}';
    }
}
