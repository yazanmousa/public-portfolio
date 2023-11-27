package app.repositories.image;

import app.models.image.ImageProject;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * @author Yazan
 * Date 24/05/2021 13:54
 */

@Repository
public interface ProjectImageRepositroy extends JpaRepository<ImageProject, Long> {
    Optional<ImageProject> findByProjectId(long projectId);
}
