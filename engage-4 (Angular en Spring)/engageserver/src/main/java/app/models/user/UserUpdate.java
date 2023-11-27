package app.models.user;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

import javax.persistence.*;

//@Entity
public class UserUpdate {
//    @Id
//    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;
    @ManyToOne
    @OnDelete(action = OnDeleteAction.NO_ACTION)
    private User user;
    private String title;
    private long time;

    public UserUpdate() {

    }

    public UserUpdate(String title, long time, User user) {
        this.title = title;
        this.time = time;
        this.user = user;
    }

    public long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public long getTime() {
        return time;
    }

    public User getUser() {
        return user;
    }

    @Override
    public String toString() {
        return "UserUpdate{" +
                "id=" + id +
                ", user=" + user +
                ", title='" + title + '\'' +
                ", time=" + time +
                '}';
    }
}
