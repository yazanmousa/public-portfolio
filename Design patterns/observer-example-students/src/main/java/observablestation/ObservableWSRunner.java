package observablestation;

public class ObservableWSRunner {

    public static void main (String args[]){
        ObservableWeatherStation observableWeatherStation = new ObservableWeatherStation();
        print ("No Observers");
        observableWeatherStation.checkSensors();
        print ("************");
        WeatherDisplay livingRoomDisplay = new WeatherDisplay("Living Room");
        observableWeatherStation.registerObserver(livingRoomDisplay);
        print ("One Observer");
        observableWeatherStation.checkSensors();
        print ("************");
        WeatherDisplay bedRoomDisplay = new WeatherDisplay("Bedroom");
        observableWeatherStation.registerObserver(bedRoomDisplay);
        print ("Two Observers");
        observableWeatherStation.checkSensors();
        print ("************");
        observableWeatherStation.removeObserver(livingRoomDisplay);
        print ("One Observer");
        observableWeatherStation.checkSensors();

    }
    private static void print (String message){
        System.out.println(message);
    }
}
