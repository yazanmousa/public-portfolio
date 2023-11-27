package org.example;

import java.util.Random;

public class GenerateRandomNumber {
    public static float randomNumber(){
        Random random = new Random();
        // Generate a random number between 1 and 10
        return random.nextInt(10) + 1;
    }
}
