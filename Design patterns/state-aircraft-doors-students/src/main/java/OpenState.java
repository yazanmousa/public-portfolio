public class OpenState implements State {

    // The door associated with this state
    private final AircraftDoor door;

    /**
     * Constructor to initialize an OpenState with a given door.
     *
     * @param door The AircraftDoor associated with this state.
     */
    public OpenState(AircraftDoor door) {
        this.door = door;
    }

    @Override
    public String lockDoor() {
        // Cannot lock an open door
        return Messages.DOOR_CANNOT_PERFORM_THIS_ACTION;
    }

    @Override
    public String closeDoor() {
        // Transition to ClosedState
        door.setState(door.getClosedState());
        return Messages.CLOSED_STATE_MESSAGE;
    }

    @Override
    public String openDoor() {
        // Cannot open an already open door
        return Messages.DOOR_CANNOT_PERFORM_THIS_ACTION;
    }

    @Override
    public String armDoor() {
        // Cannot arm an open door
        return Messages.DOOR_CANNOT_PERFORM_THIS_ACTION;
    }

    @Override
    public String toString() {
        return Messages.OPEN_STATE_MESSAGE;
    }
}
