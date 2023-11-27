package app.repositories.project;

import app.models.project.ProjectMember;
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
public class ProjectMemberRepositorySql implements Repository<ProjectMember> {

    @Autowired
    EntityManager em;

    @Override
    public List<ProjectMember> findAll() {
        TypedQuery<ProjectMember> query = this.em.createQuery(
                "SELECT p from ProjectMember p", ProjectMember.class
        );
        return query.getResultList();
    }

    @Override
    public ProjectMember findById(long id) {
        return em.find(ProjectMember.class, id);
    }

    @Override
    public ProjectMember save(ProjectMember object) {
        return em.merge(object);
    }

    @Override
    public boolean deleteById(long id) {
        ProjectMember toRemove = findById(id);
        em.remove(toRemove);
        return toRemove != null;
    }
}
