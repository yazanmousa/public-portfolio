package sensors;

import java.util.Random;

/**
 * RainGauge is a type of sensor that measures rainfall.
 */
public class RainGauge extends Sensor {

    /**
     * Takes a random rainfall measurement between 0mm and 100mm.
     */
    @Override
    public void takeMeasurement() {
        float leftLimit = 0F;
        float rightLimit = 100F;
        value = leftLimit + new Random().nextFloat() * (rightLimit - leftLimit);
    }

    /**
     * Returns a string representation of the RainGauge reading.
     * @return A string displaying the rainfall value.
     */
    @Override
    public String toString() {
        return "RainGauge{" +
                "value=" + df.format(value) +
                " mm}";
    }
}

