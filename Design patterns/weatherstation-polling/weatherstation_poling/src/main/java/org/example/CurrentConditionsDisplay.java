package org.example;

public class CurrentConditionsDisplay {
    private float temperature;
    private float humidity;
    private WeatherData weatherData;

    public CurrentConditionsDisplay(WeatherData weatherData) {
        this.weatherData = weatherData;
        startPolling();
    }

    public void display() {
        System.out.println("Current conditions: " + temperature + "F degrees and " + humidity + "% humidity" + "Prediction over weather over an hour: " + weatherData.predict());
    }

    public void startPolling() {
        Thread pollingThread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    try {
                        // Fetch data from WeatherData
                        temperature = weatherData.getTemperature();
                        humidity = weatherData.getHumidity();
                        // Update display
                        display();
                        // Sleep for 2 seconds
                        Thread.sleep(2000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        });
        pollingThread.start();
    }
}

