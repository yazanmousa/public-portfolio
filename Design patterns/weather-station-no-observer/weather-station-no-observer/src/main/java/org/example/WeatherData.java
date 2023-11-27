package org.example;

public class WeatherData {
    private float temperature;
    private float humidity;
    private float pressure;

    public void setMeasurements(float temperature, float humidity, float pressure) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.pressure = pressure;
        measurementsChanged();
    }

    private void measurementsChanged() {
        CurrentConditionsDisplay.update(temperature, humidity, pressure);
        StatisticsDisplay.update(temperature, humidity, pressure);
        ForecastDisplay.update(temperature, humidity, pressure);
    }
}

