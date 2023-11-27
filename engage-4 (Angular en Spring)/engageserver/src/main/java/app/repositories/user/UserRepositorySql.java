package app.repositories.user;

import app.models.user.User;
import app.repositories.Repository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Primary;

import javax.persistence.EntityManager;
import javax.persistence.TypedQuery;
import javax.transaction.Transactional;
import java.util.List;

/**
 * @author Yazan
 * Date 12/05/2021 20:15
 *
 */

@org.springframework.stereotype.Repository
@Transactional
@Primary
public class UserRepositorySql implements Repository<User> {

    @Autowired
    private EntityManager em;

    @Override
    public List<User> findAll() {
        TypedQuery<User> query = this.em.createQuery(
                "SELECT e from User e", User.class
        );
        return query.getResultList();
    }

    @Override
    public User findById(long id) {
        return em.find(User.class, id);
    }

    @Override
    public User save(User object) {
        return this.em.merge(object);
    }

    @Override
    public boolean deleteById(long id) {
        User toRemove = findById(id);
        em.remove(toRemove);
        return toRemove != null;
    }
}
