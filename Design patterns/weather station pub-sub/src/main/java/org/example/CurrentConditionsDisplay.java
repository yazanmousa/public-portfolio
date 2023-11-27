package org.example;

// Display elements
public class CurrentConditionsDisplay implements Subscriber {
    @Override
    public void onMessage(WeatherTopic topic, float value) {
        if (topic == WeatherTopic.TEMPERATURE) {
            System.out.println("Current temperature: " + value);
        } else if (topic == WeatherTopic.HUMIDITY) {
            System.out.println("Current humidity: " + value + "%");
        }
        System.out.println("prediction of temperature over an hour: " + predict(value));
    }

    @Override
    public float predict(float temp) {
        return GenerateRandomNumber.randomNumber() + temp;
    }
}
