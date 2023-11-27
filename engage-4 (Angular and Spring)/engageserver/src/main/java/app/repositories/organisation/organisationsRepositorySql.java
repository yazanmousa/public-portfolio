package app.repositories.organisation;

import app.models.organisation.Organisation;
import app.repositories.Repository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Primary;

import javax.persistence.EntityManager;
import javax.persistence.TypedQuery;
import javax.transaction.Transactional;
import java.util.List;

/**
 * @author Yazan
 * Date 13/05/2021 18:45
 */
@org.springframework.stereotype.Repository
@Transactional
@Primary
public class organisationsRepositorySql implements Repository<Organisation> {
    @Autowired
    private EntityManager em;


    @Override
    public List<Organisation> findAll() {
        TypedQuery<Organisation> query = this.em.createQuery(
                "SELECT e from Organisation e", Organisation.class
        );
        return query.getResultList();
    }

    @Override
    public Organisation findById(long id) {
        return em.find(Organisation.class, id);
    }

    @Override
    public Organisation save(Organisation object) {
        return em.merge(object);
    }

    @Override
    public boolean deleteById(long id) {
        Organisation toRemove = findById(id);
        em.remove(toRemove);
        return toRemove != null;
    }
}
