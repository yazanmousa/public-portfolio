package org.example;

public class ForecastDisplay implements WeatherDataCallback {
    private float temperature;
    private float humidity;

    @Override
    public void onWeatherDataUpdated(float temperature, float humidity, float pressure) {
        this.temperature = temperature;
        this.humidity = humidity;
        display();
    }

    public void display() {
        System.out.println("Forecast: " + temperature + "F degrees and " + humidity + "% humidity");
    }
}

