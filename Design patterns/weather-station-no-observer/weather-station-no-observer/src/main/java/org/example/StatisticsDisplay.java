package org.example;

public class StatisticsDisplay {
    private static float temperature;
    private static float humidity;
    private static float pressure;

    public static void update(float temperature, float humidity, float pressure) {
        StatisticsDisplay.temperature = temperature;
        StatisticsDisplay.humidity = humidity;
        StatisticsDisplay.pressure = pressure;
        display();
    }

    public static void display() {
        System.out.println("Statistics: " + temperature + "F degrees and " + humidity + "% humidity");
    }
}

