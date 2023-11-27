public class ClosedState implements State {

    // The door associated with this state
    private final AircraftDoor door;

    /**
     * Constructor to initialize a ClosedState with a given door.
     *
     * @param door The AircraftDoor associated with this state.
     */
    public ClosedState(AircraftDoor door) {
        this.door = door;
    }

    @Override
    public String lockDoor() {
        // Cannot lock a closed door
        return Messages.DOOR_CANNOT_PERFORM_THIS_ACTION;
    }

    @Override
    public String closeDoor() {
        // Cannot close an already closed door
        return Messages.DOOR_CANNOT_PERFORM_THIS_ACTION;
    }

    @Override
    public String openDoor() {
        // Transition to OpenState
        door.setState(door.getOpenState());
        return Messages.OPEN_STATE_MESSAGE;
    }

    @Override
    public String armDoor() {
        // Transition to ArmedState
        door.setState(door.getArmedState());
        return Messages.ARMED_STATE_MESSAGE;
    }

    @Override
    public String toString() {
        return Messages.CLOSED_STATE_MESSAGE;
    }
}
