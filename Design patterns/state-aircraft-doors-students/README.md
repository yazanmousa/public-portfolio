# Aircraft Door State Design Pattern

## Overview

This Java application demonstrates the use of the State design pattern to model the behavior of an aircraft door. The door can exist in various states such as Open, Closed, Armed, Locked, and Slide Deployed, each with its own set of permissible actions.

## Table of Contents

- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Classes](#classes)
- [Testing](#testing)
- [Contributing](#contributing)


## Getting Started

### Prerequisites

- Java JDK 8 or higher installed
- A Java IDE (Eclipse, IntelliJ, etc.) or a text editor for code editing

### Installation

1. Clone the repository to your local machine.
2. Open the project in your preferred Java IDE.

## Project Structure

The project is organized as follows:

- `src/`: Contains the source code files.
    - `AircraftDoor.java`: Represents an aircraft door and its associated states.
    - `Aircraft.java`: Represents an aircraft with a specific type and an associated cabin door.
    - `State.java`: Defines the State interface that all door states implement.
    - `ArmedState.java`, `ClosedState.java`, `LockedState.java`, `OpenState.java`, `SlideDeployedState.java`: Various door states.
    - `Messages.java`: Contains constant messages used throughout the application.
    - `AircraftDoorDemo.java`: Demonstrates the behavior of the aircraft door.
- `test/`: Contains JUnit test files for unit testing the code.

## Usage

To use this application, follow the steps below:

1. Open the project in your preferred Java IDE.
2. Run the `AircraftDoorDemo.java` file.
3. View the console output to see the door's behavior in different states.

## Classes

### AircraftDoor

This class represents an aircraft door and manages its state transitions.

### Aircraft

This class represents an aircraft with a specific type and an associated cabin door.

### State

The `State` interface defines the methods that each door state must implement.

### ArmedState

Represents the state of the door when it is armed.

### ClosedState

Represents the state of the door when it is closed.

### LockedState

Represents the state of the door when it is locked.

### OpenState

Represents the state of the door when it is open.

### SlideDeployedState

Represents the state of the door when the emergency slide is deployed.

## Testing

Unit tests are provided in the `DoorStateTest.java` file. These tests ensure that the door behaves correctly in different states and follows the specified state transitions.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Test thoroughly
5. Create a pull request
