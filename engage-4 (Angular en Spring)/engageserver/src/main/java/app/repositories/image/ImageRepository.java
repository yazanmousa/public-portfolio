package app.repositories.image;

import app.models.image.ImageModel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * @author Yazan
 * Date 12/05/2021 13:11
 */
@Repository
public interface ImageRepository extends JpaRepository<ImageModel, Long> {
    Optional<ImageModel> findByName(String name);

    Optional<ImageModel> findByUser_id(long userId);

}
