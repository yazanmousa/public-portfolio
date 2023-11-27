package app;

import app.models.user.User;
import app.repositories.Repository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;
import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDate;
import java.util.List;

@SpringBootTest
class TestUserRepository {

    @Autowired
    private Repository<User> userRepository;

    // Niek Boon
    @Test
    @DirtiesContext
    void testAddingOneUser() {

        User user1 = new User("Niek", "Boon", "niek_boon@hotmail.com", "password", LocalDate.of(1998, 10, 28), "The Netherlands", "Very Cool User", "assets/images/user.png");
        User user1Saved = userRepository.save(user1);

        assertNotEquals(user1Saved.getId(), 0);
        assertNotNull(user1Saved);
        assertEquals(user1Saved.getFirstName(), "Niek");
        assertEquals(user1Saved.getEmail(), "niek_boon@hotmail.com");

        userRepository.deleteById(user1Saved.getId());
        assertNull(userRepository.findById(user1Saved.getId()));
    }

    // Niek Boon
    @Test
    @DirtiesContext
    void testUpdatingOneUser() {
        User user1 = new User("Niek", "Boon", "niek_boon@hotmail.com", "password", LocalDate.of(1998, 10, 28), "The Netherlands", "Very Cool User", "assets/images/user.png");
        User user1Saved = userRepository.save(user1);

        assertNotNull(user1Saved);

        User toUpdate = new User("Henk", "Boon", "niek_boon@hotmail.com", "password", LocalDate.of(1998, 10, 28), "The Netherlands", "Very Cool User", "assets/images/user.png");
        toUpdate.setId(user1Saved.getId());

        userRepository.save(toUpdate);

        assertEquals(userRepository.findById(user1Saved.getId()).getFirstName(), "Henk");

        // Delete test additions to the database
        userRepository.deleteById(user1Saved.getId());
        assertNull(userRepository.findById(user1Saved.getId()));
    }

    // Niek Boon
    @Test
    void testGettingAllUsers() {
        List<User> users = userRepository.findAll();
        assertEquals(users.size(), 6);
    }

    // Niek Boon
    @Test
    @DirtiesContext
    void testIdIsCorrectlyIncremented() {
        User user1 = new User("Niek", "Boon", "niek_boon@hotmail.com", "password", LocalDate.of(1998, 10, 28), "The Netherlands", "Very Cool User", "assets/images/user.png");
        User user2 = new User("Lars", "Smeets", "lars.smeets@hotmail.com", "password", LocalDate.of(1999, 10, 28), "Sri Lanka", "The best user ever!", "assets/images/man.png");

        User user1Saved = userRepository.save(user1);
        User user2Saved = userRepository.save(user2);

        assertNotNull(user1Saved);
        assertNotNull(user2Saved);
        assertEquals(user2Saved.getId(), user1Saved.getId() + 1);

        // Delete test additions to the database
        userRepository.deleteById(user1Saved.getId());
        userRepository.deleteById(user2Saved.getId());
        assertNull(userRepository.findById(user1Saved.getId()));
        assertNull(userRepository.findById(user2Saved.getId()));
    }

}
