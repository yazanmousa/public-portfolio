package app.models.user;
import javax.persistence.*;

@Entity
public class UserAttribute {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;
    @ManyToOne
    private User user;
    private String attribute;
    private double average;

    public UserAttribute() {

    }

    public UserAttribute(User user, String attribute, double average) {
        this.user = user;
        this.attribute = attribute;
        this.average = average;
    }

    public long getId() {
        return id;
    }

    public User getUser() {
        return user;
    }

    public String getAttribute() {
        return attribute;
    }

    public double getAverage() {
        return average;
    }

    @Override
    public String toString() {
        return "UserAttribute{" +
                "id=" + id +
                ", user=" + user +
                ", attribute='" + attribute + '\'' +
                ", average=" + average +
                '}';
    }
}
