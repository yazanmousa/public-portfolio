package app;

import app.models.organisation.Organisation;
import app.models.project.Project;
import app.repositories.Repository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;
import static org.junit.jupiter.api.Assertions.*;
import java.time.LocalDate;
import java.util.List;

@SpringBootTest
public class TestOrganisationRepository {

    @Autowired
    private Repository<Organisation> organisationRepository;

    //Lars

    @Test
    void testGetOrganisations() {
        List<Organisation> organisations = organisationRepository.findAll();
        assertEquals(organisations, 4);
    }


    @Test
    @DirtiesContext
    void testAddingOrganisation() {

        Organisation organisationTest = new Organisation("lars", "test@test.com", "test",  LocalDate.of(2000,10,3), "", "the Netherlands");
        Organisation organisationSaved = organisationRepository.save(organisationTest);

        assertNotNull(organisationSaved);
        assertEquals(organisationSaved.getEmail(), "test@test.com");

    }

    @Test
    @DirtiesContext
    void testDeleteOrganisation() {
        organisationRepository.deleteById(1683);
        assertNull(organisationRepository.findById(1683));
    }

    @Test
    @DirtiesContext
    void testUpdateOrganisation() {
        Organisation organisationTest = new Organisation("lars", "test@test.com", "test",  LocalDate.of(2000,10,3), "", "the Netherlands");
        Organisation organisationSaved = organisationRepository.save(organisationTest);
        assertNotNull(organisationSaved);

        Organisation updatedOrganisation = new Organisation("Tommy", "test@test.com", "test",  LocalDate.of(2000,10,3), "", "the Netherlands");
        updatedOrganisation.setId(organisationSaved.getId());
        organisationRepository.save(updatedOrganisation);
        assertEquals(organisationRepository.findById(organisationSaved.getId()).getName(), "Tommy");
    }
}
