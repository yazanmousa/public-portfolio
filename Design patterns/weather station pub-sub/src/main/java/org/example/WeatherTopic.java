package org.example;

// Topics
public class WeatherTopic {
    public static final WeatherTopic TEMPERATURE = new WeatherTopic("temperature");
    public static final WeatherTopic HUMIDITY = new WeatherTopic("humidity");
    public static final WeatherTopic PRESSURE = new WeatherTopic("pressure");

    private final String name;

    private WeatherTopic(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}

