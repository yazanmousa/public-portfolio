# Weather Monitoring System

This project implements a Weather Monitoring System that simulates the functioning of a weather station. It includes classes for various sensors (Rain Gauge, Thermometer, Hygrometer, Anemometer) and a display unit to visualize the weather data.

## Table of Contents

- [Project Structure](#project-structure)
- [How to Use](#how-to-use)
- [Sensor Classes](#sensor-classes)
- [ObservableWeatherStation](#observableweatherstation)
- [WeatherDisplay](#weatherdisplay)
- [OldStyleWeatherStation](#oldstyleweatherstation)
- [Contributing](#contributing)

## Project Structure

```
.
├── observablestation
│   ├── ObservableWeatherStation.java
│   ├── Observer.java
│   ├── Subject.java
│   ├── WeatherDisplay.java
├── oldstyleweatherstation
│   ├── OldStyleWSRunner.java
│   ├── WeatherOldStyle.java
├── sensors
│   ├── Anemometer.java
│   ├── Hygrometer.java
│   ├── RainGauge.java
│   ├── Sensor.java
│   ├── Thermometer.java
└── README.md
```

## How to Use

1. Clone the repository to your local machine.
2. Compile and run the `OldStyleWSRunner.java` file to use the OldStyleWeatherStation.
3. Compile and run the `ObservableWeatherStation.java` file to use the ObservableWeatherStation with Observers.

## Sensor Classes

- `Anemometer`: Measures wind speed.
- `Hygrometer`: Measures humidity.
- `RainGauge`: Measures rainfall.
- `Thermometer`: Measures temperature in degrees Celsius.
- `Sensor`: Abstract class providing a framework for sensor functionality.

## ObservableWeatherStation

This class represents a weather station that observes sensor data and notifies registered observers about changes.

## WeatherDisplay

This class represents a display unit that observes sensor data and displays the current weather.

## OldStyleWeatherStation

This class represents an older style weather station that directly interacts with sensors and displays weather information.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear commit messages.
4. Push your changes to your fork.
5. Submit a pull request with a description of your changes.
