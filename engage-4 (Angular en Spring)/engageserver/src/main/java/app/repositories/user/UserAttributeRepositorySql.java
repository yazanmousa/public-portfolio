package app.repositories.user;

import app.models.user.UserAttribute;
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
public class UserAttributeRepositorySql implements Repository<UserAttribute> {
    @Autowired
    private EntityManager em;

    @Override
    public List<UserAttribute> findAll() {
        TypedQuery<UserAttribute> query = this.em.createQuery(
                "SELECT u FROM UserAttribute u", UserAttribute.class
        );
        return query.getResultList();
    }

    @Override
    public UserAttribute findById(long id) {
        return em.find(UserAttribute.class, id);
    }

    @Override
    public UserAttribute save(UserAttribute object) {
        return em.merge(object);
    }

    @Override
    public boolean deleteById(long id) {
        UserAttribute toRemove = findById(id);
        em.remove(toRemove);
        return toRemove != null;
    }
}
