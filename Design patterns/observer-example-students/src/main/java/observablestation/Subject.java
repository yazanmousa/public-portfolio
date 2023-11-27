package observablestation;

/**
 * This interface represents a Subject that can be observed by observers.
 */
public interface Subject {

    /**
     * Notifies all registered observers about updates.
     */
    void notifyObserver();

    /**
     * Registers an observer to receive updates from the subject.
     * @param observer The observer to be registered.
     */
    void registerObserver(Observer observer);

    /**
     * Removes an observer from the list of registered observers.
     * @param observer The observer to be removed.
     */
    void removeObserver(Observer observer);
}
