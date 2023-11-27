import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class DoorStateTest {
    AircraftDoor aircraftDoor1;
    @BeforeEach
    void setup(){
        aircraftDoor1 = new AircraftDoor("Cabin Door 1");
    }

    @Test
    void intialStateMustBeOpen(){
        assert(aircraftDoor1.getState() instanceof OpenState);
        assertEquals ( Messages.OPEN_STATE_MESSAGE, aircraftDoor1.getState().toString());
    }

    @Test
    void statesReportCorrectMessage(){
        assertEquals(Messages.OPEN_STATE_MESSAGE, aircraftDoor1.getOpenState().toString());
        assertEquals(Messages.CLOSED_STATE_MESSAGE, aircraftDoor1.getClosedState().toString());
        assertEquals(Messages.ARMED_STATE_MESSAGE, aircraftDoor1.getArmedState().toString());
        assertEquals(Messages.LOCKED_STATE_MESSAGE, aircraftDoor1.getLockedState().toString());
        assertEquals(Messages.SLIDE_DEPLOYED, aircraftDoor1.getDeployedState().toString());
    }
    /**
     * The door should only be able to move from open to closed to armed to locked.  Once locked it can only move
     * from locked to armed (which is unlocked).  In normal circumstance, a door can then be moved from
     * armed to closed (disarmed) and then open.  Opening an armed door is done in an emergency which deploys
     * an evacuation slide.  A door in a SlideDeployedState cannot move to any other state.
     */
    @Test
    void allSequencesCorrect(){
        assert(aircraftDoor1.getState() instanceof OpenState);
        assertEquals(Messages.CLOSED_STATE_MESSAGE, aircraftDoor1.closeDoor());
        assert(aircraftDoor1.getState() instanceof ClosedState);
        assertEquals(Messages.ARMED_STATE_MESSAGE, aircraftDoor1.armDoor());
        assert(aircraftDoor1.getState() instanceof ArmedState);
        assertEquals(Messages.LOCKED_STATE_MESSAGE, aircraftDoor1.lockDoor());
        assert(aircraftDoor1.getState() instanceof LockedState);
        assertEquals(Messages.ARMED_STATE_MESSAGE, aircraftDoor1.armDoor());
        assert(aircraftDoor1.getState() instanceof ArmedState);
        assertEquals(Messages.CLOSED_STATE_MESSAGE, aircraftDoor1.closeDoor());
        assert(aircraftDoor1.getState() instanceof ClosedState);
        assertEquals(Messages.OPEN_STATE_MESSAGE, aircraftDoor1.openDoor());
        assert(aircraftDoor1.getState() instanceof OpenState);
    }
    @Test
    void sequenceMustBeCorrect(){
        assert(aircraftDoor1.getState() instanceof OpenState);
        aircraftDoor1.armDoor();
        aircraftDoor1.lockDoor();
        assert(aircraftDoor1.getState() instanceof OpenState);

        aircraftDoor1.closeDoor();
        aircraftDoor1.lockDoor();
        assert(aircraftDoor1.getState() instanceof ClosedState);

        aircraftDoor1.armDoor();
        aircraftDoor1.lockDoor();
        assert(aircraftDoor1.getState() instanceof LockedState);

    }

    @Test
    void openCannotBeOpened(){
        assert(aircraftDoor1.getState() instanceof OpenState);
        assertEquals(Messages.DOOR_CANNOT_PERFORM_THIS_ACTION, aircraftDoor1.openDoor());
        assert(aircraftDoor1.getState() instanceof OpenState);
    }
    @Test
    void openCanBeClosed(){
        assert(aircraftDoor1.getState() instanceof OpenState);
        assertEquals (Messages.CLOSED_STATE_MESSAGE, aircraftDoor1.closeDoor());
        assert(aircraftDoor1.getState() instanceof ClosedState);
    }
    @Test
    void openCannotBeLocked(){
        assert(aircraftDoor1.getState() instanceof OpenState);
        assertEquals(Messages.DOOR_CANNOT_PERFORM_THIS_ACTION, aircraftDoor1.lockDoor());
        assert(aircraftDoor1.getState() instanceof OpenState);
    }
    @Test
    void openCannotBeArmed(){
        assert(aircraftDoor1.getState() instanceof OpenState);
        assertEquals(Messages.DOOR_CANNOT_PERFORM_THIS_ACTION, aircraftDoor1.armDoor());
        assert(aircraftDoor1.getState() instanceof OpenState);
    }
    @Test
    void closedCannotBeLocked(){
        aircraftDoor1.closeDoor();
        assert(aircraftDoor1.getState() instanceof ClosedState);
        assertEquals(Messages.DOOR_CANNOT_PERFORM_THIS_ACTION, aircraftDoor1.lockDoor());
        assert(aircraftDoor1.getState() instanceof ClosedState);
    }
    @Test
    void closedCanBeOpened(){
        aircraftDoor1.closeDoor();
        assert(aircraftDoor1.getState() instanceof ClosedState);
        assertEquals(Messages.OPEN_STATE_MESSAGE, aircraftDoor1.openDoor());
        assert(aircraftDoor1.getState() instanceof OpenState);
    }
    @Test
    void closedCanBeArmed(){
        aircraftDoor1.closeDoor();
        assert(aircraftDoor1.getState() instanceof ClosedState);
        assertEquals(Messages.ARMED_STATE_MESSAGE, aircraftDoor1.armDoor());
        assert(aircraftDoor1.getState() instanceof ArmedState);
    }

    @Test
    void lockedCannotBeClosed(){
        aircraftDoor1.closeDoor();
        aircraftDoor1.armDoor();
        aircraftDoor1.lockDoor();
        assert(aircraftDoor1.getState() instanceof LockedState);
        assertEquals(Messages.DOOR_CANNOT_PERFORM_THIS_ACTION, aircraftDoor1.closeDoor());
        assert(aircraftDoor1.getState() instanceof LockedState);
    }

    @Test
    void lockedCanBeChangedToArmed(){
        aircraftDoor1.closeDoor();
        aircraftDoor1.armDoor();
        aircraftDoor1.lockDoor();
        assert(aircraftDoor1.getState() instanceof LockedState);
       assertEquals(Messages.ARMED_STATE_MESSAGE, aircraftDoor1.armDoor());
       assert(aircraftDoor1.getState() instanceof ArmedState);
    }
    @Test
    void armedCanBeLocked(){
        aircraftDoor1.closeDoor();
        aircraftDoor1.armDoor();
        assert(aircraftDoor1.getState() instanceof ArmedState);
        assertTrue(Messages.ARMED_STATE_MESSAGE.equals(aircraftDoor1.getState().toString()));
        assertEquals(Messages.LOCKED_STATE_MESSAGE, aircraftDoor1.lockDoor());
        assert(aircraftDoor1.getState() instanceof LockedState);
    }
    //Opening a armed door causes the emergency slide to be deployed.  This is why pilots give the
    //instruction to the crew to disarm the doors when an aircraft is near the airport gate.
    @Test
    void openingArmedDoorDeploysSlide(){
        aircraftDoor1.closeDoor();
        aircraftDoor1.armDoor();
        assert(aircraftDoor1.getState() instanceof ArmedState);
        assertEquals(Messages.SLIDE_DEPLOYED, aircraftDoor1.openDoor());
        assert(aircraftDoor1.getState() instanceof SlideDeployedState);
    }
    //Once a slide is deployed the door cannot move to any other state.
    @Test
    void deployedSlideCannotChangeState(){
        aircraftDoor1.closeDoor();
        aircraftDoor1.armDoor();
        assertEquals(Messages.SLIDE_DEPLOYED, aircraftDoor1.openDoor());
        assert(aircraftDoor1.getState() instanceof SlideDeployedState);
        assertEquals(Messages.DOOR_NEEDS_RESETTING, aircraftDoor1.closeDoor());
        assert(aircraftDoor1.getState() instanceof SlideDeployedState);
        assertEquals(Messages.DOOR_NEEDS_RESETTING, aircraftDoor1.armDoor());
        assert(aircraftDoor1.getState() instanceof SlideDeployedState);
        assertEquals(Messages.DOOR_NEEDS_RESETTING, aircraftDoor1.openDoor());
        assert(aircraftDoor1.getState() instanceof SlideDeployedState);
        assertEquals(Messages.DOOR_NEEDS_RESETTING, aircraftDoor1.lockDoor());
        assert(aircraftDoor1.getState() instanceof SlideDeployedState);
    }


}
