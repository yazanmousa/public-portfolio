package org.example;

import java.util.Random;

public class WeatherData {
    private float temperature;
    private float humidity;
    private float pressure;

    public float getTemperature() {
        return temperature;
    }

    public float getHumidity() {
        return humidity;
    }

    public float getPressure() {
        return pressure;
    }

    // This method simulates updating weather data
    public void updateWeatherData() {
        // Update temperature, humidity, and pressure
        temperature = (float) (Math.random() * 100);
        humidity = (float) (Math.random() * 100);
        pressure = (float) (Math.random() * 100);
    }

    public float predict(){
        Random random = new Random();

        // Generate a random number between 1 and 10
        return (float) (random.nextInt(10) + 1 + temperature);
    }


}

