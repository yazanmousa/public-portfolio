public class AircraftDoorDemo {

    /**
     * The main method to demonstrate the behavior of the aircraft door in different scenarios.
     * @param args Command line arguments (not used in this program).
     */
    public static void main(String args[]) {
        // Create an aircraft of type "VC10"
        Aircraft aircraft = new Aircraft("VC10");

        // Normal flight scenarios
        printState(aircraft);
        aircraft.getCabinDoor1().closeDoor();
        printState(aircraft);
        aircraft.getCabinDoor1().armDoor();
        printState(aircraft);
        aircraft.getCabinDoor1().lockDoor();
        printState(aircraft);
        aircraft.getCabinDoor1().armDoor();
        printState(aircraft);
        aircraft.getCabinDoor1().closeDoor();
        printState(aircraft);
        aircraft.getCabinDoor1().openDoor();
        printState(aircraft);

        // Emergency scenarios
        printState(aircraft);
        aircraft.getCabinDoor1().closeDoor();
        printState(aircraft);
        aircraft.getCabinDoor1().armDoor();
        printState(aircraft);
        aircraft.getCabinDoor1().lockDoor();
        printState(aircraft);
        aircraft.getCabinDoor1().armDoor();
        printState(aircraft);
        aircraft.getCabinDoor1().openDoor();
        printState(aircraft);
    }

    /**
     * Print the current state of the aircraft.
     * @param aircraft The aircraft object to be printed.
     */
    public static void printState(Aircraft aircraft) {
        System.out.println(aircraft.toString());
    }
}
