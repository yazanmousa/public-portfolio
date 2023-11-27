package org.example;
public class WeatherStation {
    public static void main(String[] args) {
        MessageBus messageBus = new MessageBus();



        WeatherData weatherData = new WeatherData(messageBus);
        CurrentConditionsDisplay currentConditionsDisplay = new CurrentConditionsDisplay(weatherData);
        ForecastDisplay forecastDisplay = new ForecastDisplay(weatherData);
        StatisticsDisplay statisticsDisplay = new StatisticsDisplay(weatherData);

        messageBus.subscribe(currentConditionsDisplay);
        messageBus.subscribe(forecastDisplay);
        messageBus.subscribe(statisticsDisplay);

        // Simulate updating weather data
        weatherData.updateWeatherData(75.0f, 60.0f, 30.0f);
        weatherData.updateWeatherData(76,30, 50);
    }
}


