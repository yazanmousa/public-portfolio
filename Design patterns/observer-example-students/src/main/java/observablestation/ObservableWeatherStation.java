package observablestation;

import sensors.*;

import java.util.ArrayList;
import java.util.List;

/**
 * This class represents an Observable Weather Station that monitors various sensors and notifies observers about changes.
 */
public class ObservableWeatherStation implements Subject {

    private List<Sensor> sensors;
    private List<Observer> observers;

    /**
     * Constructs an ObservableWeatherStation and initializes sensors.
     */
    public ObservableWeatherStation() {
        this.observers = new ArrayList<>();
        this.sensors = new ArrayList<>();
        this.sensors.add(new RainGauge());
        this.sensors.add(new Thermometer());
        this.sensors.add(new Hygrometer());
        this.sensors.add(new Anemometer());
    }

    /**
     * Checks the sensors for readings and notifies observers.
     */
    public void checkSensors(){
        for (Sensor s: sensors){
            s.takeMeasurement();
        }
        notifyObserver();
    }

    /**
     * Notifies all registered observers with the latest sensor readings.
     */
    @Override
    public void notifyObserver() {
        for (Observer observer : observers) {
            observer.update(sensors);
        }
    }

    /**
     * Registers an observer to receive updates from the weather station.
     * @param observer The observer to be registered.
     */
    @Override
    public void registerObserver(Observer observer) {
        observers.add(observer);
    }

    /**
     * Removes an observer from the list of registered observers.
     * @param observer The observer to be removed.
     */
    @Override
    public void removeObserver(Observer observer) {
        observers.remove(observer);
    }
}

