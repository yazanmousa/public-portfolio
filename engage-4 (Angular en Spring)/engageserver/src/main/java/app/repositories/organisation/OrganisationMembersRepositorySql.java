package app.repositories.organisation;

import app.models.organisation.Organisation;
import app.models.organisation.OrganisationMember;
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
public class OrganisationMembersRepositorySql implements Repository<OrganisationMember> {

    @Autowired
    private EntityManager em;

    @Override
    public List<OrganisationMember> findAll() {
        TypedQuery<OrganisationMember> query = this.em.createQuery(
                "SELECT om from OrganisationMember om", OrganisationMember.class
        );
        return query.getResultList();
    }

    @Override
    public OrganisationMember findById(long id) {
        return em.find(OrganisationMember.class, id);
    }

    @Override
    public OrganisationMember save(OrganisationMember object) {
        return em.merge(object);
    }

    @Override
    public boolean deleteById(long id) {
        OrganisationMember toRemove = findById(id);
        em.remove(toRemove);
        return toRemove != null;
    }
}
