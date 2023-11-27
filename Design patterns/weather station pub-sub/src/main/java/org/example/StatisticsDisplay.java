package org.example;

public class StatisticsDisplay implements Subscriber {
    @Override
    public void onMessage(WeatherTopic topic, float value) {
        if (topic == WeatherTopic.TEMPERATURE) {
            System.out.println("stats");
        }
        System.out.println("prediction of temperature over an hour: " + predict(value));

    }

    @Override
    public float predict(float temp) {
        return GenerateRandomNumber.randomNumber() + temp;

    }
}
