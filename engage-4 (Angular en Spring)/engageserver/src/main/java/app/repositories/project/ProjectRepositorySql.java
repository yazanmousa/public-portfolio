package app.repositories.project;

import app.models.project.Project;
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
 * Date 13/05/2021 19:02
 */
@org.springframework.stereotype.Repository
@Transactional
@Primary
public class ProjectRepositorySql implements Repository<Project> {
    @Autowired
    private EntityManager em;

    @Override
    public List<Project> findAll() {
        TypedQuery<Project> query = this.em.createQuery(
                "SELECT e from Project e", Project.class
        );
        return query.getResultList();
    }

    @Override
    public Project findById(long id) {
        return em.find(Project.class, id);
    }

    @Override
    public Project save(Project object) {
        return em.merge(object);
    }

    @Override
    public boolean deleteById(long id) {
        Project toRemove = findById(id);
        em.remove(toRemove);
        return toRemove != null;
    }
}
