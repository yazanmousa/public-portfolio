package org.example;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

// Publisher
public class WeatherDataPublisher {
    private final Map<WeatherTopic, List<Subscriber>> subscribers = new HashMap<>();

    public void subscribe(WeatherTopic topic, Subscriber subscriber) {
        subscribers.computeIfAbsent(topic, k -> new ArrayList<>()).add(subscriber);
    }

    public void publish(WeatherTopic topic, float value) {
        subscribers.get(topic).forEach(subscriber -> subscriber.onMessage(topic, value));
    }
}

