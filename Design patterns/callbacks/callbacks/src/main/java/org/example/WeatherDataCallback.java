package org.example;

public interface WeatherDataCallback {
    void onWeatherDataUpdated(float temperature, float humidity, float pressure);
}
