package org.example;

public class WeatherData {
    private MessageBus messageBus;
    private float temperature;
    private float humidity;
    private float pressure;

    public WeatherData(MessageBus messageBus) {
        this.messageBus = messageBus;
    }

    public void updateWeatherData(float temperature, float humidity, float pressure) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.pressure = pressure;
        messageBus.publishMessage("Weather data updated");
    }

    public float getTemperature() {
        return temperature;
    }

    public float getHumidity() {
        return humidity;
    }

    public float getPressure() {
        return pressure;
    }
}

