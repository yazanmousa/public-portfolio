package org.example;

import java.util.ArrayList;
import java.util.List;

public class WeatherData {
    private List<WeatherDataListener> listeners = new ArrayList<>();
    private float temperature;
    private float humidity;
    private float pressure;

    public void addListener(WeatherDataListener listener) {
        listeners.add(listener);
    }

    public void removeListener(WeatherDataListener listener) {
        listeners.remove(listener);
    }

    public void updateWeatherData(float temperature, float humidity, float pressure) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.pressure = pressure;
        notifyListeners();
    }

    private void notifyListeners() {
        for (WeatherDataListener listener : listeners) {
            listener.onWeatherDataUpdated(temperature, humidity, pressure);
        }
    }
}

