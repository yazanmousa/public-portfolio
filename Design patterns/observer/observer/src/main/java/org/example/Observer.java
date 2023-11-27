package org.example;

public interface Observer {
    public void update(float temp, float humidity, float pressure);

    public float predict();
}
