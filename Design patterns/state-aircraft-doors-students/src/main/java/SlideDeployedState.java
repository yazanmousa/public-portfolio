public class SlideDeployedState implements State {

    // The door associated with this state
    private final AircraftDoor door;

    /**
     * Constructor to initialize a SlideDeployedState with a given door.
     *
     * @param door The AircraftDoor associated with this state.
     */
    public SlideDeployedState(AircraftDoor door) {
        this.door = door;
    }

    @Override
    public String lockDoor() {
        // Slide deployed, door needs resetting
        return Messages.DOOR_NEEDS_RESETTING;
    }

    @Override
    public String closeDoor() {
        // Slide deployed, door needs resetting
        return Messages.DOOR_NEEDS_RESETTING;
    }

    @Override
    public String openDoor() {
        // Slide deployed, door needs resetting
        return Messages.DOOR_NEEDS_RESETTING;
    }

    @Override
    public String armDoor() {
        // Slide deployed, door needs resetting
        return Messages.DOOR_NEEDS_RESETTING;
    }

    @Override
    public String slideDeployed() {
        return State.super.slideDeployed(); // Calling default behavior
    }

    @Override
    public String toString() {
        return Messages.SLIDE_DEPLOYED;
    }
}
