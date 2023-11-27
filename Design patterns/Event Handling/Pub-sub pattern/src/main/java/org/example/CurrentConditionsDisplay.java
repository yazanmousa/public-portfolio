package org.example;

public class CurrentConditionsDisplay implements Subscriber {
    private float temperature;
    private float humidity;

    private WeatherData weatherData;

    public CurrentConditionsDisplay(WeatherData weatherData) {
        this.weatherData = weatherData;
    }

    @Override
    public void receiveMessage(String message) {
        // Update display with new weather data
        updateDisplay();
    }

    public void updateDisplay() {
        this.temperature = weatherData.getTemperature();
        this.humidity = weatherData.getHumidity();
        System.out.println("Current conditions: " + temperature + "F degrees and " + humidity + "% humidity");
    }
}

