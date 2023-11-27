package app.repositories.project;

import app.models.project.EngagedOrganisation;
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
public class EngagedOrganisationRepositorySql implements Repository<EngagedOrganisation> {

    @Autowired
    private EntityManager em;

    @Override
    public List<EngagedOrganisation> findAll() {
        TypedQuery<EngagedOrganisation> query = this.em.createQuery(
                "SELECT e FROM EngagedOrganisation e", EngagedOrganisation.class
        );
        return query.getResultList();
    }

    @Override
    public EngagedOrganisation findById(long id) {
        return em.find(EngagedOrganisation.class, id);
    }

    @Override
    public EngagedOrganisation save(EngagedOrganisation object) {
        return em.merge(object);
    }

    @Override
    public boolean deleteById(long id) {
        EngagedOrganisation toRemove = findById(id);
        em.remove(toRemove);
        return toRemove != null;
    }
}
