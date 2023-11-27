package app.models.organisation;

import app.models.user.User;
import com.fasterxml.jackson.annotation.JsonBackReference;

import javax.persistence.*;

@Entity
public class PendingOrganisationRequest {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;
    @OneToOne
    private User sendByUser;
    @ManyToOne
    private Organisation organisation;

    public PendingOrganisationRequest() {

    }

    public PendingOrganisationRequest(User sendByUser, Organisation organisation) {
        this.sendByUser = sendByUser;
        this.organisation = organisation;
    }

    public long getId() {
        return id;
    }

    public User getSendByUser() {
        return sendByUser;
    }

    public Organisation getOrganisation() {
        return organisation;
    }

    @Override
    public String toString() {
        return "PendingOrganisationRequest{" +
                "id=" + id +
                ", sendByUser=" + sendByUser +
                ", organisation=" + organisation +
                '}';
    }
}
