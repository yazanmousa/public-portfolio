package observablestation;

import sensors.Sensor;
import java.util.ArrayList;
import java.util.List;

/**
 * This class represents a Weather Display that observes sensors and displays the current weather.
 */
public class WeatherDisplay implements Observer {

    private String name;
    private List<Sensor> sensors;

    /**
     * Constructs a WeatherDisplay with a given name.
     * @param name The name of the display.
     */
    public WeatherDisplay(String name) {
        this.name = name;
        sensors = new ArrayList<>();
    }

    /**
     * Displays the current weather based on the latest sensor readings.
     */
    public void display(){
        System.out.println(name);
        System.out.println("Current weather is: ");
        for (Sensor s: sensors){
            s.takeMeasurement();
            System.out.println(s);
        }
    }

    /**
     * Updates the list of sensors and triggers a display update.
     * @param sensors The list of sensors with their latest measurements.
     */
    @Override
    public void update(List<Sensor> sensors) {
        this.sensors = sensors;
        display();
    }
}

