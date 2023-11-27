public class AircraftDoor {

    // Unique identifier for the door
    private String id;

    // The current state of the door
    private State state;

    // Different states of the door
    private ArmedState armedState;
    private ClosedState closedState;
    private LockedState lockedState;
    private OpenState openState;
    private SlideDeployedState slideDeployedState;

    /**
     * Constructor to initialize an AircraftDoor with a given ID.
     *
     * @param id The unique identifier for the door.
     */
    public AircraftDoor(String id) {
        this.id = id;

        // Initialize different states
        this.armedState = new ArmedState(this);
        this.closedState = new ClosedState(this);
        this.lockedState = new LockedState(this);
        this.openState = new OpenState(this);
        this.slideDeployedState = new SlideDeployedState(this);

        // Set the initial state to open
        this.state = openState;
    }

    /**
     * Attempt to open the door.
     *
     * @return The message indicating the result of the operation.
     */
    public String openDoor(){
        return state.openDoor();
    }

    /**
     * Attempt to close the door.
     *
     * @return The message indicating the result of the operation.
     */
    public String closeDoor() {
        return this.state.closeDoor();
    }

    /**
     * Attempt to arm the door.
     *
     * @return The message indicating the result of the operation.
     */
    public String armDoor() {
        return state.armDoor();
    }

    /**
     * Attempt to lock the door.
     *
     * @return The message indicating the result of the operation.
     */
    public String lockDoor() {
        return state.lockDoor();
    }

    /**
     * Set the current state of the door.
     *
     * @param state The new state of the door.
     */
    void setState(State state) {
        this.state = state;
    }

    /**
     * Get the current state of the door.
     *
     * @return The current state of the door.
     */
    public State getState() {
        return this.state;
    }

    // Getter methods for different states
    public State getOpenState() { return this.openState; }
    public State getClosedState() { return this.closedState; }
    public State getLockedState() { return this.lockedState; }
    public State getArmedState() { return this.armedState; }
    public State getDeployedState() { return this.slideDeployedState; }

    /**
     * String representation of the AircraftDoor object.
     *
     * @return A string describing the state of the door.
     */
    public String toString() {
        StringBuilder status = new StringBuilder();
        status.append("\nAircraft Door: " + id);
        status.append("\n");
        status.append("State is " + state + "\n");
        return status.toString();
    }
}
