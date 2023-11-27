package app.models.organisation;

import app.models.user.User;

import javax.persistence.*;

@Entity
public class OrganisationMember {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;
    @OneToOne
    private User user;
    @ManyToOne(cascade = CascadeType.PERSIST)
    private Organisation organisation;
    private boolean owner;
    private boolean administrator;

    public OrganisationMember() {

    }

    public OrganisationMember(User user, Organisation organisation, boolean owner, boolean administrator) {
        this.user = user;
        this.organisation = organisation;
        this.owner = owner;
        this.administrator = administrator;
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Organisation getOrganisation() {
        return organisation;
    }

    public void setOrganisation(Organisation organisation) {
        this.organisation = organisation;
    }

    public boolean isOwner() {
        return owner;
    }

    public void setOwner(boolean owner) {
        this.owner = owner;
    }

    public boolean isAdministrator() {
        return administrator;
    }

    public void setAdministrator(boolean administrator) {
        this.administrator = administrator;
    }

    @Override
    public String toString() {
        return "OrganisationMember{" +
                "id=" + id +
                ", user=" + user +
                ", organisation=" + organisation +
                ", owner=" + owner +
                ", administrator=" + administrator +
                '}';
    }
}
