package models;

public class Train {
    public final String origin;
    public final String destination;
    private final Locomotive engine;
    private Wagon firstWagon;
    private final int MINIMUM_VALUE_ZERO = 0;
    private final int ONE = 1;

    /* Representation invariants:
        firstWagon == null || firstWagon.previousWagon == null
        engine != null
     */

    public Train(Locomotive engine, String origin, String destination) {
        this.engine = engine;
        this.destination = destination;
        this.origin = origin;
    }

    /**
     * Indicates whether the train has at least one connected Wagon
     *
     * @return
     */
    public boolean hasWagons() {

        return firstWagon != null;   // replace by proper outcome
    }

    /**
     * A train is a passenger train when its first wagon is a PassengerWagon
     * (we do not worry about the posibility of mixed compositions here)
     *
     * @return
     */
    public boolean isPassengerTrain() {
        return firstWagon instanceof PassengerWagon;   // replace by proper outcome
    }

    /**
     * A train is a freight train when its first wagon is a FreightWagon
     * (we do not worry about the posibility of mixed compositions here)
     *
     * @return
     */
    public boolean isFreightTrain() {
        return firstWagon instanceof FreightWagon;  // replace by proper outcome
    }

    public Locomotive getEngine() {
        return engine;
    }

    public Wagon getFirstWagon() {

        return firstWagon;
    }

    /**
     * Replaces the current sequence of wagons (if any) in the train
     * by the given new sequence of wagons (if any)
     *
     * @param wagon the first wagon of a sequence of wagons to be attached (can be null)
     */
    public void setFirstWagon(Wagon wagon) {
        firstWagon = wagon;

    }

    /**
     * @return the number of Wagons connected to the train
     */
    public int getNumberOfWagons() {
        return firstWagon != null ? firstWagon.getSequenceLength() : 0;   // replace by proper outcome
    }

    /**
     * @return the last wagon attached to the train
     */
    public Wagon getLastWagonAttached() {
        Wagon wagon = firstWagon;

        if (firstWagon == null) {
            return null;
        }

        //Loop and get nextWagon until there is none
        while (wagon.hasNextWagon()) {
            wagon = wagon.getNextWagon();

        }
        return wagon;
    }

    /**
     * @return the total number of seats on a passenger train
     * (return 0 for a freight train)
     */
    public int getTotalNumberOfSeats() {
        if (!(firstWagon instanceof PassengerWagon)) {
            return 0;
        }

        Wagon wagon = firstWagon;
        int counter = 0;

        //Loop and get nextWagon until there is none
        //Meanwhile count all seats and return seats while casting wagon to Passenger wagon so that we can access numberOfSeats.
        while (wagon.hasNextWagon()) {
            counter += ((PassengerWagon) wagon).numberOfSeats;
            wagon = wagon.getNextWagon();
        }

        counter += ((PassengerWagon) wagon).numberOfSeats;

        return counter;   // replace by proper outcome
    }

    /**
     * calculates the total maximum weight of a freight train
     *
     * @return the total maximum weight of a freight train
     * (return 0 for a passenger train)
     */
    public int getTotalMaxWeight() {
        if (!(firstWagon instanceof FreightWagon)) {
            return 0;
        }

        Wagon wagon = firstWagon;
        int counter = 0;

        while (wagon.hasNextWagon()) {
            counter += ((FreightWagon) wagon).maxWeight;
            wagon = wagon.getNextWagon();
        }

        counter += ((FreightWagon) wagon).maxWeight;

        return counter;   // replace by proper outcome
    }

    /**
     * Finds the wagon at the given position (starting at 0 for the first wagon of the train)
     *
     * @param position
     * @return the wagon found at the given position
     * (return null if the position is not valid for this train)
     */
    public Wagon findWagonAtPosition(int position) {
        int i = MINIMUM_VALUE_ZERO;

        if (firstWagon == null) {
            return null;
        }

        Wagon currentWagon = firstWagon;

        //Loop through wagon sequence and check if position matches wagon loop count
        while (currentWagon.hasNextWagon()) {
            if (position == i) {
                return currentWagon;
            } else {
                i++;
                currentWagon = currentWagon.getNextWagon();
            }

        }

        //Extra check for last wagon
        if (position == i) {
            return currentWagon;
        }

        return null;    // replace by proper outcome
    }

    /**
     * Finds the wagon with a given wagonId
     *
     * @param wagonId
     * @return the wagon found
     * (return null if no wagon was found with the given wagonId)
     */
    public Wagon findWagonById(int wagonId) {
        if (firstWagon == null) {
            return null;
        }

        Wagon currentWagon = firstWagon;
        while (currentWagon.hasNextWagon()) {
            if (currentWagon.id == wagonId) {
                return currentWagon;
            }
            currentWagon = currentWagon.getNextWagon();
        }

        //Extra check for last wagon
        if (currentWagon.id == wagonId) {
            return currentWagon;
        }

        return null;
    }

    /**
     * Determines if the given sequence of wagons can be attached to this train
     * Verifies if the type of wagons match the type of train (Passenger or Freight)
     * Verifies that the capacity of the engine is sufficient to also pull the additional wagons
     * Verifies that the wagon is not part of the train already
     * Ignores the predecessors before the head wagon, if any
     *
     * @param wagon the head wagon of a sequence of wagons to consider for attachment
     * @return whether type and capacity of this train can accommodate attachment of the sequence
     */
    public boolean canAttach(Wagon wagon) {
        if (firstWagon == null) {
            return true;
        }

        return firstWagon.getSequenceLength() + wagon.getSequenceLength() <= engine.getMaxWagons() && findWagonById(wagon.id) == null && wagon.getClass().equals(firstWagon.getClass());

    }

    /**
     * Tries to attach the given sequence of wagons to the rear of the train
     * No change is made if the attachment cannot be made.
     * (when the sequence is not compatible or the engine has insufficient capacity)
     * if attachment is possible, the head wagon is first detached from its predecessors, if any
     *
     * @param wagon the head wagon of a sequence of wagons to be attached
     * @return whether the attachment could be completed successfully
     */
    public boolean attachToRear(Wagon wagon) {
        //Íf there is no firstwagon, detach any wagon before given wagon and set it as the first wagon
        if (firstWagon == null) {
            if (wagon.hasPreviousWagon()) {
                wagon.detachFront();
            }

            setFirstWagon(wagon);
            return true;
        }

        //Check compatibility
        if (canAttach(wagon)) {

            if (wagon.hasPreviousWagon()) wagon.detachFront();
            firstWagon.getLastWagonAttached().attachTail(wagon);
            return true;
        }

        return false;
    }

    /**
     * Tries to insert the given sequence of wagons at the front of the train
     * (the front is at position one, before the current first wagon, if any)
     * No change is made if the insertion cannot be made.
     * (when the sequence is not compatible or the engine has insufficient capacity)
     * if insertion is possible, the head wagon is first detached from its predecessors, if any
     *
     * @param wagon the head wagon of a sequence of wagons to be inserted
     * @return whether the insertion could be completed successfully
     */
    public boolean insertAtFront(Wagon wagon) {
        if (firstWagon == null && wagon.getSequenceLength() <= engine.getMaxWagons()) {
            attachToRear(wagon);
            return true;
        }

        //Check compatibility
        if (canAttach(wagon)) {

            //Detach front of given wagon and get last wagon attached so that we can attach first wagon at the tail
            wagon.detachFront();
            Wagon currentFirstWagon = firstWagon;
            setFirstWagon(wagon);
            wagon.getLastWagonAttached().attachTail(currentFirstWagon);

            return true;
        }
        return false;
    }

    /**
     * Tries to insert the given sequence of wagons at/before the given position in the train.
     * (The current wagon at given position including all its successors shall then be reattached
     * after the last wagon of the given sequence.)
     * No change is made if the insertion cannot be made.
     * (when the sequence is not compatible or the engine has insufficient capacity
     * or the given position is not valid for insertion into this train)
     * if insertion is possible, the head wagon of the sequence is first detached from its predecessors, if any
     *
     * @param position the position where the head wagon and its successors shall be inserted
     *                 0 <= position <= numWagons
     *                 (i.e. insertion immediately after the last wagon is also possible)
     * @param wagon    the head wagon of a sequence of wagons to be inserted
     * @return whether the insertion could be completed successfully
     */
    public boolean insertAtPosition(int position, Wagon wagon) {
        if (firstWagon == null) {
            //No wagon found
            attachToRear(wagon);
            setFirstWagon(findWagonAtPosition(MINIMUM_VALUE_ZERO));
            return true;
        }

        //If wagon.id is found it's a duplicate, so it cannot insert
        if (findWagonById(wagon.id) != null) {
            return false;
        }

        //If wagon has a wagon at front, remove it
        if (wagon.hasPreviousWagon()) {
            wagon.detachFront();
        }

        if (canAttach(wagon) && position < engine.getMaxWagons() && position >= MINIMUM_VALUE_ZERO) {
            //there's currently no wagon at given position

            if (findWagonAtPosition(position) != null) {
                // No free spot, remove wagon at given position
                Wagon foundWagon = findWagonAtPosition(position);

                //If the foundwagon is the firstwagon in sequence
                if (!foundWagon.hasPreviousWagon()) {
                    wagon.detachFront();
                    foundWagon.detachFront();
                    wagon.getLastWagonAttached().attachTail(foundWagon);
                    setFirstWagon(wagon);
                    return true;
                }

                //Detachfront
                foundWagon.detachFront();
                wagon.getLastWagonAttached().attachTail(foundWagon);

            }  // Free spot
                //lets check if the pos is bigger than to sequenceLength +1 because then the position is invalid
            if (position > firstWagon.getSequenceLength() + ONE){
                return false;
            }

            firstWagon.getLastWagonAttached().attachTail(wagon);
            return true;
        }

        return false;
    }

    /**
     * Tries to remove one Wagon with the given wagonId from this train
     * and attach it at the rear of the given toTrain
     * No change is made if the removal or attachment cannot be made
     * (when the wagon cannot be found, or the trains are not compatible
     * or the engine of toTrain has insufficient capacity)
     *
     * @param wagonId the id of the wagon to be removed
     * @param toTrain the train to which the wagon shall be attached
     *                toTrain shall be different from this train
     * @return whether the move could be completed successfully
     */
    public boolean moveOneWagon(int wagonId, Train toTrain) {
        if (findWagonById(wagonId) != null) {

            //Wagons needed
            Wagon foundWagon = findWagonById(wagonId);
            Wagon previous = foundWagon.getPreviousWagon();
            Wagon next = foundWagon.getNextWagon();

            //Check if wagons are compatible
            if (this.getNumberOfWagons() > ONE && toTrain.getTotalMaxWeight() > ONE
                    || foundWagon.getSequenceLength() +
                    toTrain.getNumberOfWagons() > toTrain.getEngine().getMaxWagons()) {
                return false;
            }

            //Check for firstwagon
            if (foundWagon == firstWagon) {
                //Detach firstwagon completely and attach it to the rear of given train
                firstWagon.detachFront();
                firstWagon.detachTail();
                toTrain.attachToRear(firstWagon);
                setFirstWagon(next);
                return true;
            }

            //Detach found wagon completely and attach it to the rear of given train
            foundWagon.detachFront();
            foundWagon.detachTail();
            toTrain.attachToRear(foundWagon);
            if (previous != null && next != null) {
                previous.attachTail(next);
            }
            return true;
        }

        //We do not want the wagon because it is available already
        return false;
    }

    /**
     * Tries to split this train before the wagon at given position and move the complete sequence
     * of wagons from the given position to the rear of toTrain.
     * No change is made if the split or re-attachment cannot be made
     * (when the position is not valid for this train, or the trains are not compatible
     * or the engine of toTrain has insufficient capacity)
     *
     * @param position 0 <= position < numWagons
     * @param toTrain  the train to which the split sequence shall be attached
     *                 toTrain shall be different from this train
     * @return whether the move could be completed successfully
     */
    public boolean splitAtPosition(int position, Train toTrain) {
        if (firstWagon == null) {
            //No wagon found so we cannot split
            return false;
        }

        //No wagons to split at, return false
        if (!this.hasWagons()) {
            return false;
        }

        if (findWagonAtPosition(position) != null) {
            //If it does not return null, we get a position meaning that we have to split the train at that point
            Wagon foundWagon = findWagonAtPosition(position);

            //We know that a train must either carry wagons or weight in order to be seen as a freight or passenger wagon, so we use this information to check against each other
            //Can attach method also works
            if (this.getNumberOfWagons() > 1 && toTrain.getTotalMaxWeight() > 1 || foundWagon.getSequenceLength() + toTrain.getNumberOfWagons() > toTrain.getEngine().getMaxWagons()) {
                return false;
            }

            if (foundWagon == firstWagon) {
                firstWagon.detachFront();
                setFirstWagon(null);
                toTrain.attachToRear(foundWagon);
            }

            foundWagon.detachFront();
            toTrain.attachToRear(foundWagon);

            return true;
        }

        return false;   // replace by proper outcome
    }

    /**
     * Reverses the sequence of wagons in this train (if any)
     * i.e. the last wagon becomes the first wagon
     * the previous wagon of the last wagon becomes the second wagon
     * etc.
     * (No change if the train has no wagons or only one wagon)
     */
    public void reverse() {
        if (firstWagon == null){
            return;
        }
        Wagon oldLastWagon = firstWagon.getLastWagonAttached();
        firstWagon.reverseSequence();
        firstWagon = oldLastWagon;
    }

    @Override
    public String toString() {
        return "[Loc-" + engine.getLocNumber() + "]" + returnRepresentationOfWagons() + " with " + this.getNumberOfWagons() + " wagons from " + origin + " to " + destination;
    }
    public String returnRepresentationOfWagons() {
        StringBuilder stringBuilder = new StringBuilder();

        Wagon currentWagon = firstWagon;
        while (currentWagon.hasNextWagon()) {
            stringBuilder.append(currentWagon);
            currentWagon = currentWagon.getNextWagon();

        }
        //Don't forget to print last wagon

        if (!currentWagon.hasNextWagon()) {
            stringBuilder.append(currentWagon);
        }
        return stringBuilder.toString();
    }

}
