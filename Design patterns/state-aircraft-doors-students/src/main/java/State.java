public interface State {

    // Methods for different door actions
    String lockDoor(); // Lock the door
    String closeDoor(); // Close the door
    String openDoor(); // Open the door
    String armDoor(); // Arm the door

    // Default method for when slide is deployed (can be overridden by implementing classes)
    default String slideDeployed() {
        return Messages.DOOR_CANNOT_PERFORM_THIS_ACTION; // Default behavior is to return a message indicating action is not possible
    }

}
