package app.models.project;

import app.models.user.User;
import com.fasterxml.jackson.annotation.JsonBackReference;

import javax.persistence.*;

@Entity
public class PendingRequest {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;
    @ManyToOne
    private User sendByUser;
    @ManyToOne
    private Project project;

    public PendingRequest() {

    }

    public PendingRequest(long id, User sendByUser) {
        this.id = id;
        this.sendByUser = sendByUser;
    }

    public long getId() {
        return id;
    }

    public User getSendByUser() {
        return sendByUser;
    }

    public Project getProject() {
        return project;
    }

    @Override
    public String toString() {
        return "PendingRequest{" +
                "id=" + id +
                ", sendByUser=" + sendByUser +
                ", project=" + project +
                '}';
    }
}
