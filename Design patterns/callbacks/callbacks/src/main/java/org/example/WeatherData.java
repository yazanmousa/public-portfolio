package org.example;

import java.util.ArrayList;

public class WeatherData {

    private ArrayList<WeatherDataCallback> callbacks;
    private float temperature;
    private float humidity;
    private float pressure;


    public WeatherData() {
        this.callbacks = new ArrayList<>();
    }

    public void setCallback(WeatherDataCallback callback) {
        this.callbacks.add(callback);
    }

    public void updateWeatherData(float temperature, float humidity, float pressure) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.pressure = pressure;
        notifyCallback();
    }

    private void notifyCallback() {

        for (WeatherDataCallback callback : callbacks)
        {
            callback.onWeatherDataUpdated(temperature, humidity, pressure);
        }


    }
}
