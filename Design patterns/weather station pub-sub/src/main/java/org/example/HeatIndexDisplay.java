package org.example;

public class HeatIndexDisplay implements Subscriber{
    @Override
    public void onMessage(WeatherTopic topic, float value) {
        System.out.println("prediction of temperature over an hour: " + predict(value));    }

    @Override
    public float predict(float temp) {
        return GenerateRandomNumber.randomNumber() + temp;
    }
}
