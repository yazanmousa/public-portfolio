package sensors;

import java.util.Random;

/**
 * Hygrometer is a type of sensor that measures humidity.
 */
public class Hygrometer extends Sensor {

    /**
     * Takes a random humidity measurement between 0% and 100%.
     */
    @Override
    public void takeMeasurement() {
        float leftLimit = 0F;
        float rightLimit = 100F;
        value = leftLimit + new Random().nextFloat() * (rightLimit - leftLimit);
    }

    /**
     * Returns a string representation of the Hygrometer reading.
     * @return A string displaying the humidity value.
     */
    @Override
    public String toString() {
        return "Hygrometer{" +
                "value=" + df.format(value) +
                "%}";
    }
}
