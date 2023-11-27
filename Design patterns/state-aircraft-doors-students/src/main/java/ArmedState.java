public class ArmedState implements State {

    // The door associated with this state
    private final AircraftDoor door;

    /**
     * Constructor to initialize an ArmedState with a given door.
     *
     * @param door The AircraftDoor associated with this state.
     */
    public ArmedState(AircraftDoor door) {
        this.door = door;
    }

    @Override
    public String lockDoor() {
        // Transition to LockedState
        door.setState(door.getLockedState());
        return Messages.LOCKED_STATE_MESSAGE;
    }

    @Override
    public String closeDoor() {
        // Transition to ClosedState
        door.setState(door.getClosedState());
        return Messages.CLOSED_STATE_MESSAGE;
    }

    @Override
    public String openDoor() {
        // Transition to SlideDeployedState
        door.setState(door.getDeployedState());
        return Messages.SLIDE_DEPLOYED;
    }

    @Override
    public String armDoor() {
        // Cannot arm an already armed door
        return Messages.CLOSED_STATE_MESSAGE;
    }

    @Override
    public String toString() {
        return Messages.ARMED_STATE_MESSAGE;
    }
}
