package app.models.user;

import javax.persistence.*;

@Entity
public class UserReview {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private long id;
    @ManyToOne
    private User evaluator;
    @ManyToOne
    private UserAttribute evaluated;
    private int rating;
    private long time;

    public UserReview() {

    }

    public UserReview(User evaluator, UserAttribute evaluated, int rating, long time) {
        this.evaluator = evaluator;
        this.evaluated = evaluated;
        this.rating = rating;
        this.time = time;
    }

    public long getId() {
        return id;
    }

    public User getEvaluator() {
        return evaluator;
    }

    public UserAttribute getEvaluated() {
        return evaluated;
    }

    public int getRating() {
        return rating;
    }

    public long getTime() {
        return time;
    }

    @Override
    public String toString() {
        return "UserReview{" +
                "id=" + id +
                ", evaluator=" + evaluator +
                ", evaluated=" + evaluated +
                ", rating=" + rating +
                ", time=" + time +
                '}';
    }
}
