package org.example;

public class ForecastDisplay {
    private static float temperature;
    private static float humidity;
    private static float pressure;

    public static void update(float temperature, float humidity, float pressure) {
        ForecastDisplay.temperature = temperature;
        ForecastDisplay.humidity = humidity;
        ForecastDisplay.pressure = pressure;
        display();
    }

    public static void display() {
        System.out.println("Forecast: " + temperature + "F degrees and " + humidity + "% humidity");
    }
}

