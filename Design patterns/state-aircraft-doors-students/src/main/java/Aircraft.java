public class Aircraft {

    private AircraftDoor cabinDoor1; // The cabin door of the aircraft
    private String type; // The type of the aircraft

    /**
     * Constructor to initialize the Aircraft object.
     * @param type The type of the aircraft.
     */
    public Aircraft(String type) {
        this.type = type;
        cabinDoor1 = new AircraftDoor("Cabin Door 1");
    }

    /**
     * Getter method to retrieve the cabin door of the aircraft.
     * @return The cabin door object.
     */
    public AircraftDoor getCabinDoor1() {
        return cabinDoor1;
    }

    /**
     * Override of the toString() method to provide a custom string representation of the Aircraft object.
     * @return A formatted string representing the aircraft.
     */
    @Override
    public String toString() {
        return "Aircraft: " + type + ": " + cabinDoor1;
    }
}
