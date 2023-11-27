package sensors;

import java.text.DecimalFormat;

/**
 * Abstract class representing a sensor for measuring environmental parameters.
 */
public abstract class Sensor {

    /**
     * Decimal format used for displaying sensor measurements.
     */
    public static final DecimalFormat df = new DecimalFormat("0.00");

    /**
     * The measured value from the sensor.
     */
    float value;

    /**
     * Default constructor for Sensor.
     */
    public Sensor(){

    }

    /**
     * Abstract method for taking a measurement with the sensor.
     */
    public abstract void takeMeasurement();

    /**
     * Gets the current measurement value from the sensor.
     * @return The current measurement value.
     */
    public float getMeasurement(){
        return value;
    }
}
