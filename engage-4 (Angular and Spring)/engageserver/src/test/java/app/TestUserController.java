package app;

import app.models.user.User;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
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
public class TestUserController {

    @Autowired
    private TestRestTemplate restTemplate;

    // Niek Boon
    @Test
    @DirtiesContext(methodMode = DirtiesContext.MethodMode.AFTER_METHOD)
    void postingNewUserShouldRespondWith201Created() {
        User user = new User("Niek", "Boon", "niek_boon@hotmail.com", "password", LocalDate.of(1998, 10, 28), "The Netherlands", "Very Cool User", "assets/images/user.png");
        ResponseEntity<User> postResult = this.restTemplate.postForEntity("/users", user, User.class);
        assertEquals(postResult.getStatusCode(), HttpStatus.CREATED);
    }

//    @Test
//    @DirtiesContext
//    void puttingUserWithWrongIdShouldThrowPreconditionFailed() {
//        User user = new User("Niek", "Boon", "niek_boon@hotmail.com", "password", LocalDate.of(1998, 10, 28), "The Netherlands", "Very Cool User", "assets/images/user.png");
//        user.setId(69420);
//
//        try {
//            this.restTemplate.put("/users/69419", user, User.class);
//        } catch (Exception e) {
//            System.out.println("HELLO MISTER CRABS");
//        }
//
//    }


}
