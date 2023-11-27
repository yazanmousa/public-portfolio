package observablestation;

import sensors.Sensor;

import java.util.List;

/**
 * This interface represents an Observer that receives updates from the ObservableWeatherStation.
 */
public interface Observer {
    /**
     * This method is called by the ObservableWeatherStation to update the observer with the latest sensor readings.
     * @param sensors The list of sensors with their latest measurements.
     */
    void update(List<Sensor> sensors);
}
