package org.example;

public class WeatherStation {
    public static void main(String[] args) {
        WeatherData weatherData = new WeatherData();

        CurrentConditionsDisplay currentConditionsDisplay = new CurrentConditionsDisplay();
        ForecastDisplay forecastDisplay = new ForecastDisplay();
        StatisticsDisplay statisticsDisplay = new StatisticsDisplay();

        weatherData.addListener(currentConditionsDisplay);
        weatherData.addListener(forecastDisplay);
        weatherData.addListener(statisticsDisplay);

        // Simulate updating weather data
        weatherData.updateWeatherData(75.0f, 60.0f, 30.0f);
    }
}

