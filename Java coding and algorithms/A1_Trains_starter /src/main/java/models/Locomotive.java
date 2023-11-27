package models;

public class Locomotive {
    private int locNumber;
    private int maxWagons;


    public Locomotive(int locNumber, int maxWagons) {
        this.locNumber = locNumber;
        this.maxWagons = maxWagons;
    }

    //Getters and setters

    public int getMaxWagons() {
        return maxWagons;
    }

    public int getLocNumber() {
        return locNumber;
    }

    public void setLocNumber(int locNumber) {
        this.locNumber = locNumber;
    }

    public void setMaxWagons(int maxWagons) {
        this.maxWagons = maxWagons;
    }

    @Override
    public String toString() {
        return String.valueOf(locNumber + maxWagons);
    }
}
