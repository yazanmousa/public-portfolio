package sensors;

import java.util.Random;

/**
 * Anemometer is a type of sensor that measures wind speed.
 */
public class Anemometer extends Sensor {

    /**
     * Takes a random wind speed measurement between 0 and 80 knots.
     */
    @Override
    public void takeMeasurement() {
        float leftLimit = 0F;
        float rightLimit = 80F;
        value = leftLimit + new Random().nextFloat() * (rightLimit - leftLimit);
    }

    /**
     * Returns a string representation of the Anemometer reading.
     * @return A string displaying the wind speed value.
     */
    @Override
    public String toString() {
        return "Anemometer{" +
                "value=" + df.format(value) +
                " knots}";
    }
}
