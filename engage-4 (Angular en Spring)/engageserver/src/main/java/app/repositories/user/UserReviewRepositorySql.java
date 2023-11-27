package app.repositories.user;

import app.models.user.UserReview;
import app.repositories.Repository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Primary;

import javax.persistence.EntityManager;
import javax.persistence.TypedQuery;
import javax.transaction.Transactional;
import java.util.List;

@org.springframework.stereotype.Repository
@Transactional
@Primary
public class UserReviewRepositorySql implements Repository<UserReview> {

    @Autowired
    private EntityManager em;

    @Override
    public List<UserReview> findAll() {
        TypedQuery<UserReview> query = this.em.createQuery(
                "SELECT u FROM UserReview u", UserReview.class
        );
        return query.getResultList();
    }

    @Override
    public UserReview findById(long id) {
        return em.find(UserReview.class, id);
    }

    @Override
    public UserReview save(UserReview object) {
        return em.merge(object);
    }

    @Override
    public boolean deleteById(long id) {
        UserReview toRemove = findById(id);
        em.remove(toRemove);
        return toRemove != null;
    }
}
