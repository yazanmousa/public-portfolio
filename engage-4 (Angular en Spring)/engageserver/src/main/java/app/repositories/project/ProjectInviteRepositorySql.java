package app.repositories.project;

import app.models.project.ProjectInvite;
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
public class ProjectInviteRepositorySql implements Repository<ProjectInvite> {

    @Autowired
    private EntityManager em;

    @Override
    public List<ProjectInvite> findAll() {
        TypedQuery<ProjectInvite> query = this.em.createQuery(
                "SELECT i FROM ProjectInvite i", ProjectInvite.class
        );
        return query.getResultList();
    }

    @Override
    public ProjectInvite findById(long id) {
        return em.find(ProjectInvite.class, id);
    }

    @Override
    public ProjectInvite save(ProjectInvite object) {
        return em.merge(object);
    }

    @Override
    public boolean deleteById(long id) {
        ProjectInvite toRemove = findById(id);
        em.remove(toRemove);
        return toRemove != null;
    }
}
