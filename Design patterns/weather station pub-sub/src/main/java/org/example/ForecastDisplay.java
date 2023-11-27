package org.example;

import java.util.Random;

public class ForecastDisplay implements Subscriber {
    @Override
    public void onMessage(WeatherTopic topic, float value) {
        if (topic == WeatherTopic.PRESSURE) {
            System.out.println("prediction of temperature over an hour: " + predict(value));

        }
    }

    @Override
    public float predict(float temp) {

        return GenerateRandomNumber.randomNumber() + temp;
    }
}
