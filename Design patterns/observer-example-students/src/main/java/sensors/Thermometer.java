package sensors;

import java.util.Random;

/**
 * Thermometer is a type of sensor that measures temperature in degrees Celsius.
 */
public class Thermometer extends Sensor {

    /**
     * Takes a random temperature measurement between -30°C and 50°C.
     */
    @Override
    public void takeMeasurement() {
        float leftLimit = -30F;
        float rightLimit = 50F;
        value = leftLimit + new Random().nextFloat() * (rightLimit - leftLimit);
    }

    /**
     * Returns a string representation of the Thermometer reading.
     * @return A string displaying the temperature value in degrees Celsius.
     */
    @Override
    public String toString() {
        return "Thermometer{" +
                "value=" + df.format(value) +
                " degrees C}";
    }
}
