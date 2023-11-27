package org.example;

// Subscriber
public interface Subscriber {
    void onMessage(WeatherTopic topic, float value);
    float predict(float temp);
}
