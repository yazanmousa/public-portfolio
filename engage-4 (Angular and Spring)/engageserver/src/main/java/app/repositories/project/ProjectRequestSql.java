package app.repositories.project;

import app.models.project.PendingRequest;
import app.models.project.Project;
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
public class ProjectRequestSql implements Repository<PendingRequest> {

    @Autowired
    private EntityManager em;

    @Override
    public List<PendingRequest> findAll() {
        TypedQuery<PendingRequest> query = this.em.createQuery(
                "SELECT e from PendingRequest e", PendingRequest.class
        );
        return query.getResultList();
    }

    @Override
    public PendingRequest findById(long id) {
        return em.find(PendingRequest.class, id);
    }

    @Override
    public PendingRequest save(PendingRequest object) {
        return em.merge(object);
    }

    @Override
    public boolean deleteById(long id) {
        PendingRequest toRemove = findById(id);
        em.remove(toRemove);
        return toRemove != null;
    }
}
