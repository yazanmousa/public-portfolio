package org.example;

public class CurrentConditionsDisplay {
    private static float temperature;
    private static float humidity;
    private static float pressure;

    public static void update(float temperature, float humidity, float pressure) {
        CurrentConditionsDisplay.temperature = temperature;
        CurrentConditionsDisplay.humidity = humidity;
        CurrentConditionsDisplay.pressure = pressure;
        display();
    }

    public static void display() {
        System.out.println("Current conditions: " + temperature + "F degrees and " + humidity + "% humidity");
    }
}

