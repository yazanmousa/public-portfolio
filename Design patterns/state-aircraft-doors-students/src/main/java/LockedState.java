public class LockedState implements State {

    // The door associated with this state
    private final AircraftDoor door;

    /**
     * Constructor to initialize a LockedState with a given door.
     *
     * @param door The AircraftDoor associated with this state.
     */
    public LockedState(AircraftDoor door) {
        this.door = door;
    }

    @Override
    public String lockDoor() {
        // Cannot lock an already locked door
        return Messages.DOOR_CANNOT_PERFORM_THIS_ACTION;
    }

    @Override
    public String closeDoor() {
        // Cannot close a locked door
        return Messages.DOOR_CANNOT_PERFORM_THIS_ACTION;
    }

    @Override
    public String openDoor() {
        // Cannot open a locked door
        return Messages.DOOR_CANNOT_PERFORM_THIS_ACTION;
    }

    @Override
    public String armDoor() {
        // Transition to ArmedState
        door.setState(door.getArmedState());
        return Messages.ARMED_STATE_MESSAGE;
    }

    @Override
    public String toString() {
        return Messages.LOCKED_STATE_MESSAGE;
    }
}
