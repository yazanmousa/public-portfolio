package org.example;

public class StatisticsDisplay implements WeatherDataListener {
    private float temperature;
    private float humidity;

    @Override
    public void onWeatherDataUpdated(float temperature, float humidity, float pressure) {
        this.temperature = temperature;
        this.humidity = humidity;
        display();
    }

    public void display() {
        System.out.println("Statistics: " + temperature + "F degrees and " + humidity + "% humidity");
    }
}
