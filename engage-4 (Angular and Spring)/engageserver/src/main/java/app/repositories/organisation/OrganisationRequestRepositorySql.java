package app.repositories.organisation;

import app.models.organisation.PendingOrganisationRequest;
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
public class OrganisationRequestRepositorySql implements Repository<PendingOrganisationRequest> {
    @Autowired
    private EntityManager em;


    @Override
    public List<PendingOrganisationRequest> findAll() {
        TypedQuery<PendingOrganisationRequest> query = this.em.createQuery(
                "SELECT p from PendingOrganisationRequest p", PendingOrganisationRequest.class
        );
        return query.getResultList();
    }

    @Override
    public PendingOrganisationRequest findById(long id) {
        return em.find(PendingOrganisationRequest.class, id);
    }

    @Override
    public PendingOrganisationRequest save(PendingOrganisationRequest object) {
        return em.merge(object);
    }

    @Override
    public boolean deleteById(long id) {
        PendingOrganisationRequest toRemove = findById(id);
        em.remove(toRemove);
        return toRemove != null;
    }
}
