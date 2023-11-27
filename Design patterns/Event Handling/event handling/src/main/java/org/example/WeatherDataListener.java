package org.example;

public interface WeatherDataListener {
    void onWeatherDataUpdated(float temperature, float humidity, float pressure);
}

