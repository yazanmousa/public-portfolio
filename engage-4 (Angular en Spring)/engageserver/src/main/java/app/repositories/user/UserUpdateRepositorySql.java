package app.repositories.user;

import app.models.user.User;
import app.models.user.UserUpdate;
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
public class UserUpdateRepositorySql implements Repository<UserUpdate> {

    @Autowired
    private EntityManager em;

    @Override
    public List<UserUpdate> findAll() {
        TypedQuery<UserUpdate> query = this.em.createQuery(
                "SELECT u FROM UserUpdate u", UserUpdate.class
        );
        return query.getResultList();
    }

    @Override
    public UserUpdate findById(long id) {
        return em.find(UserUpdate.class, id);
    }

    @Override
    public UserUpdate save(UserUpdate object) {
        return em.merge(object);
    }

    @Override
    public boolean deleteById(long id) {
        UserUpdate toRemove = findById(id);
        em.remove(toRemove);
        return toRemove != null;
    }
}
