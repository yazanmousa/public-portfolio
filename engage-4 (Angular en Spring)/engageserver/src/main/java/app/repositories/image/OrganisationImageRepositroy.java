package app.repositories.image;

import app.models.image.ImageOrganisation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * @author Yazan
 * Date 24/05/2021 13:21
 */
@Repository
public interface OrganisationImageRepositroy extends JpaRepository<ImageOrganisation, Long> {

    Optional<ImageOrganisation> findByOrganisationId(long organisationId);


}
