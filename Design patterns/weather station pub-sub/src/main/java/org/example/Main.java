package org.example;

public class Main {
    public static void main(String[] args) {

        // Create a weather data publisher
        WeatherDataPublisher weatherDataPublisher = new WeatherDataPublisher();

        // Create display elements
        CurrentConditionsDisplay currentConditions = new CurrentConditionsDisplay();
        StatisticsDisplay statisticsDisplay = new StatisticsDisplay();
        ForecastDisplay forecastDisplay = new ForecastDisplay();
        HeatIndexDisplay heatIndexDisplay = new HeatIndexDisplay();

        // Subscribe the display elements to the weather data publisher
        weatherDataPublisher.subscribe(WeatherTopic.TEMPERATURE, currentConditions);
        weatherDataPublisher.subscribe(WeatherTopic.HUMIDITY, currentConditions);
        weatherDataPublisher.subscribe(WeatherTopic.TEMPERATURE, statisticsDisplay);
        weatherDataPublisher.subscribe(WeatherTopic.PRESSURE, forecastDisplay);
        weatherDataPublisher.subscribe(WeatherTopic.TEMPERATURE, heatIndexDisplay);


        // Publish some weather data
        weatherDataPublisher.publish(WeatherTopic.TEMPERATURE, 80);
        weatherDataPublisher.publish(WeatherTopic.HUMIDITY, 65);
        weatherDataPublisher.publish(WeatherTopic.PRESSURE, 30.4f);

    }



}
