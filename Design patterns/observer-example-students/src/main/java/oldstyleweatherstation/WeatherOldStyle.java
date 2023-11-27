package oldstyleweatherstation;

import sensors.*;
import java.util.ArrayList;

public class WeatherOldStyle {

    private ArrayList<Sensor> sensors;

    public WeatherOldStyle() {
        this.sensors = new ArrayList<>();
        sensors.add(new RainGauge());
        sensors.add(new Thermometer());
        sensors.add (new Hygrometer());
        sensors.add (new Anemometer());
    }

    public void display(){
        System.out.println("Current weather is: ");
        for (Sensor s: sensors){
            s.takeMeasurement();
            System.out.println(s);
        }
    }


}
