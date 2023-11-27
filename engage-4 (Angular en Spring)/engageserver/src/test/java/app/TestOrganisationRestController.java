package app;

import app.models.organisation.Organisation;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDate;

@ExtendWith(SpringExtension.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class TestOrganisationRestController {

    @Autowired
    private TestRestTemplate restTemplate;

    //Lars
    @Test
    @DirtiesContext
    void postNewOrganisationReturnsResponseCreated() {
        Organisation organisationTest = new Organisation("lars", "test@test.com", "test",  LocalDate.of(2000,10,3), "assets/images/user.png", "the Netherlands");
        ResponseEntity<Organisation> result = this.restTemplate.postForEntity("/organisations", organisationTest, Organisation.class);
        assertEquals(result.getStatusCode(), HttpStatus.CREATED);

    }
}
