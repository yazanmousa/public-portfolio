package models;

public abstract class Wagon {
    protected int id;               // some unique ID of a Wagon
    private Wagon nextWagon;        // another wagon that is appended at the tail of this wagon
                                    // a.k.a. the successor of this wagon in a sequence
                                    // set to null if no successor is connected
    private Wagon previousWagon;    // another wagon that is prepended at the front of this wagon
                                    // a.k.a. the predecessor of this wagon in a sequence
                                    // set to null if no predecessor is connected

    // representation invariant propositions:
    // tail-connection-invariant:   wagon.nextWagon == null or wagon == wagon.nextWagon.previousWagon
    // front-connection-invariant:  wagon.previousWagon == null or wagon = wagon.previousWagon.nextWagon

    public Wagon (int wagonId) {
        this.id = wagonId;
    }

    public int getId() {
        return id;
    }

    public Wagon getNextWagon() {
        return nextWagon;
    }

    public Wagon getPreviousWagon() {
        return previousWagon;
    }

    /**
     * @return  whether this wagon has a wagon appended at the tail
     */
    public boolean hasNextWagon() {
        return !(nextWagon == null);
    }

    /**
     * @return  whether this wagon has a wagon prepended at the front
     */
    public boolean hasPreviousWagon() {
        return !(previousWagon == null);
    }

    /**
     * Returns the last wagon attached to it,
     * if there are no wagons attached to it then this wagon is the last wagon.
     * @return  the last wagon
     */
    public Wagon getLastWagonAttached() {
        Wagon currentLastWagon = this;
        if (hasNextWagon()){
            currentLastWagon = nextWagon.getLastWagonAttached();
        }
        return currentLastWagon;
    }

    /**
     * @return  the length of the sequence of wagons towards the end of its tail
     * including this wagon itself.
     */
    public int getSequenceLength() {
        if (hasNextWagon()){
            return 1 + nextWagon.getSequenceLength();
        }
        return 1; // if there are no next wagons. There is only one wagon in the sequence.
    }

    /**
     * Attaches the tail wagon and its connected successors behind this wagon,
     * if and only if this wagon has no wagon attached at its tail
     * and if the tail wagon has no wagon attached in front of it.
     * @param tail the wagon to attach behind this wagon.
     * @throws IllegalStateException if this wagon already has a wagon appended to it.
     * @throws IllegalStateException if tail is already attached to a wagon in front of it.
     *          The exception should include a message that reports the conflicting connection,
     *          e.g.: "%s is already pulling %s"
     *          or:   "%s has already been attached to %s"
     */
    public void attachTail(Wagon tail) {

        if (!this.hasNextWagon() && !tail.hasPreviousWagon()){
            tail.previousWagon = this;
            nextWagon = tail;
            return;
        }
        if (hasNextWagon()){
            throw new IllegalStateException(toString() + "is already pulling" + nextWagon.toString());
        }
        if (tail.hasPreviousWagon()){
            throw new IllegalStateException(tail.toString() + "has already been attached to" + tail.previousWagon.toString());
        }
    }

    /**
     * Detaches the tail from this wagon and returns the first wagon of this tail.
     * @return the first wagon of the tail that has been detached
     *          or <code>null</code> if it had no wagons attached to its tail.
     */
    public Wagon detachTail() {

        Wagon detachedWagon = nextWagon;
        if (hasNextWagon()){
            nextWagon = null;
            detachedWagon.previousWagon = null;
        }
        return detachedWagon;
    }

    /**
     * Detaches this wagon from the wagon in front of it.
     * No action if this wagon has no previous wagon attached.
     * @return  the former previousWagon that has been detached from,
     *          or <code>null</code> if it had no previousWagon.
     */
    public Wagon detachFront() {

        Wagon oldPreviousWagon = previousWagon;
        if (hasPreviousWagon()){    // The front can only be attached if the wagon has a previous wagon
            previousWagon = null;
            oldPreviousWagon.nextWagon = null;
        }
        return oldPreviousWagon;
    }

    /**
     * Replaces the tail of the <code>front</code> wagon by this wagon and its connected successors
     * Before such reconfiguration can be made,
     * the method first disconnects this wagon form its predecessor,
     * and the <code>front</code> wagon from its current tail.
     * @param front the wagon to which this wagon must be attached to.
     */
    public void reAttachTo(Wagon front) {

        if(front == null){
            return;
        }
        // the logic that is required to reattach is already written in other methods. Let's reuse them.
        detachFront();
        front.detachTail();
        front.attachTail(this);
    }

    /**
     * Removes this wagon from the sequence that it is part of,
     * and reconnects its tail to the wagon in front of it, if any.
     */
    public void removeFromSequence() {
        if (hasPreviousWagon() && hasNextWagon()){
            nextWagon.reAttachTo(previousWagon);
        }

        if (hasPreviousWagon() && !hasNextWagon()){
            previousWagon.detachTail();
        }

        if (!hasPreviousWagon() && hasNextWagon()){
            detachTail();
        }
    }


    /**
     * Reverses the order in the sequence of wagons from this Wagon until its final successor.
     * The reversed sequence is attached again to the wagon in front of this Wagon, if any.
     * No action if this Wagon has no succeeding next wagon attached.
     * @return the new start Wagon of the reversed sequence (with is the former last Wagon of the original sequence)
     */
    public Wagon reverseSequence() {
        Wagon oldLastWagon = getLastWagonAttached();
        if (this.equals(oldLastWagon)){ // if this wagon is the last wagon of the sequence, nothing can be reversed.
            return null;
        }
        Wagon current = this;
        Wagon temp = null;
        Wagon oldPreviousWagon = previousWagon;

        detachFront();

        /* swap next and prev for all nodes of
         doubly linked list */
        while (current != null) {
            temp = current.previousWagon;
            current.previousWagon = current.nextWagon;
            current.nextWagon = temp;
            current = current.previousWagon;
        }
        /* Before changing head, check for the cases like
         empty list and list with only one node */
        if (temp != null) {
            oldLastWagon.reAttachTo(oldPreviousWagon);
        }
        return oldLastWagon;
    }

    /**
     * Returns a string representation of the wagon.
     * This method overrides the default implementation of the {@code toString} method
     * provided by the Object class. It generates a string in the format "[Wagon-ID]" where
     * "ID" is the unique identifier of the wagon.
     * @return A string in the format "[Wagon-ID]" representing the wagon.
     */
    @Override
    public String toString() {
        return "[Wagon-" + id +"]";
    }
}
